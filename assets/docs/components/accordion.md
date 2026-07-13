---
title: "Accordion"
description: "A vertically stacked set of interactive headings that each reveal a section of content."
order: 0
---


## Accordion, A Vertically Stacked Set Of Interactive Headings That Each Reveal A Section Of Content.



> Component `accordion` not found


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
from reflex.components.component import Component
from reflex.utils.imports import ImportVar
from reflex.vars.base import Var, VarData

from ..core.core import CoreComponent

REACT_LIBRARY = "@hugeicons/react@1.1.6"
CORE_ICONS_LIBRARY = "@hugeicons/core-free-icons@4.2.1"


class HugeIcon(CoreComponent):
    library = REACT_LIBRARY

    tag = "HugeiconsIcon"

    icon: Var[str]

    alt_icon: Var[str | None]

    show_alt: Var[bool]

    size: Var[int | str] = Var.create(16)

    color: Var[str]

    primary_color: Var[str]

    secondary_color: Var[str]

    stroke_width: Var[float] = Var.create(1.5)

    absolute_stroke_width: Var[bool]

    disable_secondary_opacity: Var[bool]

    @classmethod
    def create(cls, *children, **props) -> Component:

        if children and isinstance(children[0], str) and "icon" not in props:
            props["icon"] = children[0]
            children = children[1:]

        for prop in ("icon", "alt_icon"):
            value = props.get(prop)

            if isinstance(value, str):
                props[prop] = Var(
                    value,
                    _var_data=VarData(
                        imports={CORE_ICONS_LIBRARY: [ImportVar(tag=value)]}
                    ),
                )

        stroke_width = props.get("stroke_width", 1.5)

        cls.set_class_name(
            f"[&_path]:stroke-[{stroke_width}]",
            props,
        )

        return super().create(*children, **props)


hi = icon = HugeIcon.create
```

```python
import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn
from ..core.hugeicon import hi


class ClassNames:
    ROOT = "flex w-full flex-col"

    ITEM = "not-last:border-b border-input block group/accordion-item"

    TRIGGER = (
        "flex flex-1 items-start justify-between "
        "rounded-lg border border-transparent py-2.5 text-left text-sm font-medium "
        "list-none cursor-pointer outline-none hover:underline"
    )

    TRIGGER_ICON = (
        "pointer-events-none shrink-0 ml-auto size-4 text-muted-foreground "
        "transition-transform duration-50 "
        "group-open/accordion-item:rotate-180"
    )

    PANEL = "overflow-hidden text-sm"

    PANEL_DIV = (
        "pt-0 pb-2.5 "
        "[&_a]:underline [&_a]:underline-offset-3 [&_a]:hover:text-foreground "
        "[&_p:not(:last-child)]:mb-4"
    )


class NativeAccordionRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        data_slot = props.pop("data_slot", "accordion")
        props["data-slot"] = data_slot
        cls.set_class_name(ClassNames.ROOT, props)
        return rx.el.div(*children, **props)


class NativeAccordionItem(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        data_slot = props.pop("data_slot", "accordion-item")
        props["data-slot"] = data_slot
        name = props.pop("name", None)
        if name:
            custom_attrs = props.setdefault("custom_attrs", {})
            custom_attrs["name"] = name

        cls.set_class_name(ClassNames.ITEM, props)
        return rx.el.details(*children, **props)


class NativeAccordionTrigger(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        data_slot = props.pop("data_slot", "accordion-trigger")
        props["data-slot"] = data_slot
        cls.set_class_name(ClassNames.TRIGGER, props)

        return rx.el.summary(
            *children,
            hi(
                "ArrowDown01Icon",
                class_name=ClassNames.TRIGGER_ICON,
                data_slot="accordion-trigger-icon",
            ),
            **props,
        )


class NativeAccordionPanel(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        data_slot = props.pop("data_slot", "accordion-panel")
        props["data-slot"] = data_slot
        inner_class = props.pop("class_name", "")
        cls.set_class_name(ClassNames.PANEL, props)

        return rx.el.div(
            rx.el.div(*children, class_name=cn(ClassNames.PANEL_DIV, inner_class)),
            **props,
        )


class NativeAccordion(ComponentNamespace):
    root = staticmethod(NativeAccordionRoot.create)
    item = staticmethod(NativeAccordionItem.create)
    trigger = staticmethod(NativeAccordionTrigger.create)
    panel = staticmethod(NativeAccordionPanel.create)
    class_names = ClassNames


accordion = NativeAccordion()
```

# Examples

## Basic

Built on native `<details>`/`<summary>` — expand/collapse, keyboard support, and the chevron rotation all come from the browser and `group-open/accordion-item:rotate-180`, no JS required.

**Props used:** `name` on `accordion.item` (groups items so only one stays open at a time, matching native `<details name="...">` behavior).

```python
def accordion_basic():
    return rx.el.div(
        accordion.root(
            accordion.item(
                accordion.trigger("Models"),
                accordion.panel(
                    rx.el.p("- Genesis launched a new era of exploration."),
                    rx.el.p("- Explorer uncovered new planets beyond our reach."),
                    rx.el.p("- Voyager 1 ventured into interstellar space."),
                    rx.el.p("- Apollo landed humans on the Moon."),
                ),
                name="single",
            ),
            accordion.item(
                accordion.trigger("Spacecraft"),
                accordion.panel(
                    rx.el.p("- Curiosity sent back valuable data from Mars."),
                    rx.el.p("- The Hubble Telescope captured distant galaxies."),
                    rx.el.p("- James Webb will explore the universe's origins."),
                    rx.el.p("- The ISS orbits Earth, conducting critical experiments."),
                ),
                open=True,
                name="single",
            ),
            accordion.item(
                accordion.trigger("Space Discoveries"),
                accordion.panel(
                    rx.el.p("- Saturn's rings have fascinated scientists for years."),
                    rx.el.p("- The Mars Rover is studying the planet's surface."),
                    rx.el.p(
                        "- NASA's Artemis program aims to return humans to the Moon."
                    ),
                    rx.el.p("- Solar missions help us understand space weather."),
                ),
                name="single",
            ),
            class_name="w-full max-w-md mx-auto",
        ),
        class_name="h-[45vh] w-full justify-center pt-10 px-8",
    )
```

# API Reference

## accordion.root

```python
accordion.root(
    accordion.item(...),
    accordion.item(...),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## accordion.item

Renders a native `<details>`. Give matching items the same `name` to make them mutually exclusive (native `<details name="...">` grouping — opening one closes the others in the group automatically).

```python
accordion.item(
    accordion.trigger("Is it accessible?"),
    accordion.panel("Yes, built on native semantics."),
    name="faq",
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `name`       | `str` |         |
| `class_name` | `str` | `""`    |

## accordion.trigger

Renders a `<summary>` with a chevron icon appended automatically — no need to add one yourself.

```python
accordion.trigger("Is it accessible?")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## accordion.panel

```python
accordion.panel("Yes. It adheres to the WAI-ARIA design pattern.")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |
