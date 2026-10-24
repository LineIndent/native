"""Regression tests for the /typeset page layout.

Guards against the off-by-one breakpoint bug where the "Get Code"
panel (``#source-space``) became unreachable on viewports in the
Tailwind ``lg``-``xl`` band (1024px ≤ width < 1280px): the panel used
``xl:flex`` as its only desktop always-visible override while the
"Get Code/Preview" toggle button was ``lg:hidden``, leaving the
[1024, 1280)px range with neither a visible panel nor a toggle to
reveal it. The fix is to make the panel always visible at ``lg``
(``lg:flex``), matching the breakpoint where the page switches to its
three-column desktop layout (``lg:flex-row``) and where the toggle
disappears (``lg:hidden``).

These tests assert the class-string contract statically (no browser
required) so the regression cannot silently return.
"""

from native.pages.typeset import source_space, typeset_page

_CLASS_DELIMS = str.maketrans({'"': " ", "(": " ", ")": " ", ",": " "})


def _is_component(node) -> bool:
    return hasattr(node, "children") and hasattr(node, "class_name")


def _find_by_id(root, target_id: str):
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


def _class_str(component) -> str:
    cls = component.class_name
    return cls if isinstance(cls, str) else str(cls)


def _tokens(cls: str) -> set[str]:
    return set(cls.translate(_CLASS_DELIMS).split())


def test_source_space_is_always_visible_at_lg_not_xl():
    cls = source_space().class_name
    assert isinstance(cls, str)
    tokens = _tokens(cls)

    assert "hidden" in tokens, "base visibility must be hidden (mobile default)"
    assert "max-lg:group-data-[show=true]:flex" in tokens, (
        "mobile toggle-reveal rule must be preserved"
    )
    assert "lg:flex" in tokens, (
        "desktop always-visible override must activate at lg breakpoint"
    )
    assert "xl:flex" not in tokens, (
        "xl:flex reintroduces the 1024-1279px dead band: the panel would "
        "only reappear at 1280px while the lg:hidden toggle vanishes at 1024px"
    )


def test_typeset_desktop_layout_and_source_panel_share_lg_breakpoint():
    page = typeset_page()

    wrapper = _find_by_id(page, "typeset-toggle-wrapper")
    assert wrapper is not None, "typeset-toggle-wrapper must exist"
    assert "lg:flex-row" in _tokens(_class_str(wrapper)), (
        "the page switches to its three-column desktop layout at lg; the "
        "source column must therefore also be visible at lg"
    )

    toggle = _find_by_id(page, "typeset-code-button")
    assert toggle is not None, "typeset-code-button toggle must exist"
    assert "lg:hidden" in _tokens(_class_str(toggle)), (
        "the 'Get Code/Preview' toggle must be hidden at lg+ since the "
        "panel is always visible there"
    )

    source = _find_by_id(page, "source-space")
    assert source is not None, "source-space panel must exist"
    source_tokens = _tokens(_class_str(source))
    assert "lg:flex" in source_tokens, (
        "source-space must become always-visible at the same lg breakpoint "
        "where the desktop layout starts (lg:flex-row) and the toggle "
        "disappears (lg:hidden)"
    )
    assert "xl:flex" not in source_tokens, (
        "an xl:flex override on source-space is inconsistent with the "
        "lg:flex-row wrapper and lg:hidden toggle and reintroduces the "
        "1024-1279px dead band"
    )
