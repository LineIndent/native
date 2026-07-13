---
title: "Avatar"
description: "An image element with a fallback for representing the user."
order: 1
---


## Avatar, An Easily Stylable Avatar Component That Displays A User'S Profile Picture, Initials, Or Fallback Icon.


```python
from components.ui.avatar import Avatar
```

```python
from typing import Any

from reflex.components.component import Component
from reflex.utils.imports import ImportVar
from reflex.vars import FunctionVar, Var
from reflex.vars.base import VarData

PACKAGE_CN = "clsx-for-tailwind@1.0.0"
CN = Var(
    "cn",
    _var_data=VarData(
        imports={
            PACKAGE_CN: ImportVar(tag="cn"),
        },
    ),
).to(FunctionVar)


class CoreComponent(Component):
    unstyled: Var[bool]

    @classmethod
    def set_class_name(
        cls, default_class_name: str | Var[str], props: dict[str, Any]
    ) -> None:

        if "render_" in props:
            return

        props_class_name = props.get("class_name", "")

        if props.pop("unstyled", False):
            props["class_name"] = props_class_name
            return

        props["class_name"] = cn(default_class_name, props_class_name)

    def _exclude_props(self) -> list[str]:
        return [
            *super()._exclude_props(),
            "unstyled",
        ]


def cn(*classes: Var | str | tuple | list | None) -> Var:
    return CN.call(*classes).to(str)
```

```python
import uuid

import reflex as rx
from reflex.components.component import ComponentNamespace
from reflex_components_core.el import Div, Span

from ..core.core import CoreComponent, cn


class ClassNames:
    ROOT = (
        "group/avatar relative flex size-8 shrink-0 rounded-full select-none "
        "after:absolute after:inset-0 after:rounded-full after:border after:border-border "
        "after:mix-blend-darken data-[size=xl]:size-14 data-[size=lg]:size-10 "
        "data-[size=sm]:size-6 dark:after:mix-blend-lighten"
    )
    IMAGE = "aspect-square size-full rounded-full object-cover"
    FALLBACK = (
        "flex size-full items-center justify-center rounded-full bg-muted text-sm "
        "text-muted-foreground group-data-[size=sm]/avatar:text-xs"
    )
    BADGE = (
        "absolute right-0 bottom-0 z-10 inline-flex items-center justify-center "
        "rounded-full bg-primary text-primary-foreground bg-blend-color "
        "ring-2 ring-background select-none "
        "group-data-[size=sm]/avatar:size-2 group-data-[size=sm]/avatar:[&>svg]:hidden "
        "group-data-[size=default]/avatar:size-2.5 group-data-[size=default]/avatar:[&>svg]:size-2 "
        "group-data-[size=lg]/avatar:size-3 group-data-[size=lg]/avatar:[&>svg]:size-2"
    )
    GROUP = (
        "group/avatar-group flex -space-x-2 "
        "*:data-[slot=avatar]:ring-2 *:data-[slot=avatar]:ring-background"
    )
    GROUP_COUNT = (
        "relative flex size-8 shrink-0 items-center justify-center rounded-full "
        "bg-muted text-sm text-muted-foreground ring-2 ring-background "
        "group-has-data-[size=lg]/avatar-group:size-10 "
        "group-has-data-[size=sm]/avatar-group:size-6 "
        "[&>svg]:size-4 group-has-data-[size=lg]/avatar-group:[&>svg]:size-5 "
        "group-has-data-[size=sm]/avatar-group:[&>svg]:size-3"
    )


class AvatarRoot(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        custom_classes = props.pop("class_name", "")
        size = props.pop("size", "default")
        props["data-slot"] = "avatar"
        props["data-size"] = size
        return super().create(
            *children, class_name=cn(ClassNames.ROOT, custom_classes), **props
        )


class AvatarImage(CoreComponent):
    """
    Renders an <img> and probes its `src` client-side on mount. If the image
    fails to load, it hides itself and reveals the sibling AvatarFallback
    (matched via the nearest ancestor with data-slot="avatar").

    Note: if this is rendered inside rx.foreach, the auto-generated uuid will
    be baked in once at template-build time and shared across all rendered
    items. In that case pass an explicit `id` derived from your loop data,
    e.g. id=f"avatar-img-{user.id}".
    """

    @classmethod
    def create(cls, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-image"

        img_id = props.get("id") or f"avatar-img-{uuid.uuid4().hex[:8]}"
        props["id"] = img_id

        src = props.get("src", "")

        js = f"""
        (function() {{
            var img = document.getElementById('{img_id}');
            if (!img) return;
            var root = img.closest('[data-slot="avatar"]');
            var fallback = root ? root.querySelector('[data-slot="avatar-fallback"]') : null;
            var tester = new Image();
            tester.onload = function() {{
                img.style.display = '';
                if (fallback) fallback.style.display = 'none';
            }};
            tester.onerror = function() {{
                img.style.display = 'none';
                if (fallback) fallback.style.display = 'flex';
            }};
            tester.src = '{src}';
        }})()
        """

        props["on_mount"] = rx.call_script(js)

        cls.set_class_name(cn(ClassNames.IMAGE, custom_classes), props)
        return rx.el.img(**props)


class AvatarFallback(Span, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Span:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-fallback"
        props["style"] = {"display": "none", **props.get("style", {})}
        return super().create(
            *children, class_name=cn(ClassNames.FALLBACK, custom_classes), **props
        )


class AvatarBadge(Span, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Span:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-badge"
        return super().create(
            *children, class_name=cn(ClassNames.BADGE, custom_classes), **props
        )


class AvatarGroup(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-group"
        return super().create(
            *children, class_name=cn(ClassNames.GROUP, custom_classes), **props
        )


class AvatarGroupCount(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-group-count"
        return super().create(
            *children, class_name=cn(ClassNames.GROUP_COUNT, custom_classes), **props
        )


class Avatar(ComponentNamespace):
    root = staticmethod(AvatarRoot.create)
    image = staticmethod(AvatarImage.create)
    fallback = staticmethod(AvatarFallback.create)
    badge = staticmethod(AvatarBadge.create)
    group = staticmethod(AvatarGroup.create)
    group_count = staticmethod(AvatarGroupCount.create)
    class_names = ClassNames


avatar = Avatar()
```

# Examples

## Basic

A basic avatar component with an image and a fallback.

```python
def avatar_basic() -> rx.Component:
    fallback_id = "avatar-basic-fallback"

    return avatar.root(
        avatar.image(
            src="https://github.com/LineIndent.png",
            fallback_id=fallback_id,
            custom_attrs={"alt": "@lineindent"},
        ),
        avatar.fallback(
            "AH",
            fallback_id=fallback_id,
        ),
    )
```

## Badge

Use the `avatar.badge` component to add a badge to the avatar. The badge is positioned at the bottom right of the avatar.

```python
def avatar_with_badge() -> rx.Component:
    fallback_id = "avatar-badge-fallback"

    return avatar.root(
        avatar.image(
            src="https://avatars.githubusercontent.com/u/84860195?v=4",
            fallback_id=fallback_id,
            custom_attrs={"alt": "@LineIndent"},
        ),
        avatar.fallback(
            "AH",
            fallback_id=fallback_id,
        ),
        avatar.badge(
            class_name="bg-green-600 dark:bg-green-800",
        ),
    )
```

Use the `class_name` prop to add custom styles to the badge such as custom colors, sizes, etc.

```python
avatar.badge(class_name="bg-green-600 dark:bg-green-800")
```

## Badge with Icon

You can also use an icon inside `avatar.badge`.

```python
def avatar_badge_icon() -> rx.Component:
    fallback_id = "avatar-badge-icon-fallback"

    return avatar.root(
        avatar.image(
            src="https://avatars.githubusercontent.com/u/104714959?s=200&v=4",
            fallback_id=fallback_id,
            custom_attrs={"alt": "Reflex Dev"},
        ),
        avatar.fallback(
            "RD",
            fallback_id=fallback_id,
        ),
        avatar.badge(
            hi("PlusSignIcon"),
        ),
    )
```

## Avatar Group

Use the `avatar.group` component to add a group of avatars.

```python
def avatar_as_group() -> rx.Component:

    return avatar.group(
        avatar.root(
            avatar.image(
                src="/avatars/01.png",
                custom_attrs={"alt": "@avatar-1"},
            ),
            avatar.fallback("RD"),
        ),
        avatar.root(
            avatar.image(
                src="/avatars/02.png",
                custom_attrs={"alt": "@avatar-2"},
            ),
            avatar.fallback("LI"),
        ),
        avatar.root(
            avatar.image(
                src="/avatars/10.png",
                custom_attrs={"alt": "@avatar-10"},
            ),
            avatar.fallback("AH"),
        ),
        class_name="grayscale",
    )
```

## Avatar Group Count

Use `avatar.group_count` to add a count to the group.

```python
def avatar_with_group_count() -> rx.Component:
    return avatar.group(
        avatar.root(
            avatar.image(
                src="/avatars/10.png",
                alt="@avatar-10",
            ),
            avatar.fallback("AH"),
        ),
        avatar.root(
            avatar.image(
                src="/avatars/01.png",
                alt="@avatar-1",
            ),
            avatar.fallback("RD"),
        ),
        avatar.root(
            avatar.image(
                src="/avatars/02.png",
                alt="@avatar-2",
            ),
            avatar.fallback("LI"),
        ),
        avatar.group_count("+3"),
        class_name="grayscale",
    )
```

## Avatar Group with Icon

You can also use an icon inside `avatar.group_count`.

```python
def avatar_group_count_icon() -> rx.Component:
    return avatar.group(
        avatar.root(
            avatar.image(
                src="https://doesnotexist.com",
                alt="@none-dev",
            ),
            avatar.fallback("AH"),
        ),
        avatar.root(
            avatar.image(
                src="https://avatars.githubusercontent.com/u/104714959?s=200&v=4",
                alt="@reflex-dev",
            ),
            avatar.fallback("CN"),
        ),
        avatar.root(
            avatar.image(
                src="https://avatars.githubusercontent.com/u/84860195?v=4",
                alt="LineIndent",
            ),
            avatar.fallback("LI"),
        ),
        avatar.group_count(
            hi("PlusSignIcon"),
        ),
        class_name="grayscale",
    )
```

## Sizes

Use the `size` prop to change the size of the avatar.

```python
def avatar_sizes() -> rx.Component:
    return rx.el.div(
        avatar.root(
            avatar.image(
                src="https://avatars.githubusercontent.com/u/84860195?v=4",
                alt="@LineIndent",
            ),
            avatar.fallback("LI"),
            size="sm",
        ),
        avatar.root(
            avatar.image(
                src="https://avatars.githubusercontent.com/u/84860195?v=4",
                alt="@LineIndent",
            ),
            avatar.fallback("LI"),
        ),
        avatar.root(
            avatar.image(
                src="https://avatars.githubusercontent.com/u/84860195?v=4",
                alt="@LineIndent",
            ),
            avatar.fallback("LI"),
            size="lg",
        ),
        class_name="flex flex-wrap items-center gap-2",
    )
```

## Dropdown

You can use the `Avatar` component as a trigger for a dropdown menu.

```python
def avatar_dropdown_menu() -> rx.Component:
    return menu.root(
        menu.trigger(
            rx.el.img(
                src="https://github.com/LineIndent.png",
                alt="lineindent",
                class_name=avatar.class_names.IMAGE,
            ),
            class_name=avatar.class_names.ROOT,
        ),
        menu.content(
            menu.item("Profile"),
            menu.item("Billing"),
            menu.item("Settings"),
        ),
    )
```

<br>

# API Reference

## avatar.root

The `avatar.root` component is the root component that wraps the avatar image and fallback.

| Prop        | Type                        | Default     |
| ----------- | --------------------------- | ----------- |
| `size`      | `"default" \| "sm" \| "lg"` | `"default"` |
| `class_name` | `string`                    | -           |

## avatar.image

The `avatar.image` component displays the avatar image. It accepts all Base UI Avatar Image props.

| Prop        | Type     | Default |
| ----------- | -------- | ------- |
| `src`       | `string` | -       |
| `alt`       | `string` | -       |
| `class_name` | `string` | -       |

## avatar.fallback

The `avatar.fallback` component displays a fallback when the image fails to load. It accepts all Base UI Avatar Fallback props.

| Prop        | Type     | Default |
| ----------- | -------- | ------- |
| `class_name` | `string` | -       |

## avatar.badge

The `avatar.badge` component displays a badge indicator on the avatar, typically positioned at the bottom right.

| Prop        | Type     | Default |
| ----------- | -------- | ------- |
| `class_name` | `string` | -       |

## avatar.group

The `avatar.group` component displays a group of avatars with overlapping styling.

| Prop        | Type     | Default |
| ----------- | -------- | ------- |
| `class_name` | `string` | -       |

## avatar.group_count

The `avatar.group_count` component displays a count indicator in an avatar group, typically showing the number of additional avatars.

| Prop        | Type     | Default |
| ----------- | -------- | ------- |
| `class_name` | `string` | -       |
