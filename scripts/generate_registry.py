#!/usr/bin/env python3
"""
generate_registry.py

Regenerates `registry/components.py` (COMPONENT_REGISTRY) by scanning the
actual source tree and parsing real import statements -- instead of
hand-maintaining the dependency dict.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_ROOTS = ["components", "native/lib/blocks"]
DEFAULT_OUT = "native/registry/components.py"


@dataclass
class ComponentFile:
    name: str  # registry key
    path: Path  # absolute path on disk
    rel_path: str  # path to record in the registry (posix, relative to repo root)
    dotted_module: str  # e.g. components.ui.button
    package_dotted: str  # dotted package the file lives in, e.g. components.ui
    group: str  # top-level folder used for section headers, e.g. "components/ui"
    dependencies: set[str] = field(default_factory=set)


def discover_files(repo_root: Path, roots: list[str]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        root_path = repo_root / root
        if not root_path.exists():
            print(f"  (skipping missing root: {root})", file=sys.stderr)
            continue
        for p in sorted(root_path.rglob("*.py")):
            if p.name == "__init__.py":
                continue
            if "__pycache__" in p.parts or "__MACOSX" in p.parts:
                continue
            files.append(p)
    return files


def _unique_name(stem: str, rel_path: str, seen: dict[str, str]) -> str:
    if stem not in seen:
        seen[stem] = rel_path
        return stem
    disambiguated = f"{Path(rel_path).parent.name}_{stem}"
    print(
        f"  WARNING: duplicate component name '{stem}' "
        f"({seen[stem]} vs {rel_path}). Using '{disambiguated}' for the latter.",
        file=sys.stderr,
    )
    return disambiguated


def build_component_index(
    repo_root: Path, files: list[Path]
) -> dict[str, ComponentFile]:
    by_name: dict[str, ComponentFile] = {}
    seen_stems: dict[str, str] = {}

    for path in files:
        rel = path.relative_to(repo_root)
        rel_posix = rel.as_posix()
        stem = path.stem

        if re.match(r"^v\d+(?:_\d+)*$", stem) and len(path.parent.name) > 0:
            component_name = path.parent.name
            version = stem[1:].replace("_", ".")
            name = _unique_name(f"{component_name}@{version}", rel_posix, seen_stems)
        else:
            name = _unique_name(stem, rel_posix, seen_stems)

        module_parts = rel.with_suffix("").parts
        dotted_module = ".".join(module_parts)
        package_dotted = ".".join(module_parts[:-1])
        group = "/".join(rel.parts[:-1]) or "."

        by_name[name] = ComponentFile(
            name=name,
            path=path,
            rel_path=rel_posix,
            dotted_module=dotted_module,
            package_dotted=package_dotted,
            group=group,
        )

    return by_name


def resolve_relative_module(package_dotted: str, level: int, module: str | None) -> str:
    parts = package_dotted.split(".") if package_dotted else []
    if level > 1:
        parts = parts[: len(parts) - (level - 1)]
    if module:
        parts = parts + module.split(".")
    return ".".join(parts)


def find_dependencies(comp: ComponentFile, module_lookup: dict[str, str]) -> set[str]:
    deps: set[str] = set()
    try:
        tree = ast.parse(comp.path.read_text(encoding="utf-8"), filename=str(comp.path))
    except SyntaxError as e:
        print(f"  WARNING: could not parse {comp.rel_path}: {e}", file=sys.stderr)
        return deps

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                base = resolve_relative_module(
                    comp.package_dotted, node.level, node.module
                )
            else:
                base = node.module or ""

            if base in module_lookup and module_lookup[base] != comp.name:
                deps.add(module_lookup[base])

            for alias in node.names:
                candidate = f"{base}.{alias.name}" if base else alias.name
                if candidate in module_lookup and module_lookup[candidate] != comp.name:
                    deps.add(module_lookup[candidate])

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if (
                    alias.name in module_lookup
                    and module_lookup[alias.name] != comp.name
                ):
                    deps.add(module_lookup[alias.name])

    return deps


def find_package_aliases(
    repo_root: Path, roots: list[str], module_lookup: dict[str, str]
) -> dict[str, str]:
    """Versioned components (e.g. a `button/` folder containing v1.py/v2.py)
    need an `__init__.py` that re-exports one version, e.g.:

        # components/ui/button/__init__.py
        from .v2 import button

    so that sibling files can keep doing `from .button import button` the
    normal Python way. That package-level dotted path
    (`components.ui.button`) never appears in `module_lookup` on its own --
    only the versioned files do (`components.ui.button.v1`, `.v2`) -- because
    __init__.py files are excluded from being components themselves.

    This scans __init__.py files, follows their own re-export imports, and
    registers an alias: package dotted path -> whichever versioned
    component that package's __init__.py actually re-exports. That lets
    find_dependencies() understand `from .button import button` correctly,
    instead of silently missing the edge.
    """
    aliases: dict[str, str] = {}

    for root in roots:
        root_path = repo_root / root
        if not root_path.exists():
            continue

        for init_path in sorted(root_path.rglob("__init__.py")):
            rel = init_path.relative_to(repo_root)
            module_parts = rel.with_suffix("").parts  # (..., "button", "__init__")
            package_dotted = ".".join(module_parts[:-1])
            if not package_dotted:
                continue

            try:
                tree = ast.parse(
                    init_path.read_text(encoding="utf-8"), filename=str(init_path)
                )
            except SyntaxError as e:
                print(
                    f"  WARNING: could not parse {rel.as_posix()}: {e}",
                    file=sys.stderr,
                )
                continue

            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom):
                    continue

                if node.level and node.level > 0:
                    base = resolve_relative_module(
                        package_dotted, node.level, node.module
                    )
                else:
                    base = node.module or ""

                if base not in module_lookup:
                    continue

                target = module_lookup[base]
                if package_dotted in aliases and aliases[package_dotted] != target:
                    print(
                        f"  WARNING: {rel.as_posix()} appears to re-export more than "
                        f"one version ({aliases[package_dotted]} and {target}); "
                        f"keeping '{aliases[package_dotted]}'.",
                        file=sys.stderr,
                    )
                    continue
                aliases[package_dotted] = target

    return aliases


def build_registry(repo_root: Path, roots: list[str]) -> dict[str, ComponentFile]:
    files = discover_files(repo_root, roots)
    if not files:
        print(
            "No component files found -- check your --roots argument.", file=sys.stderr
        )
        sys.exit(1)

    by_name = build_component_index(repo_root, files)
    module_lookup = {c.dotted_module: c.name for c in by_name.values()}

    aliases = find_package_aliases(repo_root, roots, module_lookup)
    for package_dotted, target in aliases.items():
        if package_dotted in module_lookup and module_lookup[package_dotted] != target:
            print(
                f"  WARNING: '{package_dotted}' is both a real component "
                f"({module_lookup[package_dotted]}) and an __init__.py re-export "
                f"alias ({target}); keeping the real component.",
                file=sys.stderr,
            )
            continue
        module_lookup[package_dotted] = target

    for comp in by_name.values():
        comp.dependencies = find_dependencies(comp, module_lookup)

    return by_name


def render_registry(by_name: dict[str, ComponentFile]) -> str:
    groups: dict[str, list[ComponentFile]] = {}
    for comp in by_name.values():
        groups.setdefault(comp.group, []).append(comp)

    lines = [
        '"""Buridan UI Component Registry.',
        "",
        "AUTO-GENERATED by scripts/generate_registry.py -- do not edit by hand.",
        "Re-run the script after adding/moving/renaming component files.",
        '"""',
        "",
        "COMPONENT_REGISTRY = {",
    ]

    for group in sorted(groups):
        lines.append(f"    # --- {group} ---")
        for comp in sorted(groups[group], key=lambda c: c.name):
            deps = ", ".join(f'"{d}"' for d in sorted(comp.dependencies))
            lines.append(f'    "{comp.name}": {{')
            lines.append(f'        "files": ["{comp.rel_path}"],')
            lines.append(f'        "dependencies": [{deps}],')
            lines.append("    },")
        lines.append("")

    if lines[-1] == "":
        lines.pop()
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--roots", nargs="+", default=DEFAULT_ROOTS)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    print(
        f"Scanning: {', '.join(args.roots)} (repo root: {repo_root})", file=sys.stderr
    )
    by_name = build_registry(repo_root, args.roots)
    rendered = render_registry(by_name)

    out_path = repo_root / args.out

    if args.check:
        existing = out_path.read_text(encoding="utf-8") if out_path.exists() else None
        if existing == rendered:
            print("Registry is up to date.", file=sys.stderr)
            sys.exit(0)
        else:
            print(
                "Registry is OUT OF DATE. Run without --check to regenerate.",
                file=sys.stderr,
            )
            sys.exit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {len(by_name)} components to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
