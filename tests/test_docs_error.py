"""Scans every markdown file under assets/docs/ for component-resolution
errors that indicate a doc's embedded demo/code reference (e.g. a
--DEMO(...)-- block) failed to resolve to a real component, such as:

    Component `button_group_select` not found
    Component `input_group` not found

These strings mean something in the doc didn't get parsed/rendered
correctly and needs fixing in either the markdown or the component
registry — this test exists to catch that automatically instead of
someone spotting it by eye while browsing the docs site.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# Matches: Component `<anything except a backtick>` not found
# Extend this if other renderers/registries use a differently-worded error.
COMPONENT_NOT_FOUND_RE = re.compile(r"Component `([^`]+)` not found")


def _find_docs_dir() -> Path:
    """Locate assets/docs/, searching upward from this file if the current
    working directory isn't the repo root (e.g. running pytest from a
    subdirectory, or from an IDE's own cwd)."""
    candidate = Path.cwd() / "assets" / "docs"
    if candidate.is_dir():
        return candidate

    for parent in Path(__file__).resolve().parents:
        candidate = parent / "assets" / "docs"
        if candidate.is_dir():
            return candidate

    raise FileNotFoundError(
        "Could not locate an 'assets/docs' directory from the current "
        "working directory or any parent of this test file. If your docs "
        "live somewhere else, update _find_docs_dir()."
    )


def _iter_markdown_files(docs_dir: Path) -> list[Path]:
    return sorted(p for ext in ("*.md", "*.mdx") for p in docs_dir.rglob(ext))


DOCS_DIR = _find_docs_dir()
MARKDOWN_FILES = _iter_markdown_files(DOCS_DIR)


def test_docs_dir_is_not_empty():
    """Sanity check for the parametrized test below.

    If MARKDOWN_FILES is empty, pytest.mark.parametrize silently generates
    zero test cases rather than failing — so test_no_unresolved_components
    would report "0 passed" and look completely fine while actually
    checking nothing. This test exists so a broken glob/path shows up as an
    explicit failure instead of quiet false confidence.
    """
    assert MARKDOWN_FILES, f"No markdown files found under {DOCS_DIR}"


@pytest.mark.parametrize(
    "md_file",
    MARKDOWN_FILES,
    ids=[str(p.relative_to(DOCS_DIR)) for p in MARKDOWN_FILES],
)
def test_no_unresolved_components(md_file: Path):
    content = md_file.read_text(encoding="utf-8")
    matches = COMPONENT_NOT_FOUND_RE.findall(content)

    assert not matches, (
        f"{md_file.relative_to(DOCS_DIR)} references component(s) that "
        f"failed to resolve: {', '.join(sorted(set(matches)))}"
    )
