"""Regression tests for ``input_group``'s addon focus-management handler.

``InputGroupAddon.add_custom_code`` injects an ``onclick`` handler that moves
focus to the group's form control when a non-button region of the addon is
clicked. The handler originally located the control with
``querySelector('input')`` — a CSS *type* selector that matches only ``<input>``
elements and returns ``null`` for a ``<textarea>``, so the focus redirect was
silently no-op'd for ``input_group.textarea`` groups.

The fix selects the shared ``data-slot="input-group-control"`` attribute that
both ``InputGroupInput`` and ``InputGroupTextarea`` emit. These tests guard
the two ways that regression could be reintroduced: reverting the handler to a
bare tag selector, or dropping the shared ``data-slot`` from one of the two
control factories.
"""

from __future__ import annotations

import pytest

from components.ui.input_group import InputGroupAddon, input_group

CONTROL_SLOT = "input-group-control"


def _focus_script() -> str:
    """Return the JS string injected by ``InputGroupAddon.add_custom_code``.

    ``InputGroupAddon.create`` is used (rather than direct instantiation)
    because Reflex logs a warning when components are instantiated directly.
    """
    scripts = InputGroupAddon.create().add_custom_code()
    assert isinstance(scripts, list) and len(scripts) == 1, (
        f"expected one custom-code script, got {len(scripts)}"
    )
    return scripts[0]


def test_addon_focus_handler_targets_shared_control_slot():
    """The click handler must select the shared ``input-group-control`` slot
    rather than a hard-coded tag name, so it matches both ``<input>`` and
    ``<textarea>`` controls. A bare ``querySelector('input')`` type selector
    must not return — it never matches a ``<textarea>``."""
    script = _focus_script()
    assert f'[data-slot="{CONTROL_SLOT}"]' in script
    assert "querySelector('input')" not in script


@pytest.mark.parametrize(
    "factory",
    [input_group.input, input_group.textarea],
    ids=["input", "textarea"],
)  # pyright: ignore[reportUntypedFunctionDecorator]
def test_control_carries_shared_data_slot(factory):
    """Both ``input_group.input`` and ``input_group.textarea`` must render a
    control carrying ``data-slot="input-group-control"`` in its DOM attributes.
    The focus handler's selector keys off this slot, so dropping it (or
    diverging the value) from either factory would silently break focus
    management for that control type."""
    component = factory()
    custom_attrs = getattr(component, "custom_attrs", None)
    assert isinstance(custom_attrs, dict), (
        f"{factory.__name__} component has no custom_attrs dict"
    )
    assert custom_attrs.get("data-slot") == CONTROL_SLOT, (
        f"{factory.__name__} expected data-slot={CONTROL_SLOT!r}, "
        f"got {custom_attrs.get('data-slot')!r}"
    )
