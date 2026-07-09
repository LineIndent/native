#!/usr/bin/env python3
"""
generate_registry.py

Regenerates `registry/components.py` (COMPONENT_REGISTRY) by scanning the
actual source tree and parsing real import statements -- instead of
hand-maintaining the dependency dict.

Why this approach:
    Your folder structure keeps changing (e.g. twmerge.py / component.py /
    base_ui.py / others.py all got merged into a single core.py per package).
    Rather than re-editing a dict by hand every time that happens, this
    script treats each *file* as a component, and derives its dependencies
    by literally parsing the `import` statements in that file with Python's
    `ast` module. If a file imports from another file that is also a known
    component, that becomes a dependency edge. No guessing, no drift.

Usage:
    python scripts/generate_registry.py
    python scripts/generate_registry.py --check        # CI mode: no write, exit 1 on diff
    python scripts/generate_registry.py --roots components app/www/library/blocks
    python scripts/generate_registry.py --out registry/components.py

Assumptions (tell me if any of these are wrong and I'll adjust):
    - Each component == one .py file (excluding __init__.py) under one of
      the scanned root folders.
    - The component's registry "name" is the file's stem (e.g. button.py -> "button").
      If you ever have duplicate stems across folders, the script will
      warn and disambiguate them (see `_unique_name`).
    - Dependencies are discovered from relative imports (`from .core import X`,
      `from ..icons.hugeicon import hi`) and from absolute imports that
      resolve inside one of the scanned roots (`from components.ui.button import button`).
    - External/third-party imports (reflex, typing, etc.) are ignored --
      they're not part of your internal dependency graph.
"""

from __future__ import annotations

import argparse
import ast
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
    """Find every .py file under the given roots, skipping __init__.py,
    __pycache__, and macOS junk."""
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
    """Return a registry-safe unique name for this file. Warns on collision
    and disambiguates using the parent folder name."""
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
    """Create the name -> ComponentFile map, and a dotted-module lookup
    table used later to resolve imports to components."""
    by_name: dict[str, ComponentFile] = {}
    seen_stems: dict[str, str] = {}

    for path in files:
        rel = path.relative_to(repo_root)
        rel_posix = rel.as_posix()
        stem = path.stem
        name = _unique_name(stem, rel_posix, seen_stems)

        module_parts = rel.with_suffix("").parts  # e.g. ('components','ui','button')
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
    """Mimic Python's own relative-import resolution.
    level=1 -> current package. level=2 -> parent package. etc.
    """
    parts = package_dotted.split(".") if package_dotted else []
    if level > 1:
        parts = parts[: len(parts) - (level - 1)]
    if module:
        parts = parts + module.split(".")
    return ".".join(parts)


def find_dependencies(comp: ComponentFile, module_lookup: dict[str, str]) -> set[str]:
    """Parse the file's AST and match imports against known components."""
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

            # Case 1: `from .core import cn` -> base itself is the target module
            if base in module_lookup and module_lookup[base] != comp.name:
                deps.add(module_lookup[base])

            # Case 2: `from . import button` / `from components.ui import button`
            # -> the imported *name* is actually a submodule
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


def build_registry(repo_root: Path, roots: list[str]) -> dict[str, ComponentFile]:
    files = discover_files(repo_root, roots)
    if not files:
        print(
            "No component files found -- check your --roots argument.", file=sys.stderr
        )
        sys.exit(1)

    by_name = build_component_index(repo_root, files)
    module_lookup = {c.dotted_module: c.name for c in by_name.values()}

    for comp in by_name.values():
        comp.dependencies = find_dependencies(comp, module_lookup)

    return by_name


def render_registry(by_name: dict[str, ComponentFile]) -> str:
    """Render COMPONENT_REGISTRY as nicely grouped, deterministic Python source."""
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
    parser.add_argument(
        "--roots",
        nargs="+",
        default=DEFAULT_ROOTS,
        help=f"Folders (relative to repo root) to scan for components. Default: {DEFAULT_ROOTS}",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help=f"Output path for the generated registry (relative to repo root). Default: {DEFAULT_OUT}",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Don't write the file. Exit with code 1 if the generated content would differ from what's on disk.",
    )
    args = parser.parse_args()

    # repo root = parent of this script's `scripts/` folder
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
