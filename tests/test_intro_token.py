"""Tests for the INTRO token rendered by `native.templates._intro.intro`.

Regression coverage for a bug where the Shimmer docs page
(`docs/utilities/shimmer.md`) carries an `--INTRO([Shimmer, ...])--` token
but `shimmer` is not a `COMPONENT_REGISTRY` entry — it is a pure-CSS
utility injected into `globals.css` by `buridan init` via
`cli.main.UTILITIES_BUNDLE`.

Root cause: `intro()` derived `slug = title.lower().replace(" ", "_")`
and unconditionally rendered `buridan add {slug}`, assuming every INTRO'd
page is a registry component. For `shimmer` that produced copyable
commands which the CLI rejects with
`Warning: Component 'shimmer' not found in registry.` and exit code 1,
directly contradicting the page's own prose ("you already have shimmer"
via `buridan init`).

Fix: `intro()` now branches on `slug in COMPONENT_REGISTRY`. Registry
components still get `buridan add <slug>`; non-registry utilities get
`buridan init` (the command that actually ships the utility).
"""

from __future__ import annotations

from pathlib import Path

import reflex as rx

from native.engine.parser import parse_and_render
from native.registry.components import COMPONENT_REGISTRY
from native.templates._intro import intro

_SHIMMER_DOC = (
    Path(__file__).resolve().parent.parent / "docs" / "utilities" / "shimmer.md"
)

REGISTRY_COMPONENT = "button"


def test_intro_non_registry_utility_renders_init_not_add() -> None:
    """A non-registry INTRO title (e.g. Shimmer) must render `buridan init`
    install commands, never `buridan add <slug>` — the latter prints
    "Component '<slug>' not found in registry." and exits 1.
    """
    component = intro(
        "[Shimmer, Utilities for adding a shimmer effect to text elements.]",
    )
    rendered = repr(component)

    assert "buridan init" in rendered
    assert "uv run buridan init" in rendered
    assert "python -m buridan init" in rendered

    assert "buridan add shimmer" not in rendered
    assert "uv run buridan add shimmer" not in rendered
    assert "python -m buridan add shimmer" not in rendered


def test_intro_registry_component_renders_add_not_init() -> None:
    """Regression: a registry component (e.g. Button) must keep rendering
    `buridan add <slug>` install commands — the fix must not reroute
    real components onto the `buridan init` path.
    """
    assert REGISTRY_COMPONENT in COMPONENT_REGISTRY

    component = intro(f"[{REGISTRY_COMPONENT.title()}, A clickable button.]")
    rendered = repr(component)

    assert f"buridan add {REGISTRY_COMPONENT}" in rendered
    assert f"uv run buridan add {REGISTRY_COMPONENT}" in rendered
    assert f"python -m buridan add {REGISTRY_COMPONENT}" in rendered

    assert "buridan init" not in rendered


def test_parse_and_render_shimmer_doc_has_no_broken_add_command() -> None:
    """End-to-end: rendering the real `docs/utilities/shimmer.md` through
    the production parser pipeline produces the init install block and
    never produces the broken `buridan add shimmer` string anywhere in
    the rendered component tree.
    """
    pieces = parse_and_render(_SHIMMER_DOC.read_text())
    assert pieces, "shimmer.md should render at least one component"
    assert all(isinstance(p, rx.Component) for p in pieces)

    joined = "".join(repr(p) for p in pieces)
    assert "buridan add shimmer" not in joined
    assert "uv run buridan add shimmer" not in joined
    assert "python -m buridan add shimmer" not in joined

    assert "buridan init" in joined
    assert "uv run buridan init" in joined
    assert "python -m buridan init" in joined
