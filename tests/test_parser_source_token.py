# noqa: INP001
"""Tests for the SOURCE branch of `native.engine.parser.render_token`.

Regression coverage for a crash where a `--SOURCE(name)--` token naming a
component not present in `COMPONENT_REGISTRY` (or whose dependency files
could not be read) made `render_token` raise
`TypeError: cannot unpack non-iterable P object`, aborting `reflex run` /
`reflex export` at app-import time.

Root cause: `_render_install` has a dual return type — a `(name, files)`
tuple on success and an `rx.el.p(...)` Component on either failure path
(empty dependency set, or OSError while reading a dependency file). The
SOURCE branch unconditionally unpacked the return value without checking
the type, so any failure path crashed the build.
"""

from __future__ import annotations

import pytest  # pyrefly: ignore[missing-import]
import reflex as rx  # pyrefly: ignore[missing-import]

from native.engine.parser import render_token

UNKNOWN_COMPONENT = "definitely_not_a_real_component_xyz"
KNOWN_COMPONENT = "button"


@pytest.mark.parametrize("bad_name", [UNKNOWN_COMPONENT, "buton"])  # pyright: ignore[reportUntypedFunctionDecorator]
def test_source_token_unknown_component_does_not_raise(bad_name: str) -> None:
    """A SOURCE token for a name not in COMPONENT_REGISTRY (a typo or
    genuinely missing component) must return a renderable error Component
    instead of raising TypeError and aborting the docs build.
    """
    result = render_token("source", bad_name)
    assert isinstance(result, rx.Component)
    assert "Installation payload empty" in repr(result)


def test_source_token_known_component_renders_source_block() -> None:
    """Regression: a valid SOURCE token still renders the source-code /
    dependency block, not the error paragraph.
    """
    result = render_token("source", KNOWN_COMPONENT)
    assert isinstance(result, rx.Component)
    assert "Source Code & Dependencies" in repr(result)
    assert "Installation payload empty" not in repr(result)


def test_source_token_oserror_failure_path(monkeypatch: pytest.MonkeyPatch) -> None:
    """The OSError path of `_render_install` (a registered component's
    dependency file becomes unreadable on disk) must also return an error
    Component instead of crashing the SOURCE branch — same root cause,
    different trigger than the unknown-name path.
    """
    import native.engine.parser as parser_mod

    def _raise_oserror(_self: object, *_args: object, **_kwargs: object) -> str:
        msg = "simulated unreadable file (test)"
        raise OSError(msg)

    monkeypatch.setattr(parser_mod.Path, "read_text", _raise_oserror)

    result = render_token("source", KNOWN_COMPONENT)
    assert isinstance(result, rx.Component)
    assert "Error reading file dependency path" in repr(result)
