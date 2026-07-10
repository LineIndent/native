import importlib
import inspect
import pathlib
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, Tuple

# Add project root
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from native.registry.components import COMPONENT_REGISTRY


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

DOCS_SOURCE_DIR = ROOT_DIR / "docs"
MARKDOWN_OUTPUT_DIR = ROOT_DIR / "assets" / "docs"

DYNAMIC_LOAD_DIRS = [
    "native/lib",
    "components",
]


# ---------------------------------------------------------
# LIVE REGISTRY
# ---------------------------------------------------------

def build_live_registry(dirs: list[str]) -> Dict[str, Tuple[object, str]]:
    registry = {}

    for folder in dirs:
        base = ROOT_DIR / folder

        if not base.exists():
            continue

        for py_file in base.rglob("*.py"):
            if py_file.name.startswith("__"):
                continue

            module_name = ".".join(
                py_file.relative_to(ROOT_DIR)
                .with_suffix("")
                .parts
            )

            try:
                module = importlib.import_module(module_name)
            except Exception as e:
                print(f"Could not import {module_name}: {e}")
                continue

            for name, obj in vars(module).items():
                if name.startswith("_"):
                    continue

                if (
                    inspect.isfunction(obj)
                    or inspect.isclass(obj)
                    or callable(obj)
                ):
                    if getattr(obj, "__module__", None) == module_name:
                        registry[name.lower()] = (obj, name)

    return registry


LIVE_REGISTRY = build_live_registry(DYNAMIC_LOAD_DIRS)


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def clean_arg(value: str | None) -> str:
    return (
        (value or "")
        .strip()
        .strip("'\"[]{}")
        .lower()
    )


def get_dependencies(name: str):
    ordered = []

    def resolve(component):
        data = COMPONENT_REGISTRY.get(component.lower())

        if not data:
            return

        for dep in data.get("dependencies", []):
            if dep not in ordered:
                resolve(dep)

        if component not in ordered:
            ordered.append(component)

    resolve(name)

    return ordered


def read_component_files(name: str):
    output = []

    for dep in get_dependencies(name):
        data = COMPONENT_REGISTRY.get(dep, {})

        for file_path in data.get("files", []):
            path = Path(file_path)

            if not path.exists():
                continue

            output.append(path.read_text().strip())

    return output


# ---------------------------------------------------------
# TOKEN CONVERSION
# ---------------------------------------------------------

TOKEN_RE = r"--([\w_]+)(?:\((.*)\))?--"


def convert_to_markdown(content: str):

    def replace(match):

        cmd = match.group(1).lower()
        name = clean_arg(match.group(2))

        try:

            # -----------------------------
            # INSTALL / SOURCE
            # -----------------------------

            if cmd in ("install", "source"):

                files = read_component_files(name)

                if not files:
                    return (
                        f"\n> No source found for `{name}`\n"
                    )

                return "\n\n".join(
                    f"```python\n{src}\n```"
                    for src in files
                )


            # -----------------------------
            # USAGE
            # -----------------------------

            if cmd == "usage":

                entry = LIVE_REGISTRY.get(name)

                if not entry:
                    return (
                        f"\n> Component `{name}` not found\n"
                    )

                obj, preferred_name = entry

                file = Path(
                    inspect.getfile(obj)
                ).stem

                return (
                    "```python\n"
                    f"from components.ui.{file} "
                    f"import {preferred_name}\n"
                    "```"
                )


            # -----------------------------
            # DEMO
            # -----------------------------

            if cmd == "demo":

                entry = LIVE_REGISTRY.get(name)

                if not entry:
                    return (
                        f"\n> Component `{name}` not found\n"
                    )

                obj, _ = entry

                source = inspect.getsource(obj)

                return (
                    "```python\n"
                    f"{source.strip()}\n"
                    "```"
                )


            # -----------------------------
            # INTRO
            # -----------------------------

            if cmd == "intro":

                return (
                    f"\n## {name.title()}\n"
                )


            return (
                f"\n> Unknown token `{cmd}`\n"
            )


        except Exception as e:
            return (
                f"\n> Error processing `{cmd}`: {e}\n"
            )


    return re.sub(
        TOKEN_RE,
        replace,
        content
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("Generating markdown docs...")

    if MARKDOWN_OUTPUT_DIR.exists():
        shutil.rmtree(MARKDOWN_OUTPUT_DIR)

    MARKDOWN_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    count = 0

    for md_file in DOCS_SOURCE_DIR.rglob("*.md"):

        count += 1

        content = md_file.read_text()

        markdown = convert_to_markdown(content)

        relative = md_file.relative_to(
            DOCS_SOURCE_DIR
        )

        output = MARKDOWN_OUTPUT_DIR / relative

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output.write_text(
            markdown,
            newline=""
        )

        print(
            f"{output}"
        )

    print(
        f"Done. Processed {count} files."
    )


if __name__ == "__main__":
    main()
