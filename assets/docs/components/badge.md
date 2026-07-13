---
title: "Badge"
description: "Displays a badge or a component that looks like a badge."
order: 2
---


## Badge, Displays A Badge Or A Component That Looks Like A Badge.


```python
from components.ui.badge import badge
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
from typing import Literal

from reflex.vars.base import Var
from reflex_components_core.el import Span

from ..core.core import CoreComponent, cn

LiteralBadgeVariant = Literal[
    "default", "secondary", "destructive", "outline", "ghost", "link"
]

DEFAULT_BASE_CLASSES = (
    "group/badge inline-flex h-5 w-fit shrink-0 items-center justify-center gap-1 overflow-hidden "
    "rounded-4xl border border-transparent px-2 py-0.5 text-xs font-medium whitespace-nowrap "
    "transition-all focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 "
    "has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 aria-invalid:border-destructive "
    "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 [&>svg]:pointer-events-none [&>svg]:size-3!"
)

BADGE_VARIANTS = {
    "default": "bg-primary text-primary-foreground [a]:hover:bg-primary/80",
    "secondary": "bg-secondary text-secondary-foreground [a]:hover:bg-secondary/80",
    "destructive": (
        "bg-destructive/10 text-destructive focus-visible:ring-destructive/20 "
        "dark:bg-destructive/20 dark:focus-visible:ring-destructive/40 [a]:hover:bg-destructive/20"
    ),
    "outline": "border-border text-foreground [a]:hover:bg-muted [a]:hover:text-muted-foreground",
    "ghost": "hover:bg-muted hover:text-muted-foreground dark:hover:bg-muted/50",
    "link": "text-primary underline-offset-4 hover:underline",
}


def badge_variants(variant: str = "default") -> Var:
    return cn(
        DEFAULT_BASE_CLASSES,
        BADGE_VARIANTS.get(variant, BADGE_VARIANTS["default"]),
    )


class Badge(Span, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Span:
        custom_classes = props.pop("class_name", "")
        variant = props.pop("variant", "default")
        props["data-slot"] = "badge"
        props["data-variant"] = variant

        return super().create(
            *children,
            class_name=cn(badge_variants(variant), custom_classes),
            **props,
        )


badge = Badge.create
```

# Examples

## Variants

Use the `variant` prop to change the badge's style.

**Props used:** `variant` on `badge`.

```python
def badge_with_variants() -> rx.Component:
    return rx.el.div(
        badge("Default"),
        badge("Secondary", variant="secondary"),
        badge("Destructive", variant="destructive"),
        badge("Outline", variant="outline"),
        badge("Ghost", variant="ghost"),
        class_name="flex flex-wrap gap-2",
    )
```

## With Icons

Render an icon inside the badge. Add `data-icon="inline-start"` or `data-icon="inline-end"` to the icon to position it correctly (adjusts padding automatically).

**Props used:** `data_icon` on the icon child.

```python
def badge_with_icon() -> rx.Component:
    return rx.el.div(
        badge(
            hi("CheckmarkBadge01Icon", custom_attrs={"data-icon": "inline-start"}),
            "Verified",
            variant="secondary",
        ),
        badge(
            "Bookmark",
            hi("Bookmark02Icon", custom_attrs={"data-icon": "inline-end"}),
            variant="outline",
        ),
        class_name="flex flex-wrap gap-2",
    )
```

## With Spinner

Render a `spinner` inside the badge — same `data-icon` positioning convention as icons.

**Props used:** `data_icon` on the spinner child.

```python
def badge_with_spinner() -> rx.Component:
    return rx.el.div(
        badge(
            spinner(custom_attrs={"data-icon": "inline-start"}),
            "Deleting",
            variant="destructive",
        ),
        badge(
            "Generating",
            spinner(custom_attrs={"data-icon": "inline-end"}),
            variant="secondary",
        ),
        class_name="flex flex-wrap gap-2",
    )
```

## Link

Pass `rx.el.a` as the badge's child to turn it into a link. `badge` accepts `*children`, so any interactive element works.

**Props used:** none required — pass `rx.el.a(...)` as a child.

```python
def badge_as_link() -> rx.Component:
    return badge(
        rx.el.a(
            "Open Link",
            hi("ArrowUpRightIcon", custom_attrs={"data-icon": "inline-end"}),
            href="#link",
            class_name="inline-flex items-center gap-1 text-inherit no-underline",
        ),
    )
```

## Custom Colors

Override colors by passing extra classes via `class_name`.

**Props used:** `class_name` on `badge`.

```python
def badge_custom_colors() -> rx.Component:
    return rx.el.div(
        badge(
            "Blue",
            class_name="bg-blue-50 text-blue-700 dark:bg-blue-950 dark:text-blue-300",
        ),
        badge(
            "Green",
            class_name="bg-green-50 text-green-700 dark:bg-green-950 dark:text-green-300",
        ),
        badge(
            "Sky",
            class_name="bg-sky-50 text-sky-700 dark:bg-sky-950 dark:text-sky-300",
        ),
        badge(
            "Purple",
            class_name="bg-purple-50 text-purple-700 dark:bg-purple-950 dark:text-purple-300",
        ),
        badge(
            "Red",
            class_name="bg-red-50 text-red-700 dark:bg-red-950 dark:text-red-300",
        ),
        class_name="flex flex-wrap gap-2",
    )
```

# API Reference

## badge

```python
badge("New", variant="secondary")
```

| Prop         | Type                                                                                   | Default     |
| ------------ | --------------------------------------------------------------------------------------- | ----------- |
| `variant`    | `Literal["default", "secondary", "destructive", "outline", "ghost", "link"]`           | `"default"` |
| `class_name` | `str`                                                                                    | `""`        |

Any other prop accepted by a native `<span>` is also passed straight through.
