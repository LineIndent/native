"""Tests for the "Source Code & Dependencies" copy card.

The card in ``native/templates/_source.py::file_codeblock`` wraps a copy button
(from ``create_copy_button``) in an outer ``div``. The outer ``div`` previously
delegated clicks to the inner button via
``document.getElementById('<btn_id>').click()``. Because ``HTMLElement.click()``
dispatches a real, bubbling ``MouseEvent``, a click on the copy button would
bubble up to the card, which re-fired ``.click()`` on the button, leading to a
double copy (and, in runtimes that process events synchronously, unbounded
recursion).

These tests pin the contract of the fix so the same footgun is not reintroduced:

* the card ``div`` runs the clipboard copy script *directly* (no ``.click()``
  delegation),
* the inner copy button keeps its own ``on_click`` copy handler with
  ``stopPropagation`` so a click on the button does not double-fire the card,
* the other consumers of ``create_copy_button`` (``_demo``, ``_dashboard``)
  stay intact.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import reflex as rx  # pyrefly: ignore

from native.templates._copy_btn import create_copy_button
from native.templates._dashboard import dashboard_demo
from native.templates._demo import demo
from native.templates._source import file_codeblock

if TYPE_CHECKING:
    from collections.abc import Iterator

# ---------------------------------------------------------------------------
# Introspection helpers
# ---------------------------------------------------------------------------


def _event_triggers(comp: object) -> dict[str, object]:
    return getattr(comp, "event_triggers", {}) or {}


def _on_click_chain(comp: object) -> object | None:
    return _event_triggers(comp).get("on_click")


def _first_spec(chain: object) -> object | None:
    events = getattr(chain, "events", None)
    if not events:
        return None
    return events[0]


def _string_value(value: object) -> str | None:
    """Coerce a Reflex ``Var``/literal into its raw Python string."""
    if isinstance(value, str):
        return value
    raw = getattr(value, "_var_value", None)
    return raw if isinstance(raw, str) else None


def on_click_js(comp: object) -> str | None:
    """JavaScript emitted for ``comp``'s ``on_click`` (``call_script`` handlers)."""
    chain = _on_click_chain(comp)
    if chain is None:
        return None
    for key, val in getattr(_first_spec(chain), "args", ()) or ():
        if getattr(key, "_js_expr", None) == "javascript_code":
            return _string_value(val)
    return None


def has_on_click(comp: object) -> bool:
    return _on_click_chain(comp) is not None


def stops_propagation(comp: object) -> bool:
    spec = _first_spec(_on_click_chain(comp))
    return bool(
        spec is not None and getattr(spec, "event_actions", {}).get("stopPropagation"),
    )


def walk(comp: object) -> Iterator[object]:
    yield comp
    for child in getattr(comp, "children", None) or []:
        yield from walk(child)


def is_copy_handler(js: str | None) -> bool:
    return js is not None and "navigator.clipboard.writeText" in js


def is_click_delegation(js: str | None) -> bool:
    """True when a handler delegates via ``element.click()`` (the bug)."""
    return js is not None and ".click(" in js


def find_copy_buttons(root: object) -> list[object]:
    """Copy buttons: carry the clipboard copy script AND stop propagation."""
    return [
        c
        for c in walk(root)
        if has_on_click(c) and is_copy_handler(on_click_js(c)) and stops_propagation(c)
    ]


# ---------------------------------------------------------------------------
# file_codeblock -- the bug fix
# ---------------------------------------------------------------------------


def test_file_codeblock_card_does_not_delegate_via_click() -> None:
    """The recursion/double-fire root: the card's on_click must NOT call `.click()`."""
    card = file_codeblock("components/ui/button.py", "print(1)")

    js = on_click_js(card)
    assert js is not None
    assert not is_click_delegation(js), (
        f"card on_click must not delegate via .click(); got: {js!r}"
    )


def test_file_codeblock_card_copies_directly() -> None:
    """Clicking anywhere on the card must copy (click-anywhere preserved)."""
    card = file_codeblock("components/ui/button.py", "print(1)")

    assert is_copy_handler(on_click_js(card))


def test_file_codeblock_nested_button_stops_propagation() -> None:
    """A button click must not bubble up and double-fire the card handler."""
    card = file_codeblock("components/ui/button.py", "print(1)")
    button = card.children[0].children[1]

    assert stops_propagation(button)


# ---------------------------------------------------------------------------
# create_copy_button
# ---------------------------------------------------------------------------


def test_copy_button_handler_stops_propagation() -> None:
    button, _ = create_copy_button(content="x")

    assert stops_propagation(button), (
        "the copy button must stop propagation so a click on it does not "
        "bubble up and re-trigger an ancestor card handler"
    )


def test_copy_script_safely_escapes_content() -> None:
    """The copied content is embedded via ``json.dumps`` so quotes, newlines,
    backticks and ``${...}`` are safely escaped — never injected as raw JS.
    """
    import json

    payload = 'he said "hi"\nimport os # evil'

    _, copy_script = create_copy_button(content=payload)

    assert json.dumps(payload) in copy_script
    assert payload not in copy_script  # raw, unescaped payload must not appear


# ---------------------------------------------------------------------------
# Regression: the other create_copy_button consumers stay healthy
# ---------------------------------------------------------------------------


def test_demo_builds_and_copy_button_is_intact() -> None:
    component = rx.el.div("preview")
    root = demo(component, "print('demo')")

    copy_buttons = find_copy_buttons(root)
    assert len(copy_buttons) == 1
    assert is_copy_handler(on_click_js(copy_buttons[0]))
    assert stops_propagation(copy_buttons[0])

    # No handler anywhere in the demo tree delegates via .click()
    assert [c for c in walk(root) if is_click_delegation(on_click_js(c))] == []


def test_dashboard_demo_builds_and_copy_button_is_intact() -> None:
    component = rx.el.div("preview")
    root = dashboard_demo(component, "print('dash')")

    copy_buttons = find_copy_buttons(root)
    assert len(copy_buttons) == 1
    assert is_copy_handler(on_click_js(copy_buttons[0]))
    assert stops_propagation(copy_buttons[0])

    assert [c for c in walk(root) if is_click_delegation(on_click_js(c))] == []
