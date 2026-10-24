"""Regression tests for the ``unstyled`` prop across CoreComponent subclasses.

Background: ``CoreComponent`` in ``components/core/core.py`` declares
``unstyled: Var[bool]``. When ``True``, the component should strip its own
default Tailwind classes and render only user-supplied ``class_name``. The
mechanism lives in ``CoreComponent.set_class_name``: any ``create()`` that
routes its ``class_name`` through ``set_class_name`` gets the behavior for
free; ``create()`` methods that build ``class_name`` directly with ``cn(...)``
and pass ``**props`` through to ``super().create(...)`` previously bypassed
``set_class_name`` and silently ignored ``unstyled``.

This file guards against that regression by asserting, for every
``CoreComponent`` whose ``create()`` previously bypassed ``set_class_name``:

  1. By default (``unstyled`` not set) the component's default classes are
     applied alongside any user-supplied ``class_name``.
  2. With ``unstyled=True`` and user ``class_name`` set, the rendered
     ``class_name`` contains ONLY the user-supplied classes; no component
     default class survives.
  3. With ``unstyled=True`` and no user ``class_name``, the component
     renders with an empty/blank ``class_name`` (no defaults leak).
  4. With ``unstyled=True`` no ``unstyled`` attribute leaks into the
     component's rendered custom_attrs (it remains excluded from the DOM).

It also re-runs the same checks against ``NativeSelectOptionComponent`` as a
control case: that component already routed through ``set_class_name`` before
this fix, so its behavior must not regress.

For ``NativeSelectComponent``, which renders both a ``<select>`` element and
a wrapper ``<div>`` from a single ``create()`` call, the same set of
guarantees is checked against BOTH the inner ``<select>`` (using the user's
``class_name``) and the outer wrapper (using ``wrapper_class_name``).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import pytest

from components.ui.avatar import (
    AvatarBadge,
    AvatarFallback,
    AvatarGroup,
    AvatarGroupCount,
    AvatarRoot,
)
from components.ui.badge import BadgeComponent
from components.ui.button import Button
from components.ui.frame import (
    FrameDescription,
    FrameFooter,
    FrameHeader,
    FramePanel,
    FrameRoot,
    FrameTitle,
)
from components.ui.input import InputComponent
from components.ui.select import (
    NativeSelectComponent,
    NativeSelectOptionComponent,
)
from components.ui.tabs import TabsContent, TabsList, TabsRoot

if TYPE_CHECKING:
    import reflex as rx
    from reflex_components_core.el import Div, Span

USER_CLASS = "u-test-class"


def _class_name_str(component: object) -> str:
    cls = getattr(component, "class_name", None)
    return "" if cls is None else str(cls)


def _assert_only_user_classes(component: object, user_class: str = USER_CLASS) -> None:
    rendered = _class_name_str(component)
    assert user_class in rendered, (
        f"Expected user class {user_class!r} in stripped class_name, got {rendered!r}"
    )
    assert "cn(" not in rendered, (
        f"With unstyled=True no default classes should be merged via cn(...); "
        f"got {rendered!r}"
    )


def _assert_defaults_and_user_classes(
    component: object,
    default_marker: str,
    user_class: str = USER_CLASS,
) -> None:
    rendered = _class_name_str(component)
    assert default_marker in rendered, (
        f"Default marker {default_marker!r} must be present in default class_name; "
        f"got {rendered!r}"
    )
    assert user_class in rendered, (
        f"User class {user_class!r} must be present in default class_name; "
        f"got {rendered!r}"
    )
    assert "cn(" in rendered, (
        f"Default class_name should be a cn(...) merge of default + user; "
        f"got {rendered!r}"
    )


def _assert_unstyled_not_rendered(component: object) -> None:
    custom_attrs = getattr(component, "custom_attrs", None) or {}
    assert "unstyled" not in custom_attrs, (
        f"`unstyled` must not leak into rendered custom_attrs; got {custom_attrs!r}"
    )


ComponentFactory = Callable[..., Any]


def _button(**kw: Any) -> rx.Component:
    return Button.create("Click", **kw)


def _tabs_content(**kw: Any) -> Div:
    return TabsContent.create("Body", value="tab", **kw)


def _avatar_fallback(**kw: Any) -> Span:
    return AvatarFallback.create("F", **kw)


def _avatar_badge(**kw: Any) -> Span:
    return AvatarBadge.create("+", **kw)


def _avatar_group_count(**kw: Any) -> Div:
    return AvatarGroupCount.create("+1", **kw)


def _badge(**kw: Any) -> Span:
    return BadgeComponent.create("B", **kw)


def _frame_panel(**kw: Any) -> rx.Component:
    return FramePanel.create("P", **kw)


def _frame_header(**kw: Any) -> rx.Component:
    return FrameHeader.create("H", **kw)


def _frame_title(**kw: Any) -> rx.Component:
    return FrameTitle.create("T", **kw)


def _frame_description(**kw: Any) -> rx.Component:
    return FrameDescription.create("D", **kw)


def _frame_footer(**kw: Any) -> rx.Component:
    return FrameFooter.create("F", **kw)


def _select_option(**kw: Any) -> rx.Component:
    return NativeSelectOptionComponent.create("Option", **kw)


SIMPLE_COMPONENTS: list[tuple[str, str, ComponentFactory]] = [
    ("Button", "bg-primary", _button),
    ("TabsRoot", "group/tabs", TabsRoot.create),
    ("TabsList", "group/tabs-list", TabsList.create),
    ("TabsContent", "flex-1 text-sm outline-none hidden", _tabs_content),
    ("AvatarRoot", "group/avatar", AvatarRoot.create),
    ("AvatarFallback", "bg-muted", _avatar_fallback),
    ("AvatarBadge", "bg-primary", _avatar_badge),
    ("AvatarGroup", "group/avatar-group", AvatarGroup.create),
    ("AvatarGroupCount", "bg-muted", _avatar_group_count),
    ("BadgeComponent", "border-transparent", _badge),
    ("FrameRoot", "rounded-xl", FrameRoot.create),
    ("FramePanel", "rounded-xl", _frame_panel),
    ("FrameHeader", "flex flex-col", _frame_header),
    ("FrameTitle", "text-sm font-semibold", _frame_title),
    ("FrameDescription", "text-muted-foreground", _frame_description),
    ("FrameFooter", "flex flex-col gap-1", _frame_footer),
    ("InputComponent", "rounded-lg", InputComponent.create),
    ("NativeSelectOptionComponent", "bg-[Canvas] text-[CanvasText]", _select_option),
]


@pytest.mark.parametrize(  # pyright: ignore[reportUntypedFunctionDecorator]
    ("name", "default_marker", "factory"),
    SIMPLE_COMPONENTS,
    ids=[row[0] for row in SIMPLE_COMPONENTS],
)
def test_default_class_name_merges_with_user_class(
    name: str,
    default_marker: str,
    factory: ComponentFactory,
) -> None:
    del name
    comp = factory(class_name=USER_CLASS)
    _assert_defaults_and_user_classes(comp, default_marker)


@pytest.mark.parametrize(  # pyright: ignore[reportUntypedFunctionDecorator]
    ("name", "default_marker", "factory"),
    SIMPLE_COMPONENTS,
    ids=[row[0] for row in SIMPLE_COMPONENTS],
)
def test_unstyled_false_matches_default_behavior(
    name: str,
    default_marker: str,
    factory: ComponentFactory,
) -> None:
    del name
    default_comp = factory(class_name=USER_CLASS)
    explicit_false_comp = factory(class_name=USER_CLASS, unstyled=False)
    assert _class_name_str(default_comp) == _class_name_str(explicit_false_comp), (
        "Passing unstyled=False must reproduce the default (unstyled not passed) "
        "class_name so that unstyled=False is not a silent no-op."
    )
    assert default_marker in _class_name_str(explicit_false_comp), (
        f"Default marker {default_marker!r} must remain with explicit unstyled=False"
    )


@pytest.mark.parametrize(  # pyright: ignore[reportUntypedFunctionDecorator]
    ("name", "default_marker", "factory"),
    SIMPLE_COMPONENTS,
    ids=[row[0] for row in SIMPLE_COMPONENTS],
)
def test_unstyled_strips_defaults_keeps_user_classes(
    name: str,
    default_marker: str,
    factory: ComponentFactory,
) -> None:
    del name, default_marker
    comp = factory(class_name=USER_CLASS, unstyled=True)
    _assert_only_user_classes(comp)


@pytest.mark.parametrize(  # pyright: ignore[reportUntypedFunctionDecorator]
    ("name", "default_marker", "factory"),
    SIMPLE_COMPONENTS,
    ids=[row[0] for row in SIMPLE_COMPONENTS],
)
def test_unstyled_without_user_class_is_blank(
    name: str,
    default_marker: str,
    factory: ComponentFactory,
) -> None:
    del name, default_marker
    comp = factory(unstyled=True)
    rendered = _class_name_str(comp)
    assert rendered.strip() == "", (
        f"With unstyled=True and no user class_name, class must be blank; "
        f"got {rendered!r}"
    )


@pytest.mark.parametrize(  # pyright: ignore[reportUntypedFunctionDecorator]
    ("name", "default_marker", "factory"),
    SIMPLE_COMPONENTS,
    ids=[row[0] for row in SIMPLE_COMPONENTS],
)
def test_unstyled_is_not_rendered_into_attrs(
    name: str,
    default_marker: str,
    factory: ComponentFactory,
) -> None:
    del name, default_marker
    comp = factory(unstyled=True)
    _assert_unstyled_not_rendered(comp)


def test_native_select_honors_unstyled_on_select_and_wrapper() -> None:
    user_select = "u-select"
    user_wrapper = "u-wrapper"

    default_sel = NativeSelectComponent.create(
        class_name=user_select,
        wrapper_class_name=user_wrapper,
    )
    unstyled_sel = NativeSelectComponent.create(
        class_name=user_select,
        wrapper_class_name=user_wrapper,
        unstyled=True,
    )

    inner_select_default = default_sel.children[0]
    inner_select_unstyled = unstyled_sel.children[0]

    _assert_defaults_and_user_classes(
        inner_select_default,
        default_marker="appearance-none rounded-lg",
        user_class=user_select,
    )
    rendered_inner_default = _class_name_str(inner_select_default)
    assert user_wrapper not in rendered_inner_default, (
        "wrapper_class_name must not bleed into the inner <select> class_name"
    )

    rendered_inner_uns = _class_name_str(inner_select_unstyled)
    assert "cn(" not in rendered_inner_uns, (
        f"unstyled=True on NativeSelect must not merge defaults into the select "
        f"element; got {rendered_inner_uns!r}"
    )
    assert user_select in rendered_inner_uns, (
        f"User select class {user_select!r} must survive unstyled=True; "
        f"got {rendered_inner_uns!r}"
    )

    _assert_defaults_and_user_classes(
        default_sel,
        default_marker="group/native-select",
        user_class=user_wrapper,
    )
    rendered_wrapper_uns = _class_name_str(unstyled_sel)
    assert "cn(" not in rendered_wrapper_uns, (
        f"unstyled=True on NativeSelect must not merge defaults into the wrapper div; "
        f"got {rendered_wrapper_uns!r}"
    )
    assert user_wrapper in rendered_wrapper_uns, (
        f"User wrapper class {user_wrapper!r} must survive unstyled=True; "
        f"got {rendered_wrapper_uns!r}"
    )

    _assert_unstyled_not_rendered(unstyled_sel)
    _assert_unstyled_not_rendered(inner_select_unstyled)


def test_unstyled_native_select_without_user_classes_renders_blank_select_and_wrapper() -> (
    None
):
    unstyled_sel = NativeSelectComponent.create(unstyled=True)
    inner_select = unstyled_sel.children[0]
    assert _class_name_str(inner_select).strip() == "", (
        f"unstyled=True with no user class_name must yield blank select; "
        f"got {_class_name_str(inner_select)!r}"
    )
    assert _class_name_str(unstyled_sel).strip() == "", (
        f"unstyled=True with no wrapper_class_name must yield blank wrapper; "
        f"got {_class_name_str(unstyled_sel)!r}"
    )


def test_unstyled_native_select_icon_class_is_preserved() -> None:
    unstyled_sel = NativeSelectComponent.create(unstyled=True)
    children = list(unstyled_sel.children)
    icon = next(
        (
            c
            for c in children
            if (getattr(c, "custom_attrs", None) or {}).get("data-slot")
            == "native-select-icon"
        ),
        None,
    )
    assert icon is not None, "NativeSelect wrapper must contain the dropdown icon"
    assert "pointer-events-none" in _class_name_str(icon), (
        "The dropdown icon's hardcoded classes must not be affected by unstyled=True"
    )


def test_native_select_default_behavior_matches_unstyled_false() -> None:
    user_select = "u-select"
    user_wrapper = "u-wrapper"
    default_comp = NativeSelectComponent.create(
        class_name=user_select,
        wrapper_class_name=user_wrapper,
    )
    explicit_false_comp = NativeSelectComponent.create(
        class_name=user_select,
        wrapper_class_name=user_wrapper,
        unstyled=False,
    )
    assert _class_name_str(default_comp.children[0]) == _class_name_str(
        explicit_false_comp.children[0],
    ), "Inner <select> class_name must match between default and unstyled=False"
    assert _class_name_str(default_comp) == _class_name_str(
        explicit_false_comp,
    ), "Wrapper class_name must match between default and unstyled=False"
