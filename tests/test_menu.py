"""Regression tests for ``MenuContent`` side/align class composition.

``MenuContent`` (``components/ui/menu.py``) positions its floating panel by
merging a side-positioning class (``top-full`` / ``bottom-full`` /
``left-full`` / ``right-full``) with an align class through ``cn()``, which
emits a JavaScript ``twMerge(clsx(...))`` call. ``tailwind-merge`` resolves
conflicting Tailwind utilities by keeping the *last* class in the same
conflict group (so ``left-full`` is dropped by a later ``left-0``, etc.),
silently — the merged class list is what the browser renders.

For ``side="left"``/``"right"`` the side class lives in the ``right``/``left``
inset group, so the align class must come from the orthogonal (vertical) axis
(``top-*``/``bottom-*``); for ``side="top"``/``"bottom"`` the side class lives in
the ``top``/``bottom`` group, so the align class must come from the horizontal
axis (``left-*``/``right-*``). Otherwise the side class is dropped by the align
class (overlap) or both axes are set (over-constraint), and the menu overlaps
its trigger.

Because ``cn(...)`` is a runtime JS ``FunctionVar`` that cannot be evaluated at
Python test time, these tests assert on the emitted ``class_name._js_expr``
string — the same Var-inspection pattern used by ``tests/test_tabs.py`` and
``tests/test_source_codeblock.py``.
"""

from __future__ import annotations

import re

import pytest

from components.ui.menu import ClassNames, MenuContent

# tailwind-merge conflict groups for the inset utilities we emit. Side and
# align classes must come from different groups, otherwise twMerge silently
# drops the side class.
_HORIZONTAL_INSET_GROUPS = [
    {"left-0", "left-1/2", "left-full"},
    {"right-0", "right-1/2", "right-full"},
]
_VERTICAL_INSET_GROUPS = [
    {"top-0", "top-1/2", "top-full"},
    {"bottom-0", "bottom-1/2", "bottom-full"},
]

# Expected positional tokens per documented side and align combination.
EXPECTED_POSITION_CLASS = {
    "bottom": "top-full",
    "top": "bottom-full",
    "left": "right-full",
    "right": "left-full",
}
EXPECTED_ALIGN_CLASS = {
    ("bottom", "start"): "left-0",
    ("bottom", "center"): "left-1/2 -translate-x-1/2",
    ("bottom", "end"): "right-0",
    ("top", "start"): "left-0",
    ("top", "center"): "left-1/2 -translate-x-1/2",
    ("top", "end"): "right-0",
    ("left", "start"): "top-0",
    ("left", "center"): "top-1/2 -translate-y-1/2",
    ("left", "end"): "bottom-0",
    ("right", "start"): "top-0",
    ("right", "center"): "top-1/2 -translate-y-1/2",
    ("right", "end"): "bottom-0",
}

SIDES = ["bottom", "top", "left", "right"]
ALIGNS = ["start", "center", "end"]


def _extract_cn_args(js: str) -> tuple[str, str, str]:
    """Pull (CONTENT, position_class, align_class) out of the inner ``cn(...)``
    call emitted for ``MenuContent``.

    The emitted shape is ``cn((cn(CONTENT, position, align)), "")``; this reads
    the inner call.
    """
    pattern = re.compile(
        r'cn\(\s*("(?:[^"\\]|\\.)*"\s*,\s*)'
        r'"(?P<position>[^"]*)"\s*,\s*'
        r'"(?P<align>[^"]*)"\s*\)',
    )
    match = pattern.search(js)
    assert match is not None, f"could not parse inner cn(...) call from: {js}"
    content_match = re.search(r'"(absolute z-50[^"]*)"', js)
    content = content_match.group(1) if content_match else ClassNames.CONTENT
    return content, match.group("position"), match.group("align")


def _group_of(token: str) -> str | None:
    """Return the tailwind-merge conflict group name a single utility belongs to.

    For multi-token align strings (``"top-1/2 -translate-y-1/2"``) only the
    inset token matters for conflict resolution; ``-translate-*`` is in its
    own group and never conflicts with the side class.
    """
    inset = token.split(maxsplit=1)[0] if token else token
    for name, groups in (
        ("left", _HORIZONTAL_INSET_GROUPS[:1]),
        ("right", _HORIZONTAL_INSET_GROUPS[1:2]),
        ("top", _VERTICAL_INSET_GROUPS[:1]),
        ("bottom", _VERTICAL_INSET_GROUPS[1:2]),
    ):
        for group in groups:
            if inset in group:
                return name
    return None


@pytest.mark.parametrize(
    ("side", "align"),
    [(s, a) for s in SIDES for a in ALIGNS],
    ids=[f"{s}-{a}" for s in SIDES for a in ALIGNS],
)  # pyright: ignore[reportUntypedFunctionDecorator]
def test_menu_content_position_and_align_classes(side: str, align: str) -> None:
    """For each documented side and align combination, the emitted class_name
    must carry exactly the expected side-positioning class and the expected
    per-side align class, and the two classes must be in different
    tailwind-merge conflict groups. If they shared a group, ``cn()``/``twMerge``
    would silently drop the side class and the menu would overlap its
    trigger — the original bug."""
    component = MenuContent.create("body", side=side, align=align)
    js = getattr(component.class_name, "_js_expr", None)
    assert isinstance(js, str), (
        f"expected class_name._js_expr to be str, got {type(js)!r}"
    )
    content, position, align_cls = _extract_cn_args(js)
    assert content == ClassNames.CONTENT, (
        f"side={side} align={align}: base CONTENT class drifted to {content!r}"
    )
    assert position == EXPECTED_POSITION_CLASS[side], (
        f"side={side}: expected position {EXPECTED_POSITION_CLASS[side]!r}, "
        f"got {position!r}"
    )
    assert align_cls == EXPECTED_ALIGN_CLASS[(side, align)], (
        f"side={side} align={align}: expected align "
        f"{EXPECTED_ALIGN_CLASS[(side, align)]!r}, got {align_cls!r}"
    )
    pos_group = _group_of(position)
    align_group = _group_of(align_cls)
    assert pos_group is not None, f"position {position!r} not in any known group"
    assert align_group is not None, f"align {align_cls!r} not in any known group"
    assert pos_group != align_group, (
        f"side={side} align={align}: position {position!r} and align "
        f"{align_cls!r} share tailwind-merge group {pos_group!r}; "
        "cn()/twMerge would drop one and the menu would overlap its trigger"
    )


def test_menu_content_defaults_match_documented_api() -> None:
    """With no side/align props, ``MenuContent`` must default to
    ``side="bottom"``, ``align="start"`` — the documented defaults and the
    configuration used by ``native/templates/navbar.py``. The emitted
    class_name must contain ``top-full`` (side class) and ``left-0`` (align
    class). Non-regression for the navbar and the four menu demos, all of
    which use the defaults."""
    component = MenuContent.create("body")
    js = getattr(component.class_name, "_js_expr", None)
    assert isinstance(js, str), (
        f"expected class_name._js_expr to be str, got {type(js)!r}"
    )
    content, position, align = _extract_cn_args(js)
    assert content == ClassNames.CONTENT
    assert position == "top-full"
    assert align == "left-0"
