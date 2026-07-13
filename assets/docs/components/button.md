---
title: "Button"
description: "Displays a button or a component that looks like a button."
order: 3
---


## Button, Displays A Button Or A Component That Looks Like A Button.


```python
from components.ui.button import button
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
from reflex_components_core.el import Button as BaseButton

from ..core.core import CoreComponent, cn

LiteralButtonVariant = Literal[
    "default",
    "destructive",
    "outline",
    "secondary",
    "ghost",
    "link",
]
LiteralButtonSize = Literal[
    "default",
    "xs",
    "sm",
    "lg",
    "icon",
    "icon-xs",
    "icon-sm",
    "icon-lg",
]

DEFAULT_CLASS_NAME = (
    "group/button inline-flex shrink-0 items-center justify-center "
    "rounded-lg border border-transparent bg-clip-padding "
    "text-sm font-medium whitespace-nowrap outline-none select-none "
    "focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 "
    "active:not-aria-[haspopup]:translate-y-px "
    "disabled:pointer-events-none disabled:opacity-50 "
    "aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 "
    "dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40 "
    "[&_svg]:pointer-events-none [&_svg]:shrink-0 "
    "[&_svg:not([class*='size-'])]:size-4"
)

BUTTON_VARIANTS = {
    "variant": {
        "default": ("bg-primary text-primary-foreground hover:bg-primary/80"),
        "outline": (
            "border-border bg-background hover:bg-muted hover:text-foreground "
            "aria-expanded:bg-muted aria-expanded:text-foreground "
            "dark:border-input dark:bg-input/30 dark:hover:bg-input/50"
        ),
        "secondary": (
            "bg-secondary text-secondary-foreground "
            "hover:bg-[color-mix(in_oklch,var(--secondary),var(--foreground)_5%)] "
            "aria-expanded:bg-secondary aria-expanded:text-secondary-foreground"
        ),
        "ghost": (
            "hover:bg-muted hover:text-foreground "
            "aria-expanded:bg-muted aria-expanded:text-foreground "
            "dark:hover:bg-muted/50"
        ),
        "destructive": (
            "bg-destructive/10 text-destructive hover:bg-destructive/20 "
            "focus-visible:border-destructive/40 focus-visible:ring-destructive/20 "
            "dark:bg-destructive/20 dark:hover:bg-destructive/30 "
            "dark:focus-visible:ring-destructive/40"
        ),
        "link": "text-primary underline-offset-4 hover:underline",
    },
    "size": {
        "default": (
            "h-8 gap-1.5 px-2.5 "
            "has-data-[icon=inline-end]:pr-2 "
            "has-data-[icon=inline-start]:pl-2"
        ),
        "xs": (
            "h-6 gap-1 rounded-[min(var(--radius-md),10px)] px-2 text-xs "
            "in-data-[slot=button-group]:rounded-lg "
            "has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 "
            "[&_svg:not([class*='size-'])]:size-3"
        ),
        "sm": (
            "h-7 gap-1 rounded-[min(var(--radius-md),12px)] px-2.5 text-[0.8rem] "
            "in-data-[slot=button-group]:rounded-lg "
            "has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 "
            "[&_svg:not([class*='size-'])]:size-3.5"
        ),
        "lg": (
            "h-9 gap-1.5 px-2.5 "
            "has-data-[icon=inline-end]:pr-2 "
            "has-data-[icon=inline-start]:pl-2"
        ),
        "icon": "size-8",
        "icon-xs": (
            "size-6 rounded-[min(var(--radius-md),10px)] "
            "in-data-[slot=button-group]:rounded-lg "
            "[&_svg:not([class*='size-'])]:size-3"
        ),
        "icon-sm": (
            "size-7 rounded-[min(var(--radius-md),12px)] "
            "in-data-[slot=button-group]:rounded-lg"
        ),
        "icon-lg": "size-9",
    },
}


class Button(BaseButton, CoreComponent):
    variant: Var[LiteralButtonVariant]
    size: Var[LiteralButtonSize]

    @classmethod
    def create(cls, *children, **props) -> BaseButton:
        variant = props.pop("variant", "default")
        size = props.pop("size", "default")
        custom_classes = props.pop("class_name", "")
        data_slot = props.pop("data_slot", "button")

        return super().create(
            *children,
            data_slot=data_slot,
            class_name=cn(
                DEFAULT_CLASS_NAME,
                BUTTON_VARIANTS["variant"].get(variant, ""),
                BUTTON_VARIANTS["size"].get(size, ""),
                custom_classes,
            ),
            **props,
        )

    def _exclude_props(self) -> list[str]:
        return [*super()._exclude_props(), "size", "variant"]


def button_variants(variant: str = "default", size: str = "default") -> Var:
    return cn(
        DEFAULT_CLASS_NAME,
        BUTTON_VARIANTS["variant"].get(variant, ""),
        BUTTON_VARIANTS["size"].get(size, ""),
    )


button = Button.create
```

# Examples

## Sizes

Use the `size` prop to change the button's size.

**Props used:** `size` on `button`.

```python
def button_size() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            button("Extra Small", size="xs", variant="outline"),
            button(
                hi("ArrowUpRight03Icon"),
                size="icon-xs",
                aria_label="Submit",
                variant="outline",
            ),
            class_name="flex items-start gap-2",
        ),
        rx.el.div(
            button("Small", size="sm", variant="outline"),
            button(
                hi("ArrowUpRight03Icon"),
                size="icon-sm",
                aria_label="Submit",
                variant="outline",
            ),
            class_name="flex items-start gap-2",
        ),
        rx.el.div(
            button("Default", variant="outline"),
            button(
                hi("ArrowUpRight03Icon"),
                size="icon",
                aria_label="Submit",
                variant="outline",
            ),
            class_name="flex items-start gap-2",
        ),
        rx.el.div(
            button("Large", variant="outline", size="lg"),
            button(
                hi("ArrowUpRight03Icon"),
                size="icon-lg",
                aria_label="Submit",
                variant="outline",
            ),
            class_name="flex items-start gap-2",
        ),
        class_name="flex flex-col items-start gap-8 sm:flex-row",
    )
```

## Default

**Props used:** none required — `variant="default"` is the default.

```python
def button_default():
    return button("Button")
```

## Secondary

**Props used:** `variant` on `button`.

```python
def button_secondary():
    return button("Secondary", variant="secondary")
```

## Outline

**Props used:** `variant` on `button`.

```python
def button_outline():
    return button("Outline", variant="outline")
```

## Ghost

**Props used:** `variant` on `button`.

```python
def button_ghost():
    return button("Ghost", variant="ghost")
```

## Link

**Props used:** `variant` on `button`.

```python
def button_link():
    return button("Link", variant="link")
```

## Destructive

**Props used:** `variant` on `button`.

```python
def button_destructive():
    return button("Destructive", variant="destructive")
```

## Icon

**Props used:** `size="icon"` on `button`.

```python
def button_icon():
    return button(
        hi("CircleArrowUp01Icon", class_name="size-4"),
        variant="outline",
        size="icon",
    )
```

## With Icon

Add `data-icon="inline-start"` or `data-icon="inline-end"` to the icon child for correct spacing.

**Props used:** `data_icon` on the icon child.

```python
def button_with_icon() -> rx.Component:
    return rx.el.div(
        button(
            hi("GitBranchIcon", custom_attrs={"data-icon": "inline-start"}),
            "New Branch",
            variant="outline",
        ),
        button(
            "Fork",
            hi("GitForkIcon", custom_attrs={"data-icon": "inline-end"}),
            variant="outline",
        ),
        class_name="flex gap-2",
    )
```

## Rounded

**Props used:** `class_name="rounded-full"` on `button`.

```python
def button_rounded() -> rx.Component:
    return rx.el.div(
        button(
            "Get Started",
            class_name="rounded-full",
        ),
        button(
            hi("ArrowUp02Icon"),
            variant="outline",
            size="icon",
            class_name="rounded-full",
        ),
        class_name="flex gap-2",
    )
```

## Spinner

Render a `spinner()` inside the button for a loading state, with the same `data-icon` positioning convention as icons.

**Props used:** `data_icon` on the spinner child.

```python
def button_loading() -> rx.Component:
    return rx.el.div(
        button(
            spinner(custom_attrs={"data-icon": "inline-start"}),
            "Generating",
            variant="outline",
        ),
        button(
            "Downloading",
            spinner(custom_attrs={"data-icon": "inline-end"}),
            variant="secondary",
            disabled=True,
        ),
        class_name="flex gap-2",
    )
```

## As Link

Use `button_variants(...)` to generate the button's classes as a plain `Var`, applied to a real `rx.el.a`. Don't wrap an `<a>` inside `button(...)` — the underlying Base UI `Button` always sets `role="button"`, which overrides the link's semantic role.

**Props used:** `variant`, `size` args on `button_variants(...)`.

```python
def button_render() -> rx.Component:
    return rx.el.a(
        "Login",
        href="#",
        class_name=button_variants(variant="secondary", size="sm"),
    )
```

# API Reference

## button

```python
button("Click me", variant="outline", size="sm")
```

| Prop      | Type                                                                                      | Default     |
| --------- | ------------------------------------------------------------------------------------------ | ----------- |
| `variant` | `Literal["default", "destructive", "outline", "secondary", "ghost", "link"]`              | `"default"` |
| `size`    | `Literal["default", "xs", "sm", "lg", "icon", "icon-xs", "icon-sm", "icon-lg"]`            | `"default"` |
| `class_name` | `str`                                                                                    | `""`        |

Any other prop accepted by the underlying Base UI `Button` is also passed straight through.

## button_variants

Returns the same classes `button(...)` would apply, as a plain `Var[str]` — for styling a non-button element (like a link) to look like a button, without wrapping it in an actual `<button>`.

```python
rx.el.a(
    "Go to docs",
    href="/docs",
    class_name=button_variants("outline", "sm"),
)
```

| Arg       | Type                                                                            | Default     |
| --------- | --------------------------------------------------------------------------------- | ----------- |
| `variant` | `Literal["default", "destructive", "outline", "secondary", "ghost", "link"]`     | `"default"` |
| `size`    | `Literal["default", "xs", "sm", "lg", "icon", "icon-xs", "icon-sm", "icon-lg"]`   | `"default"` |
