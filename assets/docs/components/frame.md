---
title: "Frame"
description: "Displays related content in a structured frame."
order: 0
---


## Frame, Displays Related Content In A Structured Frame.



> Error processing `usage`: module, class, method, function, traceback, frame, or code object was expected, got Frame


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
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn

LiteralVariant = Literal["default", "inverse", "ghost"]
LiteralSpacing = Literal["xs", "sm", "default", "lg"]


class ClassNames:
    ROOT = "relative flex flex-col bg-muted/50 gap-0.75 p-0.75 rounded-xl"
    ROOT_VARIANT_DEFAULT = "border border-border bg-clip-padding"
    ROOT_VARIANT_INVERSE = "border border-border bg-background bg-clip-padding"
    ROOT_VARIANT_GHOST = ""
    PANEL = "relative grow overflow-hidden rounded-xl border border-border bg-card bg-clip-padding shadow-xs p-(--frame-panel-p)"
    HEADER = "flex flex-col px-(--frame-panel-header-px) py-(--frame-panel-header-py)"
    TITLE = "text-sm font-semibold"
    DESCRIPTION = "text-muted-foreground text-sm"
    FOOTER = (
        "flex flex-col gap-1 px-(--frame-panel-footer-px) py-(--frame-panel-footer-py)"
    )


VARIANT_CLASSES: dict[str, str] = {
    "default": ClassNames.ROOT_VARIANT_DEFAULT,
    "inverse": ClassNames.ROOT_VARIANT_INVERSE,
    "ghost": ClassNames.ROOT_VARIANT_GHOST,
}

SPACING_CLASSES: dict[str, str] = {
    "xs": "[--frame-panel-p:--spacing(2)] [--frame-panel-header-px:--spacing(2)] [--frame-panel-header-py:--spacing(1)] [--frame-panel-footer-px:--spacing(2)] [--frame-panel-footer-py:--spacing(1)]",
    "sm": "[--frame-panel-p:--spacing(3)] [--frame-panel-header-px:--spacing(3)] [--frame-panel-header-py:--spacing(2)] [--frame-panel-footer-px:--spacing(3)] [--frame-panel-footer-py:--spacing(2)]",
    "default": "[--frame-panel-p:--spacing(4)] [--frame-panel-header-px:--spacing(4)] [--frame-panel-header-py:--spacing(3)] [--frame-panel-footer-px:--spacing(4)] [--frame-panel-footer-py:--spacing(3)]",
    "lg": "[--frame-panel-p:--spacing(5)] [--frame-panel-header-px:--spacing(5)] [--frame-panel-header-py:--spacing(4)] [--frame-panel-footer-px:--spacing(5)] [--frame-panel-footer-py:--spacing(4)]",
}


class FrameRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        variant: LiteralVariant = props.pop("variant", "default")
        spacing: LiteralSpacing = props.pop("spacing", "default")
        stacked: bool = props.pop("stacked", False)
        dense: bool = props.pop("dense", False)
        class_name: str = props.pop("class_name", "")

        stacked_class = (
            "gap-0 *:has-[+[data-slot=frame-panel]]:rounded-b-none *:[[data-slot=frame-panel]+[data-slot=frame-panel]]:rounded-t-none *:[[data-slot=frame-panel]+[data-slot=frame-panel]]:border-t-0"
            if stacked
            else ""
        )

        dense_class = (
            "p-0 gap-0 [&_[data-slot=frame-panel]]:-mx-px [&_[data-slot=frame-panel]]:before:hidden [&_[data-slot=frame-panel]:last-child]:-mb-px"
            if dense
            else ""
        )

        props["data-slot"] = "frame"
        props["data-spacing"] = spacing

        return rx.el.div(
            *children,
            class_name=cn(
                ClassNames.ROOT,
                VARIANT_CLASSES.get(variant, ""),
                SPACING_CLASSES.get(spacing, ""),
                stacked_class,
                dense_class,
                class_name,
            ),
            **props,
        )


class FramePanel(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel"
        return rx.el.div(
            *children,
            class_name=cn(ClassNames.PANEL, class_name),
            **props,
        )


class FrameHeader(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel-header"
        return rx.el.header(
            *children,
            class_name=cn(ClassNames.HEADER, class_name),
            **props,
        )


class FrameTitle(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel-title"
        return rx.el.div(
            *children,
            class_name=cn(ClassNames.TITLE, class_name),
            **props,
        )


class FrameDescription(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel-description"
        return rx.el.div(
            *children,
            class_name=cn(ClassNames.DESCRIPTION, class_name),
            **props,
        )


class FrameFooter(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel-footer"
        return rx.el.footer(
            *children,
            class_name=cn(ClassNames.FOOTER, class_name),
            **props,
        )


class Frame(ComponentNamespace):
    root = staticmethod(FrameRoot.create)
    panel = staticmethod(FramePanel.create)
    header = staticmethod(FrameHeader.create)
    title = staticmethod(FrameTitle.create)
    description = staticmethod(FrameDescription.create)
    footer = staticmethod(FrameFooter.create)
    __call__ = staticmethod(FrameRoot.create)
    class_names = ClassNames


frame = Frame()
```

# Examples

## Basic Panels

A basic frame with a header and two panels.

**Props used:** none required beyond default `frame.root` composition.

```python
def frame_basic():
    return frame.root(
        frame.header(
            frame.title("Section header"),
            frame.description("Description for the section"),
        ),
        frame.panel(
            rx.el.h2("Separated Panel", class_name="text-sm font-semibold"),
            rx.el.p("Section description", class_name="text-muted-foreground text-sm"),
        ),
        frame.panel(
            rx.el.h2("Separated Panel", class_name="text-sm font-semibold"),
            rx.el.p("Section description", class_name="text-muted-foreground text-sm"),
        ),
        class_name="w-full max-w-md",
    )
```

## Stacked Panels

Set `stacked=True` to merge panel borders into one continuous block.

**Props used:** `stacked` on `frame.root`.

```python
def frame_stacked():
    return frame.root(
        frame.header(
            frame.title("Section header"),
            frame.description("Description for the section"),
        ),
        frame.panel(
            rx.el.h2("Separated Panel", class_name="text-sm font-semibold"),
            rx.el.p("Section description", class_name="text-muted-foreground text-sm"),
        ),
        frame.panel(
            rx.el.h2("Separated Panel", class_name="text-sm font-semibold"),
            rx.el.p("Section description", class_name="text-muted-foreground text-sm"),
        ),
        stacked=True,
        class_name="w-full max-w-md",
    )
```

## Dense Panels

Set `dense=True` for minimal frame padding, edge-to-edge.

**Props used:** `dense` on `frame.root`.

```python
def frame_dense():
    return frame.root(
        frame.header(
            frame.title("Section header"),
            frame.description("Description for the section"),
        ),
        frame.panel(
            rx.el.h2("Separated Panel", class_name="text-sm font-semibold"),
            rx.el.p("Section description", class_name="text-muted-foreground text-sm"),
        ),
        frame.panel(
            rx.el.h2("Separated Panel", class_name="text-sm font-semibold"),
            rx.el.p("Section description", class_name="text-muted-foreground text-sm"),
        ),
        stacked=True,
        dense=True,
        class_name="w-full max-w-md",
    )
```

## Outer Border

Set `variant="ghost"` to remove the frame's outer border.

**Props used:** `variant` on `frame.root`.

```python
def frame_no_border():
    return frame.root(
        frame.header(
            frame.title("No Outer Border"),
            frame.description(
                "This frame uses variant='ghost' to remove the outer border."
            ),
        ),
        frame.panel(
            rx.el.p(
                "The outer container of this frame has no border, only the background and panels are visible.",
                class_name="text-muted-foreground text-sm",
            ),
        ),
        stacked=True,
        dense=True,
        variant="ghost",
        class_name="w-full max-w-md",
    )
```

# API Reference

## frame.root

```python
frame.root(
    frame.panel(
        frame.header(frame.title("Overview")),
        "Panel content",
    ),
    variant="default",
    spacing="default",
)
```

| Prop         | Type                                          | Default     | Description                                                                          |
| ------------ | ----------------------------------------------- | ----------- | -------------------------------------------------------------------------------------- |
| `variant`    | `Literal["default", "inverse", "ghost"]`       | `"default"` | Controls the visual style of the frame container.                                     |
| `spacing`    | `Literal["xs", "sm", "default", "lg"]`         | `"default"` | Controls internal padding of panels, headers, and footers via CSS variables.          |
| `stacked`    | `bool`                                          | `False`     | Removes gaps and merges panel borders so they appear as one continuous block.         |
| `dense`      | `bool`                                          | `False`     | Removes all padding/gaps and pulls panels edge-to-edge with negative margins.          |
| `class_name` | `str`                                            | `""`         | Additional classes merged onto the root wrapper.                                       |

## frame.panel

```python
frame.panel("Panel content")
```

| Prop         | Type  | Default | Description                                                          |
| ------------ | ----- | ------- | ------------------------------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the panel — overrides default bg/border/padding. |

## frame.header

```python
frame.header(frame.title("Overview"))
```

| Prop         | Type  | Default | Description                                    |
| ------------ | ----- | ------- | ----------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the header.       |

## frame.title

```python
frame.title("Overview")
```

| Prop         | Type  | Default | Description                                   |
| ------------ | ----- | ------- | ----------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the title.        |

## frame.description

```python
frame.description("A summary of recent activity.")
```

| Prop         | Type  | Default | Description                                        |
| ------------ | ----- | ------- | ----------------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the description.        |

## frame.footer

```python
frame.footer(button("View all", variant="ghost", size="sm"))
```

| Prop         | Type  | Default | Description                                    |
| ------------ | ----- | ------- | ----------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the footer.        |
