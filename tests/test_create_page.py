"""Regression tests for the /create page layout.

Guards against the mobile-unreachable bug where the entire customizer
sidebar rendered with ``hidden lg:flex`` (``display: none`` below the
Tailwind ``lg`` breakpoint, 1024px) while the *only* element that could
toggle the source-code panel (``#copy-theme-button`` flipping
``data-show`` on ``#toggle-wrapper``) lived inside that hidden aside.

Below ``lg`` the result was a read-only card preview with every
customizer control (Style/Base/Color/Chart/Radius/Font selects, Get
Code, Shuffle, Open Preset, Reset) and the source-code panel
permanently unreachable. The fix mirrors the responsive pattern used
by the sibling ``/typeset`` page (commit e3a5428): the sidebar renders
on mobile (no ``hidden lg:flex``), selects reflow into a horizontal
scroll strip, and the toggle-reveal pair (``group-data-[show=true]``
on ``#source-space`` plus ``max-lg:group-data-[show=true]:hidden`` on
the preview) lets mobile users switch between preview and code.

These tests assert the class-string contract statically (no browser
required) so the regression cannot silently return.
"""

from typing import Any

from native.pages.create import (
    _sidebar_desktop,  # pyright: ignore[reportPrivateUsage]
    create_page,
    preview_space,
    source_space,
)

_CLASS_DELIMS = str.maketrans({'"': " ", "(": " ", ")": " ", ",": " "})


def _is_component(node: Any) -> bool:
    return hasattr(node, "children") and hasattr(node, "class_name")


def _find_by_id(root: Any, target_id: str) -> Any:
    """Depth-first search for a Reflex component whose ``id`` equals ``target_id``."""
    if _is_component(root):
        cid = root.id if hasattr(root, "id") else None
        if isinstance(cid, str) and cid == target_id:
            return root
        children = root.children if hasattr(root, "children") else None
        if isinstance(children, list):
            for child in children:
                found = _find_by_id(child, target_id)
                if found is not None:
                    return found
    return None


def _class_str(component: Any) -> str:
    cls = component.class_name
    return cls if isinstance(cls, str) else str(cls)


def _tokens(cls: str) -> set[str]:
    return set(cls.translate(_CLASS_DELIMS).split())


def test_sidebar_is_visible_on_mobile_not_hidden_below_lg() -> None:
    """The customizer aside must render on mobile; ``hidden lg:flex`` made
    every sidebar control (including the source-panel toggle) unreachable
    below 1024px.
    """
    aside = _sidebar_desktop()
    tokens = _tokens(_class_str(aside))

    assert "hidden" not in tokens, (
        "the sidebar must not be display:none at base breakpoint; every "
        "customizer control and the Get Code toggle live inside it"
    )
    assert "lg:flex" not in tokens or "flex" in tokens, (
        "the aside must be visible at base breakpoint (flex), not gated "
        "behind lg:flex alone"
    )
    assert "flex" in tokens, "the aside must use flex at base breakpoint"


def test_toggle_button_is_reachable_outside_a_hidden_container() -> None:
    """``#copy-theme-button`` is the only toggler of ``data-show`` on
    ``#toggle-wrapper``; it must live in a sidebar that renders on mobile.
    """
    page = create_page()

    toggle = _find_by_id(page, "copy-theme-button")
    assert toggle is not None, "copy-theme-button toggle must exist"

    aside = _sidebar_desktop()
    aside_tokens = _tokens(_class_str(aside))
    assert "hidden" not in aside_tokens, (
        "the toggle lives inside the sidebar; the sidebar must not be "
        "hidden at base breakpoint or the toggle is unreachable on mobile"
    )

    wrapper = _find_by_id(page, "toggle-wrapper")
    assert wrapper is not None, "toggle-wrapper must exist"
    custom_attrs = getattr(wrapper, "custom_attrs", {}) or {}
    assert custom_attrs.get("data-show") == "false", (
        "toggle-wrapper must start with data-show=false so the source "
        "panel is hidden until toggled"
    )


def test_toggle_flips_data_show_on_toggle_wrapper() -> None:
    """The toggle's on_click must mutate ``data-show`` on
    ``#toggle-wrapper`` so the source panel can be revealed on mobile.
    """
    toggle = _find_by_id(create_page(), "copy-theme-button")
    assert toggle is not None
    triggers = getattr(toggle, "event_triggers", {}) or {}
    on_click = triggers.get("on_click")
    assert on_click is not None, "toggle must have an on_click handler"
    script_src = str(on_click)
    assert "toggle-wrapper" in script_src, "the toggle must target #toggle-wrapper"
    assert "dataset.show" in script_src, (
        "the toggle must flip data-show to reveal/hide the source panel"
    )


def test_source_panel_is_revealable_on_mobile() -> None:
    """``#source-space`` must become visible on mobile when
    ``data-show`` is flipped to true; previously the panel was
    ``hidden group-data-[show=true]:flex`` but the only toggler was
    hidden on mobile, so the panel could never appear.
    """
    cls = source_space().class_name
    assert isinstance(cls, str)
    tokens = _tokens(cls)

    assert "hidden" in tokens, "base visibility must be hidden (default)"
    assert "group-data-[show=true]:flex" in tokens, (
        "mobile reveal rule must trigger when #toggle-wrapper[data-show=true]"
    )
    assert "max-lg:group-data-[show=true]:flex-1" in tokens, (
        "source panel must fill available height on mobile when revealed"
    )
    assert "max-lg:group-data-[show=true]:min-h-0" in tokens, (
        "source panel must be allowed to shrink within flex on mobile"
    )


def test_preview_hides_on_mobile_when_source_shown() -> None:
    """On mobile the preview must step aside when the source panel is
    shown so the two don't compete for the small viewport; mirroring
    ``/typeset``'s ``max-lg:group-data-[show=true]:hidden`` on the preview.
    """
    page = create_page()

    wrapper = _find_by_id(page, "toggle-wrapper")
    assert wrapper is not None, "toggle-wrapper must exist"
    assert "group" in _tokens(_class_str(wrapper)), (
        "toggle-wrapper must carry the ``group`` class so its "
        "data-show state drives group-data-[show=true] descendants"
    )

    preview_tokens = _tokens(_class_str(preview_space()))
    assert "max-lg:group-data-[show=true]:hidden" in preview_tokens, (
        "preview must be hidden on mobile when #toggle-wrapper[data-show=true] "
        "so it steps aside for the source panel"
    )


def test_create_and_typeset_share_mobile_reachability_contract() -> None:
    """Quick parity check: both customizer pages must render their
    sidebars on mobile (no ``hidden lg:flex``) and expose a source panel
    that is revealable via a reachable toggle.
    """
    from native.pages.typeset import (
        _sidebar_desktop as typeset_sidebar,  # pyright: ignore[reportPrivateUsage]
    )

    create_tokens = _tokens(_class_str(_sidebar_desktop()))
    typeset_tokens = _tokens(_class_str(typeset_sidebar()))

    assert "hidden" not in create_tokens, "create sidebar must render on mobile"
    assert "hidden" not in typeset_tokens, "typeset sidebar must render on mobile"
