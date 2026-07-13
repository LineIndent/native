---
title: "Select"
description: "A styled native HTML select element with consistent design system integration."
order: 13
---


## Select, A Styled Native Html Select Element With Consistent Design System Integration.



> Error processing `usage`: module, class, method, function, traceback, frame, or code object was expected, got NativeSelect


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
from typing import Literal

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn
from ..core.hugeicon import hi

LiteralNativeSelectSize = Literal["default", "sm"]


class ClassNames:
    WRAPPER = "group/native-select relative w-fit has-[select:disabled]:opacity-50"

    SELECT = (
        "h-8 w-full min-w-0 appearance-none rounded-lg border border-input "
        "bg-transparent py-1 pr-8 pl-2.5 text-sm outline-none "
        "select-none selection:bg-primary selection:text-primary-foreground "
        "placeholder:text-muted-foreground "
        "focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 "
        "disabled:pointer-events-none disabled:cursor-not-allowed "
        "aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 "
        "data-[size=sm]:h-7 data-[size=sm]:rounded-[min(var(--radius-md),10px)] "
        "data-[size=sm]:py-0.5 "
        "dark:bg-input/30 dark:hover:bg-input/50 "
        "dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40"
    )

    ICON = (
        "pointer-events-none absolute top-1/2 right-2.5 size-4 -translate-y-1/2 "
        "text-muted-foreground select-none"
    )

    OPTION = "bg-[Canvas] text-[CanvasText]"

    OPTGROUP = "bg-[Canvas] text-[CanvasText]"


class NativeSelectComponent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        size = props.pop("size", "default")
        wrapper_class_name = props.pop("wrapper_class_name", "")
        data_slot = props.pop("data_slot", "native-select")

        select_class_name = cn(ClassNames.SELECT, props.get("class_name", ""))
        props["class_name"] = select_class_name
        props["data-slot"] = data_slot
        props["data-size"] = size

        select_el = rx.el.select(*children, **props)

        return rx.el.div(
            select_el,
            hi(
                "ArrowDown01Icon",
                class_name=ClassNames.ICON,
                data_slot="native-select-icon",
                aria_hidden="true",
            ),
            data_slot="native-select-wrapper",
            data_size=size,
            class_name=cn(ClassNames.WRAPPER, wrapper_class_name),
        )


class NativeSelectOptionComponent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "native-select-option"
        cls.set_class_name(ClassNames.OPTION, props)
        return rx.el.option(*children, **props)


class NativeSelectOptGroupComponent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "native-select-optgroup"
        cls.set_class_name(ClassNames.OPTGROUP, props)
        return rx.el.optgroup(*children, **props)


class NativeSelect(ComponentNamespace):
    __call__ = staticmethod(NativeSelectComponent.create)
    option = staticmethod(NativeSelectOptionComponent.create)
    optgroup = staticmethod(NativeSelectOptGroupComponent.create)
    class_names = ClassNames


select = NativeSelect()
```

# Examples

## Basic

A single native `<select>` paired with a `field.label`. Uses `wrapper_class_name` to stretch the select to the full width of its container.

**Props used:** `id`, `name`, `default_value`, `wrapper_class_name` on `select`; `value` on `select.option`; `html_for` on `field.label`.

```python
def select_basic() -> rx.Component:
    return rx.el.div(
        field.root(
            field.label("Favorite fruit", html_for="fruit-basic"),
            select(
                select.option("Apple", value="apple"),
                select.option("Banana", value="banana"),
                select.option("Blueberry", value="blueberry"),
                select.option("Grapes", value="grapes"),
                select.option("Pineapple", value="pineapple"),
                id="fruit-basic",
                name="fruit",
                default_value="apple",
                wrapper_class_name="w-full",
            ),
        ),
        class_name="mx-auto max-w-sm",
    )
```

## Grouped options

Options organized under `select.optgroup` headings, with a disabled, hidden first option acting as a placeholder — the standard way to show placeholder text in a native select without a real empty value being selectable.

**Props used:** `label` on `select.optgroup`; `value`, `disabled`, `hidden` on `select.option`; `id`, `name`, `default_value`, `wrapper_class_name` on `select`.

```python
def select_optgroup() -> rx.Component:
    return rx.el.div(
        field.root(
            field.label("Ingredient", html_for="ingredient-select"),
            select(
                select.option(
                    "Select an ingredient", value="", disabled=True, hidden=True
                ),
                select.optgroup(
                    select.option("Apple", value="apple"),
                    select.option("Banana", value="banana"),
                    select.option("Blueberry", value="blueberry"),
                    label="Fruits",
                ),
                select.optgroup(
                    select.option("Carrot", value="carrot"),
                    select.option("Potato", value="potato"),
                    select.option("Broccoli", value="broccoli"),
                    label="Vegetables",
                ),
                id="ingredient-select",
                name="ingredient",
                default_value="",
                wrapper_class_name="w-full",
            ),
        ),
        class_name="mx-auto max-w-sm",
    )
```

## Sizes

Two size variants side by side — `sm` for compact layouts (toolbars, table cells) and the `default` size for standalone form fields.

**Props used:** `size`, `default_value` on `select`; `value` on `select.option`.

```python
def select_sizes() -> rx.Component:
    return rx.el.div(
        select(
            select.option("Small", value="sm"),
            select.option("Medium", value="md"),
            select.option("Large", value="lg"),
            default_value="md",
            size="sm",
        ),
        select(
            select.option("Small", value="sm"),
            select.option("Medium", value="md"),
            select.option("Large", value="lg"),
            default_value="md",
        ),
        class_name="mx-auto flex max-w-sm items-center gap-4",
    )
```

## Form layout

Two selects grouped under a shared `field.set` with a `field.legend`, showing how selects compose inside a larger form section.

**Props used:** `id`, `name`, `default_value`, `wrapper_class_name` on `select`; `value` on `select.option`; `html_for` on `field.label`.

```python
def select_form() -> rx.Component:
    return field.set(
        field.legend("Shipping details"),
        field.group(
            field.root(
                field.label("Country", html_for="shipping-country"),
                select(
                    select.option("United States", value="us"),
                    select.option("Canada", value="ca"),
                    select.option("United Kingdom", value="uk"),
                    select.option("Germany", value="de"),
                    id="shipping-country",
                    name="country",
                    default_value="us",
                    wrapper_class_name="w-full",
                ),
            ),
            field.root(
                field.label("Timezone", html_for="shipping-timezone"),
                select(
                    select.option("Pacific Time (PT)", value="pt"),
                    select.option("Mountain Time (MT)", value="mt"),
                    select.option("Central Time (CT)", value="ct"),
                    select.option("Eastern Time (ET)", value="et"),
                    id="shipping-timezone",
                    name="timezone",
                    default_value="et",
                    wrapper_class_name="w-full",
                ),
            ),
        ),
        class_name="mx-auto max-w-sm",
    )
```

## Disabled

A disabled select with a `field.description` explaining why it's locked. Disabling cascades visually to the whole control via the wrapper's `has-[select:disabled]` styling.

**Props used:** `id`, `default_value`, `disabled`, `wrapper_class_name` on `select`; `value` on `select.option`.

```python
def select_disabled() -> rx.Component:
    return rx.el.div(
        field.root(
            field.label("Country", html_for="country-disabled"),
            select(
                select.option("United States", value="us"),
                select.option("Canada", value="ca"),
                select.option("Mexico", value="mx"),
                id="country-disabled",
                default_value="us",
                disabled=True,
                wrapper_class_name="w-full",
            ),
            field.description("This field is currently locked."),
        ),
        class_name="mx-auto max-w-sm",
    )
```

# API Reference
 
## select
 
The main select component. Calling `select(...)` directly renders the native `<select>` wrapped in a positioning `div` with the chevron icon — `select` is itself callable (via `NativeSelect.__call__`), so no separate `.root` is needed.
 
```python
select(
    select.option("Option 1", value="option1"),
    select.option("Option 2", value="option2"),
)
```
 
| Prop                 | Type                    | Default          |
| -------------------- | ----------------------- | ---------------- |
| `size`                | `Literal["default", "sm"]` | `"default"`   |
| `wrapper_class_name`  | `str`                   | `""`              |
| `class_name`          | `str`                   | `""`              |
| `data_slot`           | `str`                   | `"native-select"` |
| `disabled`            | `bool`                  | `False`           |
| `value` / `default_value` | `str`               |                   |
| `name`                | `str`                   |                   |
| `id`                  | `str`                   |                   |
| `on_change`           | `EventHandler`          |                   |
 
Any other prop accepted by a native HTML `<select>` (`required`, `aria-invalid`, etc.) is also passed straight through.
 
## select.option
 
Represents an individual option within the select.
 
```python
select.option("Apple", value="apple")
select.option("Sold out", value="oos", disabled=True)
```
 
| Prop       | Type   | Default |
| ---------- | ------ | ------- |
| `value`    | `str`  |         |
| `disabled` | `bool` | `False` |
| `hidden`   | `bool` | `False` |
 
## select.optgroup
 
Groups related options together under a labeled heading.
 
```python
select.optgroup(
    select.option("Apple", value="apple"),
    select.option("Banana", value="banana"),
    label="Fruits",
)
```
 
| Prop       | Type   | Default |
| ---------- | ------ | ------- |
| `label`    | `str`  |         |
| `disabled` | `bool` | `False` |
