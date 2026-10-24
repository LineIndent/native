"""Regression tests for ``attachment.group``'s default composition layout.

``attachment.group`` lays out its children as a horizontally scrollable,
snapping row by applying ``*:data-[slot=attachment]:flex-none`` to every
direct ``[data-slot=attachment]`` child. ``flex-none`` makes each child's
used main size come from its ``width`` rather than flex sizing, so the
group's layout depends entirely on the root's resolved width.

The port originally set the attachment root base to ``w-full`` (matching
``width: 100%`` of the scroll container), so every group child resolved
to the full container width and the group rendered one full-width card
per scroll/snap page — instead of the documented compact row of
content-hugging cards. The fix is to use ``w-fit`` (matching upstream
shadcn's ``new-york-v4`` registry) so each child hugs its content while
``flex-none`` keeps it from being shrunk.

These tests assert the class-string contract statically (no browser
required) so the regression cannot silently return. They mirror the
``str``-token ``class_name`` approach used by ``test_typeset_page.py``.
"""

from __future__ import annotations

from typing import Any

from components.ui.attachment import attachment

_CLASS_DELIMS = str.maketrans({'"': " ", "(": " ", ")": " ", ",": " "})


def _class_str(component: Any) -> str:
    cls = component.class_name
    return cls if isinstance(cls, str) else str(cls)


def _tokens(cls: str) -> set[str]:
    return set(cls.translate(_CLASS_DELIMS).split())


def test_root_renders_w_fit_class_via_cn() -> None:
    """The rendered root's ``class_name`` — produced by the
    ``cn(default, size, orientation, overrides)`` chain — must contain
    ``w-fit`` and must not contain a bare ``w-full`` token. ``w-full``
    resolves to ``width: 100%`` of the scroll container, so every
    ``flex-none`` group child becomes a full-page card. ``w-fit``
    resolves to ``width: fit-content``, letting each child hug its
    content while ``max-w-full`` still caps it at the container width.
    """
    root = attachment.root()
    tokens = _tokens(_class_str(root))
    assert "w-fit" in tokens, (
        "the rendered root must carry w-fit so group children hug content"
    )
    assert "w-full" not in tokens, (
        "no bare w-full token may appear on the rendered root — it forces every "
        "flex-none group child to the full container width, producing one "
        "full-width card per snap page (the regression); max-w-full is allowed"
    )
    assert "max-w-full" in tokens, "max-w-full must survive the cn(...) merge"


def test_default_composition_renders_compact_row_payload() -> None:
    """End-to-end default-composition smoke test (no browser): build
    ``attachment.group(attachment.root(...), attachment.root(...), ...)``
    with no per-root overrides and assert the rendered payload (a) has
    a group carrying the snap/flex-none rules and (b) has children each
    carrying ``w-fit`` (so they are NOT full-container-width). This is
    the static contract for the documented 'none required beyond
    default composition' usage.

    Children are passed positionally so the rendered component tree
    exposes them as direct ``group.children`` (passing a list wraps it
    in a Reflex ``Bare`` fragment whose array contents are not walked
    here; the descendant CSS selector applies identically to both).
    """
    child_count = 3
    roots = [
        attachment.root(attachment.content(attachment.title(f"f{i}.pdf")))
        for i in range(child_count)
    ]
    group = attachment.group(*roots)

    group_tokens = _tokens(_class_str(group))
    assert "*:data-[slot=attachment]:flex-none" in group_tokens, (
        "group must keep *:data-[slot=attachment]:flex-none so children hug content "
        "rather than grow to fill the scroll container"
    )
    assert "*:data-[slot=attachment]:snap-start" in group_tokens, (
        "group must keep *:data-[slot=attachment]:snap-start so each child is a snap point"
    )

    attachment_children = [
        child
        for child in (group.children or [])
        if getattr(child, "custom_attrs", {}).get("data-slot") == "attachment"
    ]
    assert len(attachment_children) == child_count, (
        f"group must contain {child_count} attachment roots, "
        f"got {len(attachment_children)}"
    )
    for child in attachment_children:
        child_tokens = _tokens(_class_str(child))
        assert "w-fit" in child_tokens, (
            "every default-composition root must carry w-fit so the group "
            "renders a compact row, not one full-width card per snap page"
        )
        assert "w-full" not in child_tokens, (
            "no default-composition root may carry a bare w-full token"
        )
