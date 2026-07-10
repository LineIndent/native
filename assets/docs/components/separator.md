---
title: "Separator"
description: "Visually or semantically separates content."
order: 0
---


## Separator, Visually Or Semantically Separates Content.


```python
from components.ui.separator import separator
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

import reflex as rx

from ..core.core import CoreComponent

LiteralOrientation = Literal["horizontal", "vertical"]


class ClassNames:
    SEPARATOR = (
        "shrink-0 bg-input "
        "data-[orientation=horizontal]:h-px data-[orientation=horizontal]:w-full "
        "data-[orientation=vertical]:w-px data-[orientation=vertical]:self-stretch"
    )


class SeparatorComponent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        orientation: str = props.pop("orientation", "horizontal")
        decorative = props.pop("decorative", True)
        data_slot = props.pop("data_slot", "separator")

        props["data-slot"] = data_slot
        props["data-orientation"] = orientation

        if decorative:
            props["aria-hidden"] = "true"
        else:
            props["role"] = "separator"
            props["aria-orientation"] = orientation

        cls.set_class_name(ClassNames.SEPARATOR, props)
        return rx.el.div(*children, **props)


separator = SeparatorComponent.create
```

# Examples

## Default

The default `orientation` is set to `horizontal`.

```python
def separator_horizontal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div("buridan/ui", class_name="leading-none font-medium"),
            rx.el.div(
                "The UI Library for Reflex Devs.",
                class_name="text-muted-foreground",
            ),
            class_name="flex flex-col gap-1.5",
        ),
        separator(class_name="bg-zinc-200 dark:bg-zinc-800"),
        rx.el.div(
            "A set of beautifully designed components that you can customize, extend, and build on."
        ),
        class_name="flex max-w-sm flex-col gap-4 text-sm",
    )
```

## Vertical 

Use `orientation="vertical"` for a vertical separator.

```python
def separator_vertical() -> rx.Component:
    return rx.el.div(
        rx.el.div("Blog"),
        separator(orientation="vertical"),
        rx.el.div("Docs"),
        separator(orientation="vertical"),
        rx.el.div("Source"),
        class_name="flex h-5 items-center gap-4 text-sm",
    )
```

## Menu

Vertical separators between menu items with descriptions.

```python
def separator_menu() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span("Settings", class_name="font-medium"),
            rx.el.span(
                "Manage preferences", class_name="text-xs text-muted-foreground"
            ),
            class_name="flex flex-col gap-1",
        ),
        separator(orientation="vertical"),
        rx.el.div(
            rx.el.span("Account", class_name="font-medium"),
            rx.el.span(
                "Profile & security", class_name="text-xs text-muted-foreground"
            ),
            class_name="flex flex-col gap-1",
        ),
        separator(orientation="vertical", class_name="hidden md:block"),
        rx.el.div(
            rx.el.span("Help", class_name="font-medium"),
            rx.el.span("Support & docs", class_name="text-xs text-muted-foreground"),
            class_name="hidden flex-col gap-1 md:flex",
        ),
        class_name="flex items-center gap-2 text-sm md:gap-4",
    )
```

## List

Horizontal separators between list items.

```python
def separator_list() -> rx.Component:
    return rx.el.div(
        rx.el.dl(
            rx.el.dt("Item 1"),
            rx.el.dd("Value 1", class_name="text-muted-foreground"),
            class_name="flex items-center justify-between",
        ),
        separator(),
        rx.el.dl(
            rx.el.dt("Item 2"),
            rx.el.dd("Value 2", class_name="text-muted-foreground"),
            class_name="flex items-center justify-between",
        ),
        separator(),
        rx.el.dl(
            rx.el.dt("Item 3"),
            rx.el.dd("Value 3", class_name="text-muted-foreground"),
            class_name="flex items-center justify-between",
        ),
        class_name="flex w-full max-w-sm flex-col gap-2 text-sm",
    )
```
