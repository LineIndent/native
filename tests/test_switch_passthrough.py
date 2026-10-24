"""Regression tests for ``switch.root``'s documented input peer pass-through.

``switch.root`` renders a hidden native ``<input type="checkbox">`` wrapped in a
clickable ``<label>``. The documented API contract
(``docs/components/switch.md``) promises that "Any other attribute accepted by a
standard HTML ``<input type="checkbox">`` (``required``, ``value``, etc.) will
pass straight through to the inner input control peer."

The forwarding is implemented with the prefix-based pattern mirrored from the
sibling ``components/ui/checkbox.py``: ``KNOWN_INPUT_PROPS`` plus any
``on_`` / ``data-`` / ``data_`` / ``aria-`` / ``aria_`` prop is routed to the
inner input peer; everything else stays on the wrapping ``<label>``.

These tests guard the future of that contract — that the props documented as
pass-through really do reach the input (and not the label), that the switch-level
props (``size``, ``data-slot``, ``class_name``, ``invalid``) stay on the label,
and that the invalid-state track CSS keeps reading from the input peer.
"""

from __future__ import annotations

import importlib

import pytest
import reflex as rx

from components.ui.switch import ClassNames, switch

_ABSENT = object()


def _input_peer(comp: object) -> object:
    """Return the inner ``<input type="checkbox">`` peer built by ``switch.root``.

    The component is constructed as ``rx.el.label(input, div, span/fragment)`` so
    the input is always the first child. It is identified defensively by peer
    semantics (a ``checked`` field) so a future reordering would surface as a
    clear failure instead of a silently wrong assertion target.
    """
    children = getattr(comp, "children", []) or []
    for child in children:
        if hasattr(child, "checked"):
            return child
    raise AssertionError(
        f"no input peer found in switch.root children: "
        f"{[type(c).__name__ for c in children]}",
    )


def _label_custom_attrs(comp: object) -> dict[str, object]:
    return dict(getattr(comp, "custom_attrs", {}) or {})


def _input_custom_attrs(comp: object) -> dict[str, object]:
    return dict(getattr(_input_peer(comp), "custom_attrs", {}) or {})


def _input_event_triggers(comp: object) -> dict[str, object]:
    return dict(getattr(_input_peer(comp), "event_triggers", {}) or {})


def _label_event_triggers(comp: object) -> dict[str, object]:
    return dict(getattr(comp, "event_triggers", {}) or {})


def _label_style(comp: object) -> dict[str, object]:
    return dict(getattr(comp, "style", {}) or {})


def _field_set(obj: object, name: str) -> bool:
    """True iff ``obj`` carries a non-None ``name`` field (never bool-converts a Var)."""
    v = getattr(obj, name, _ABSENT)
    return v is not _ABSENT and v is not None


def _label_field_unset(comp: object, name: str) -> bool:
    v = getattr(comp, name, _ABSENT)
    return v is _ABSENT or v is None


KNOWN_INPUT_PROPS_CASES = [
    "id",
    "checked",
    "default_checked",
    "disabled",
    "required",
    "name",
    "value",
    "auto_focus",
    "read_only",
    "tab_index",
    "access_key",
    "form",
    "form_action",
    "form_enc_type",
    "form_method",
    "form_no_validate",
    "form_target",
]


@pytest.mark.parametrize(
    "prop",
    KNOWN_INPUT_PROPS_CASES,
    ids=KNOWN_INPUT_PROPS_CASES,
)  # pyright: ignore[reportUntypedFunctionDecorator]
def test_known_input_props_route_to_input_peer_not_label(prop: str) -> None:
    """Every ``KNOWN_INPUT_PROPS`` entry must reach the inner ``<input>`` peer and
    not be absorbed by the wrapping ``<label>``. Guards against the whitelist
    regressing back to an incomplete fixed set (the original bug)."""
    if prop == "on_change":
        value = rx.console_log("change")
    elif prop in {"id", "name", "access_key", "form", "value"}:
        value = "x"
    elif prop.startswith("form_") and prop != "form_no_validate":
        value = "v"
    elif prop == "form_no_validate":
        value = True
    elif prop == "tab_index":
        value = 0
    else:
        value = True
    comp = switch.root("L", **{prop: value})
    assert _field_set(_input_peer(comp), prop), (
        f"input peer did not receive {prop!r}={value!r}"
    )
    assert _label_field_unset(comp, prop), (
        f"prop {prop!r} leaked onto the <label> "
        f"(label_{prop}={getattr(comp, prop, _ABSENT)!r})"
    )


def test_known_input_props_class_is_complete_per_docs() -> None:
    """``ClassNames.KNOWN_INPUT_PROPS`` must include at least the props the docs
    explicitly cite plus the input attributes the bug report found missing, so
    the pass-through sentence (`required`, `value`, etc.) stays honored."""
    required_subset = {
        "id",
        "checked",
        "default_checked",
        "disabled",
        "required",
        "name",
        "value",
        "on_change",
        "auto_focus",
        "read_only",
        "tab_index",
        "access_key",
        "form",
        "custom_attrs",
    }
    missing = required_subset - set(ClassNames.KNOWN_INPUT_PROPS)
    assert not missing, f"KNOWN_INPUT_PROPS is missing: {sorted(missing)}"


EVENT_TRIGGER_CASES = ["on_change", "on_focus", "on_blur", "on_key_down", "on_key_up"]


@pytest.mark.parametrize(
    "event",
    EVENT_TRIGGER_CASES,
    ids=EVENT_TRIGGER_CASES,
)  # pyright: ignore[reportUntypedFunctionDecorator]
def test_input_event_triggers_forward_to_input_without_crash(event: str) -> None:
    """Every ``on_*`` event the inner ``rx.el.input`` accepts must forward to the
    input peer instead of crashing. ``on_key_down`` previously raised
    ``ValueError: The Label does not take in an `on_key_down` event trigger`` because
    the prop was spread onto the wrapping ``<label>``. Guards the prefix-based
    event forwarding (``on_*`` → input)."""
    comp = switch.root("L", **{event: rx.console_log(f"{event}-fired")})
    assert event in _input_event_triggers(comp), (
        f"{event!r} not forwarded to input peer event_triggers"
    )
    assert event not in _label_event_triggers(comp), (
        f"{event!r} leaked onto the <label> event_triggers — would crash before fix"
    )


ARIA_DATA_CASES = [
    ("aria_invalid", "true", "aria-invalid"),
    ("aria-labelledby", "lbl-1", "aria-labelledby"),
    ("aria-describedby", "desc-1", "aria-describedby"),
    ("aria_required", "true", "aria-required"),
    ("data_foo", "bar", "data-foo"),
    ("data-testid", "switch-x", "data-testid"),
]


@pytest.mark.parametrize(
    ("kwarg", "value", "attr"),
    ARIA_DATA_CASES,
    ids=[c[0] for c in ARIA_DATA_CASES],
)  # pyright: ignore[reportUntypedFunctionDecorator]
def test_aria_and_data_attrs_route_to_input_custom_attrs(
    kwarg: str,
    value: object,
    attr: str,
) -> None:
    """``aria-*`` and ``data-*`` attributes (snake_case kwargs) must land on the
    inner input peer's ``custom_attrs`` (real DOM attributes on the ``<input>``),
    not the wrapping ``<label>``'s. Misrouting accessibility attributes away from
    the form control was a silent failure mode of the original whitelist bug."""
    comp = switch.root("L", **{kwarg: value})
    assert _input_custom_attrs(comp).get(attr) == value, (
        f"expected input custom_attrs[{attr!r}]={value!r}, "
        f"got {_input_custom_attrs(comp).get(attr)!r}"
    )
    assert attr not in _label_custom_attrs(comp), (
        f"{attr!r} leaked onto the <label> custom_attrs={_label_custom_attrs(comp)}"
    )


def test_invalid_prop_routes_aria_invalid_to_input_peer() -> None:
    """The switch-level ``invalid=True`` convenience prop sets
    ``aria-invalid="true"`` on the inner input control peer (the standard ARIA
    location), not the wrapping ``<label>``; and ``invalid=False`` (the
    default) synthesizes no ``aria-invalid`` on either element. Guards against
    the convenience prop regressing back onto the label, which would silently
    break the track's ``peer-aria-[invalid=true]:`` styling."""
    invalid_comp = switch.root("L", invalid=True)
    assert _input_custom_attrs(invalid_comp).get("aria-invalid") == "true"
    assert "aria-invalid" not in _label_custom_attrs(invalid_comp)

    default_comp = switch.root("L")
    assert "aria-invalid" not in _input_custom_attrs(default_comp)
    assert "aria-invalid" not in _label_custom_attrs(default_comp)


def test_input_peer_is_first_child_and_is_checkbox() -> None:
    """The input peer must remain the first child of the label, typed as
    ``checkbox`` with the ``peer sr-only`` class — this is what the track's
    ``peer-focus-visible`` / ``peer-aria-[invalid=true]`` /
    ``group-has-[input:checked]`` selectors key off of. A reordering would
    silently break all peer-based styling."""
    comp = switch.root("L", id="x1")
    children = getattr(comp, "children", []) or []
    peer = _input_peer(comp)
    assert peer is children[0], "input peer is not the first child of the label"
    inner = getattr(getattr(peer, "type", None), "_var_value", _ABSENT)
    assert inner == "checkbox", f"input peer is not type=checkbox: {inner!r}"
    assert "peer sr-only" in str(getattr(peer, "class_name", ""))


def test_switch_level_props_stay_on_label() -> None:
    """The switch-level props ``size`` (variant), ``data-slot``, and
    ``class_name`` must stay on the wrapping ``<label>`` (the ``group/switch``
    element) and must NOT be forwarded to the input peer. Accidentally forwarding
    them would lose the ROOT class, the ``data-size`` track sizing selectors, and
    the public data-slot slot."""
    comp = switch.root("hello", size="sm", class_name="extra-class")
    label_attrs = _label_custom_attrs(comp)
    assert label_attrs.get("data-size") == "sm"
    assert label_attrs.get("data-slot") == "switch"
    label_class = str(getattr(comp, "class_name", ""))
    assert "group/switch" in label_class
    assert "extra-class" in label_class
    input_attrs = _input_custom_attrs(comp)
    assert input_attrs.get("data-size") is None
    assert "data-slot" not in input_attrs
    peer_class = str(getattr(_input_peer(comp), "class_name", ""))
    assert "peer sr-only" in peer_class
    assert "group/switch" not in peer_class


def test_track_class_invalid_state_and_dependency_selectors() -> None:
    """The invalid-state track styling must read from the input peer via the
    ``peer-`` combinator (since ``aria-invalid`` lives on the input), and the
    stale ``group-aria-[invalid=true]/switch:`` selector must NOT be present
    (it would no longer match). The size/checked/disabled/focus selectors that
    read from the ``group/switch`` element or the input peer must be preserved
    (no regression in unrelated styling)."""
    track = ClassNames.TRACK
    assert "peer-aria-[invalid=true]:border-destructive" in track
    assert "peer-aria-[invalid=true]:ring-3" in track
    assert "peer-aria-[invalid=true]:ring-destructive/20" in track
    assert "group-aria-[invalid=true]/switch" not in track, (
        "stale group-form invalid selector left in TRACK class"
    )
    assert "group-data-[size=default]/switch:h-[18.4px]" in track
    assert "group-data-[size=sm]/switch:w-[24px]" in track
    assert "group-has-[input:checked]/switch:bg-primary" in track
    assert "peer-focus-visible:ring-3" in track
    assert "peer-focus-visible:ring-ring/50" in track
    assert "group-has-[:disabled]/switch:opacity-50" in track
    assert "group-has-[:disabled]/switch:pointer-events-none" in track
    assert "group-has-[:disabled]/switch:cursor-not-allowed" in track


DEMO_MODULES = [
    ("native.lib.components.switch_basic", "switch_basic"),
    ("native.lib.components.switch_with_label", "switch_with_label"),
    ("native.lib.components.switch_sizes", "switch_sizes"),
    ("native.lib.components.switch_invalid", "switch_invalid"),
    ("native.lib.components.switch_disabled", "switch_disabled"),
]


@pytest.mark.parametrize(
    ("module_path", "fn_name"),
    DEMO_MODULES,
    ids=[m[1] for m in DEMO_MODULES],
)  # pyright: ignore[reportUntypedFunctionDecorator]
def test_in_repo_demos_build(module_path: str, fn_name: str) -> None:
    """Every shipped switch demo must still construct cleanly after the
    forwarding rework. The ``switch_invalid`` demo in particular passes
    ``aria_invalid="true"`` (a non-whitelisted prop under the old code) and
    must not regress now that the prop routes to the input peer."""
    mod = importlib.import_module(module_path)
    comp = getattr(mod, fn_name)()
    assert isinstance(comp, rx.Component), (
        f"{fn_name} did not return an rx.Component: {type(comp).__name__}"
    )


def test_no_unknown_input_props_swallowed_into_label_css() -> None:
    """A broad combination of documented-but-previously-missing input props must
    all reach the input peer, and the label ``style`` (emotion ``css``) dict must
    remain empty. The original bug silently swallowed ``auto_focus`` /
    ``read_only`` into the label's emotion ``css`` object under camelCased
    ``autoFocus`` / ``readOnly`` keys with no DOM attribute at all; this
    replicates the exact rendering scenario from the bug report."""
    comp = switch.root(
        "L",
        auto_focus=True,
        read_only=True,
        tab_index=0,
        form="f1",
        access_key="k",
        on_focus=rx.console_log("f"),
        on_blur=rx.console_log("b"),
        on_key_down=rx.console_log("kd"),
        aria_invalid="true",
        data_foo="bar",
    )
    assert _label_style(comp) == {}, (
        f"label style must be empty; got {_label_style(comp)}"
    )
    peer = _input_peer(comp)
    assert _field_set(peer, "auto_focus")
    assert _field_set(peer, "read_only")
    assert _field_set(peer, "tab_index")
    assert _field_set(peer, "form")
    assert _field_set(peer, "access_key")
    for event in ("on_focus", "on_blur", "on_key_down"):
        assert event in _input_event_triggers(comp)
    assert "on_focus" not in _label_event_triggers(comp)
    assert "on_blur" not in _label_event_triggers(comp)
    assert "on_key_down" not in _label_event_triggers(comp)
    assert _input_custom_attrs(comp).get("aria-invalid") == "true"
    assert _input_custom_attrs(comp).get("data-foo") == "bar"
    assert "aria-invalid" not in _label_custom_attrs(comp)
    assert "data-foo" not in _label_custom_attrs(comp)
