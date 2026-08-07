---
title: "Radio Group"
description: "A set of checkable buttons—known as radio buttons—where no more than one of the buttons can be checked at a time."
order: 0
---


## Radio Group, A Set Of Checkable Buttons—Known As Radio Buttons—Where No More Than One Of The Buttons Can Be Checked At A Time.


```python
from components.ui.radio_group import radio_group
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
import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn


class ClassNames:
    ROOT = "w-full flex flex-col gap-3 disabled:opacity-50 disabled:cursor-not-allowed text-sm"

    ITEM_ROOT = (
        "group relative inline-flex size-4 shrink-0 cursor-pointer items-center "
        "justify-center rounded-full border border-input "
        "has-[:disabled]:cursor-not-allowed has-[:disabled]:opacity-50 "
        "has-[:focus-visible]:border-ring has-[:focus-visible]:ring-3 has-[:focus-visible]:ring-ring/50 "
        "has-[[aria-invalid=true]]:border-destructive has-[[aria-invalid=true]]:ring-3 "
        "has-[[aria-invalid=true]]:ring-destructive/20 "
        "dark:bg-input/30 "
        "has-[:checked]:border-primary "
        "peer-has-[[data-slot=field-content]]:mt-0.5 [&:has(~[data-slot=field-content])]:mt-0.5"
    )

    ITEM_INPUT = "peer sr-only"

    ITEM_INDICATOR = "hidden peer-checked:flex items-center justify-center"

    ITEM_INDICATOR_DOT = "size-2 rounded-full bg-primary"

    _KNOWN_INPUT_PROPS = (
        "checked",
        "default_checked",
        "disabled",
        "required",
        "id",
    )


class RadioGroupRoot(CoreComponent):
    @classmethod
    def create(cls, *children, disabled: bool = False, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "radio-group"
        props["role"] = "radiogroup"
        if disabled:
            props["disabled"] = True
        cls.set_class_name(cn(ClassNames.ROOT, custom_classes), props)
        return rx.el.fieldset(*children, **props)


class RadioGroupItem(CoreComponent):
    @classmethod
    def create(cls, *children, name: str, value: str, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")

        input_props = {"name": name, "value": value}
        for key in list(props.keys()):
            if (
                key in ClassNames._KNOWN_INPUT_PROPS
                or key.startswith("on_")
                or key.startswith("data-")
                or key.startswith("aria-")
            ):
                input_props[key] = props.pop(key)

        input_props["type"] = "radio"
        input_props["data-slot"] = "radio-group-item-input"
        input_props["class_name"] = ClassNames.ITEM_INPUT

        props["data-slot"] = "radio-group-item"

        if not children:
            children = (RadioGroupIndicator.create(),)

        cls.set_class_name(cn(ClassNames.ITEM_ROOT, custom_classes), props)
        return rx.el.label(rx.el.input(**input_props), *children, **props)


class RadioGroupIndicator(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        if len(children) == 0:
            children = (rx.el.span(class_name=ClassNames.ITEM_INDICATOR_DOT),)
        props["data-slot"] = "radio-group-item-indicator"
        cls.set_class_name(ClassNames.ITEM_INDICATOR, props)
        return rx.el.span(*children, **props)


class RadioGroup(ComponentNamespace):
    root = staticmethod(RadioGroupRoot.create)
    item = staticmethod(RadioGroupItem.create)
    indicator = staticmethod(RadioGroupIndicator.create)
    class_names = ClassNames


radio_group = RadioGroup()
```

# Examples

## Description

Radio group items with a description using the `Field` component.

```python
def radio_group_description() -> rx.Component:
    return radio_group.root(
        *[
            field.root(
                radio_group.item(
                    name="spacing",
                    value=value,
                    id=f"desc-{value}",
                    default_checked=(value == "comfortable"),
                ),
                field.content(
                    field.label(title, html_for=f"desc-{value}"),
                    field.description(description),
                ),
                orientation="horizontal",
            )
            for value, title, description in OPTIONS
        ],
        class_name="w-fit",
    )
```

## Choice Card

Use `field.label` to wrap the entire `Field` for a clickable card-style selection.

```python
def radio_group_choice_card() -> rx.Component:
    return radio_group.root(
        *[
            field.label(
                field.root(
                    field.content(
                        field.title(title),
                        field.description(description),
                    ),
                    radio_group.item(
                        name="plan",
                        value=value,
                        id=f"{value}-plan",
                        default_checked=(value == "plus"),
                    ),
                    orientation="horizontal",
                ),
                html_for=f"{value}-plan",
            )
            for value, title, description in PLANS
        ],
        class_name="max-w-sm",
    )
```

## Fieldset

Use `field.set` and `field.legend` to group radio items with a label and description.

```python
def radio_group_fieldset() -> rx.Component:
    return field.set(
        field.legend("Subscription Plan", variant="label"),
        field.description("Yearly and lifetime plans offer significant savings."),
        radio_group.root(
            *[
                field.root(
                    radio_group.item(
                        name="plan",
                        value=value,
                        id=f"plan-{value}",
                        default_checked=(value == "monthly"),
                    ),
                    field.label(
                        label, html_for=f"plan-{value}", class_name="font-normal"
                    ),
                    orientation="horizontal",
                )
                for value, label in PLANS
            ],
        ),
        class_name="w-full max-w-xs",
    )
```

## Disabled

Use the `disabled` prop on `radio.root` to disable all items.

```python
def radio_group_disabled() -> rx.Component:
    return radio_group.root(
        *[
            field.root(
                radio_group.item(
                    name="disabled-demo",
                    value=value,
                    id=id_,
                    disabled=is_disabled,
                    default_checked=(value == "option2"),
                ),
                field.label(label, html_for=id_, class_name="font-normal"),
                orientation="horizontal",
                **({"data-disabled": "true"} if is_disabled else {}),
            )
            for value, id_, label, is_disabled in OPTIONS
        ],
        class_name="w-fit",
    )
```

## Invalid

Use `aria-invalid` on `radio.item` and `data-invalid` on `field.root` to show validation errors.

```python
def radio_group_invalid() -> rx.Component:
    return field.set(
        field.legend("Notification Preferences", variant="label"),
        field.description("Choose how you want to receive notifications."),
        radio_group.root(
            *[
                field.root(
                    radio_group.item(
                        name="notification-preferences",
                        value=value,
                        id_=id_,
                        default_checked=(value == "email"),
                        aria_invalid=True,
                    ),
                    field.label(label, html_for=id_, class_name="font-normal"),
                    orientation="horizontal",
                    data_invalid=True,
                )
                for value, id_, label in OPTIONS
            ],
        ),
        class_name="w-full max-w-xs",
    )
```

# API Reference

## radio_group.root

The container element for a set of radio options. Renders a native `<fieldset role="radiogroup">`. Setting `disabled=True` on the root automatically disables all descendant radio controls without needing to set it on each item individually.

```python
radio_group.root(
    radio_group.item(name="plan", value="free", id_="plan-free"),
    radio_group.item(name="plan", value="pro", id_="plan-pro"),
    disabled=False,
)
```

| Prop         | Type   | Default         |
| ------------ | ------ | --------------- |
| `disabled`   | `bool` | `False`         |
| `class_name` | `str`  | `""`            |
| `data_slot`  | `str`  | `"radio-group"` |
| `role`       | `str`  | `"radiogroup"`  |

Any additional HTML props passed to `radio_group.root` are forwarded directly to the underlying `<fieldset>`.

## radio_group.item

Represents an individual radio control wrapped in a native `<label>`. Automatically extracts native form input attributes (`name`, `value`, `checked`, `disabled`, `aria-*`, `data-*`, etc.) and attaches them to an internal sr-only `<input type="radio">`. If no children are passed, it automatically renders a `radio_group.indicator`.

```python
radio_group.item(
    name="framework",
    value="reflex",
    id_="framework-reflex",
    default_checked=True,
)
```

| Prop              | Type   | Default              |
| ----------------- | ------ | -------------------- |
| `name`            | `str`  | _(required)_         |
| `value`           | `str`  | _(required)_         |
| `id` / `id_`      | `str`  |                      |
| `checked`         | `bool` |                      |
| `default_checked` | `bool` |                      |
| `disabled`        | `bool` | `False`              |
| `required`        | `bool` | `False`              |
| `class_name`      | `str`  | `""`                 |
| `data_slot`       | `str`  | `"radio-group-item"` |

Event handlers (e.g., `on_change`, `on_click`), accessibility attributes (`aria_*`), and state attributes (`data_*`) are automatically routed to the inner `<input>`.

## radio_group.indicator

Renders the visual selection state inside the radio item. Controlled purely via peer CSS rules (`peer-checked`). If called without children, it defaults to rendering a centered styled dot (`ITEM_INDICATOR_DOT`).

```python
radio_group.indicator()

radio_group.indicator(
    rx.el.span(class_name="size-2 rounded-full bg-accent")
)
```

| Prop         | Type  | Default                        |
| ------------ | ----- | ------------------------------ |
| `class_name` | `str` | `""`                           |
| `data_slot`  | `str` | `"radio-group-item-indicator"` |
