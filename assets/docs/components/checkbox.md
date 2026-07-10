---
title: "Checkbox"
description: "A control that allows the user to toggle between checked and not checked."
order: 5
---


## Checkbox, A Control That Allows The User To Toggle Between Checked And Not Checked.


```python
from components.ui.checkbox import Checkbox
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
    ROOT = (
        "group relative inline-flex size-4 shrink-0 cursor-pointer items-center "
        "justify-center rounded-[4px] border border-input "
        "has-[:disabled]:cursor-not-allowed has-[:disabled]:opacity-50 "
        "has-[:focus-visible]:border-ring has-[:focus-visible]:ring-3 has-[:focus-visible]:ring-ring/50 "
        "has-[[aria-invalid=true]]:border-destructive has-[[aria-invalid=true]]:ring-3 "
        "has-[[aria-invalid=true]]:ring-destructive/20 "
        "dark:bg-input/30 "
        "has-[:checked]:border-primary has-[:checked]:bg-primary has-[:checked]:text-primary-foreground "
        "dark:has-[:checked]:bg-primary"
    )

    INPUT = "peer sr-only"

    INDICATOR = "hidden peer-checked:grid place-content-center text-current [&>svg]:size-3.5"

    BOX = (
        "pointer-events-none flex size-4 shrink-0 items-center justify-center "
        "rounded-[4px] border border-input "
        "peer-focus-visible:border-ring peer-focus-visible:ring-3 peer-focus-visible:ring-ring/50 "
        "peer-disabled:cursor-not-allowed peer-disabled:opacity-50 "
        "peer-aria-[invalid=true]:border-destructive peer-aria-[invalid=true]:ring-3 "
        "peer-aria-[invalid=true]:ring-destructive/20 "
        "dark:bg-input/30 "
        "peer-checked:border-primary peer-checked:bg-primary peer-checked:text-primary-foreground "
        "dark:peer-checked:bg-primary"
    )



class CheckboxRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")

        input_props = {}
        for key in (
            "checked",
            "default_checked",
            "disabled",
            "required",
            "name",
            "value",
            "on_change",
            "id",
        ):
            if key in props:
                input_props[key] = props.pop(key)

        input_props["type"] = "checkbox"
        input_props["data-slot"] = "checkbox-input"
        input_props["class_name"] = ClassNames.INPUT

        props["data-slot"] = "checkbox"

        if not children:
            children = (CheckboxIndicator.create(),)

        cls.set_class_name(cn(ClassNames.ROOT, custom_classes), props)
        return rx.el.label(rx.el.input(**input_props), *children, **props)


class CheckboxIndicator(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        if len(children) == 0:
            children = (hi("Tick02Icon"),)
        props["data-slot"] = "checkbox-indicator"
        cls.set_class_name(ClassNames.INDICATOR, props)
        return rx.el.span(*children, **props)


class Checkbox(ComponentNamespace):
    root = staticmethod(CheckboxRoot.create)
    indicator = staticmethod(CheckboxIndicator.create)
    class_names = ClassNames


checkbox = Checkbox()
```

# Examples

## Basic

Pair the checkbox with `field.root` and `field.label` for proper layout and labeling.

```python
def checkbox_basic():
    return rx.el.div(
        field.root(
            checkbox.root(
                checkbox.indicator(),
                id="terms-checkbox-basic",
            ),
            field.label(
                "Accept terms and conditions",
                html_for="terms-checkbox-basic",
            ),
            orientation="horizontal",
        ),
        class_name="mx-auto max-w-sm",
    )
```

## Description

Use `field.description` for helper text.

```python
def checkbox_description() -> rx.Component:
    return field.group(
        field.root(
            checkbox.root(
                checkbox.indicator(),
                id="terms-checkbox-desc",
                name="terms-checkbox-desc",
                default_checked=True,
            ),
            field.content(
                field.label(
                    "Accept terms and conditions",
                    html_for="terms-checkbox-desc",
                ),
                field.description(
                    "By clicking this checkbox, you agree to the terms and conditions."
                ),
            ),
            orientation="horizontal",
        ),
        class_name="mx-auto w-72",
    )
```

## Disabled

Use the `disabled` prop to prevent interaction and add the `data_disabled=True` attribute to the component for disabled styles.

```python
def checkbox_disabled() -> rx.Component:
    return rx.el.div(
        field.root(
            checkbox.root(
                checkbox.indicator(),
                id="toggle-checkbox-disabled",
                name="toggle-checkbox-disabled",
                disabled=True,
            ),
            field.label(
                "Enable notifications",
                html_for="toggle-checkbox-disabled",
            ),
            orientation="horizontal",
            data_disabled=True,
        ),
        class_name="mx-auto w-56",
    )
```

## Group

Use multiple fields to create a checkbox list.

```python
def checkbox_group() -> rx.Component:
    return rx.el.fieldset(
        rx.el.legend(
            "Show these items on the desktop:",
            class_name="mb-1.5 font-medium text-sm text-foreground",
        ),
        rx.el.p(
            "Select the items you want to show on the desktop.",
            class_name="mb-4 text-sm text-muted-foreground",
        ),
        rx.el.div(
            field.root(
                checkbox.root(
                    checkbox.indicator(),
                    id="hard-disks",
                    default_checked=True,
                ),
                field.label(
                    "Hard disks", html_for="hard-disks", class_name="font-normal"
                ),
                orientation="horizontal",
            ),
            field.root(
                checkbox.root(
                    checkbox.indicator(),
                    id="ext-disks",
                    default_checked=True,
                ),
                field.label(
                    "External disks", html_for="ext-disks", class_name="font-normal"
                ),
                orientation="horizontal",
            ),
            field.root(
                checkbox.root(
                    checkbox.indicator(),
                    id="cds-dvds",
                ),
                field.label(
                    "CDs, DVDs, and iPods",
                    html_for="cds-dvds",
                    class_name="font-normal",
                ),
                orientation="horizontal",
            ),
            field.root(
                checkbox.root(
                    checkbox.indicator(),
                    id="servers",
                ),
                field.label(
                    "Connected servers", html_for="servers", class_name="font-normal"
                ),
                orientation="horizontal",
            ),
            class_name="flex flex-col w-full",
        ),
    )
```
