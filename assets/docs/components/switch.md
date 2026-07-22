---
title: "Switch"
description: "A control that allows the user to toggle between checked and not checked."
order: 0
---


## Switch, A Control That Allows The User To Toggle Between Checked And Not Checked.



> Component `switch` not found


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
    ROOT = "inline-flex items-center gap-3 cursor-pointer select-none group/switch"

    INPUT = "peer sr-only"

    TRACK = (
        "relative rounded-full bg-muted "
        "outline-none "
        "group-data-[size=default]/switch:h-[18.4px] group-data-[size=default]/switch:w-[32px] "
        "group-data-[size=sm]/switch:h-[14px] group-data-[size=sm]/switch:w-[24px] "
        "group-has-[input:checked]/switch:bg-primary "
        "peer-focus-visible:ring-3 peer-focus-visible:ring-ring/50 peer-focus-visible:outline-1 peer-focus-visible:outline-ring "
        "group-aria-[invalid=true]/switch:border-destructive group-aria-[invalid=true]/switch:ring-3 group-aria-[invalid=true]/switch:ring-destructive/20 "
        "group-has-[:disabled]/switch:opacity-50 group-has-[:disabled]/switch:pointer-events-none group-has-[:disabled]/switch:cursor-not-allowed"
    )

    THUMB = (
        "pointer-events-none block rounded-full bg-background shadow-sm ring-0 transition-transform duration-200 "
        "group-data-[size=default]/switch:size-4 group-data-[size=sm]/switch:size-3 "
        "translate-x-0.5 "
        "group-has-[input:checked]/switch:group-data-[size=default]/switch:translate-x-[14px] "
        "group-has-[input:checked]/switch:group-data-[size=sm]/switch:translate-x-[10px] "
        "group-has-[input:checked]/switch:dark:bg-primary-foreground "
        "dark:bg-foreground"
    )

    LABEL = "text-sm font-medium leading-none text-foreground"


class NativeSwitch(CoreComponent):
    @classmethod
    def create(cls, label_text: str = "", **props) -> rx.Component:
        props["data-slot"] = "switch"

        size = props.pop("size", "default")
        props["data-size"] = size

        invalid = props.pop("invalid", False)
        if invalid:
            props["aria-invalid"] = "true"

        track_class_name = props.pop("track_class_name", "")
        thumb_class_name = props.pop("thumb_class_name", "")

        input_props = {}
        for key in (
            "id",
            "checked",
            "default_checked",
            "disabled",
            "required",
            "name",
            "value",
            "on_change",
            "custom_attrs",
        ):
            if key in props:
                input_props[key] = props.pop(key)

        cls.set_class_name(ClassNames.ROOT, props)

        return rx.el.label(
            rx.el.input(type="checkbox", class_name=ClassNames.INPUT, **input_props),
            rx.el.div(
                rx.el.span(
                    # Dynamically merge custom thumb classes
                    class_name=cn(ClassNames.THUMB, thumb_class_name)
                ),
                # Dynamically merge custom track classes
                class_name=cn(ClassNames.TRACK, track_class_name),
            ),
            rx.el.span(label_text, class_name=ClassNames.LABEL)
            if label_text
            else rx.fragment(),
            **props,
        )


class SwitchNamespace(ComponentNamespace):
    root = staticmethod(NativeSwitch.create)
    class_names = ClassNames


switch = SwitchNamespace()
```

# Examples

## Basic

A simple switch rendering an internal semantic label using the inline `label_text` argument.

**Props used:** `label_text` as the first argument in `switch.root`.

```python
def switch_basic() -> rx.Component:
    return field.root(
        field.content(
            field.title("Strict Mode"),
            field.description(
                "Enable strict validation protocols across all incoming API payloads."
            ),
        ),
        switch.root(id="strict-mode"),
        orientation="horizontal",
        class_name="justify-between items-center border rounded-lg p-4 w-full max-w-md",
    )
```


## Choice Card

Card-style premium selection where `field.label` wraps the entire layout block. Clicking anywhere on the card container natively triggers the nested switch checkbox.

**Props used:** `id` on `switch.root`; `html_for` on `field.label`.

```python
def switch_with_label() -> rx.Component:
    return field.label(
        rx.el.div(
            field.content(
                field.title("Enterprise Pipeline"),
                field.description(
                    "Deploy dedicated runners, isolated networks, and unlimited concurrency."
                ),
            ),
            switch.root(id="enterprise-plan"),
            class_name="flex items-start justify-between gap-4 max-w-sm",
        ),
        html_for="enterprise-plan",
    )
```

## Sizes

Two size variants available side by side—`sm` for tight, compact toolbars or layouts, and the `default` size for normal structural form elements.

**Props used:** `size` on `switch.root`; `orientation="horizontal"` on `field.root`.

```python
def switch_sizes() -> rx.Component:
    return field.group(
        field.root(
            switch.root(
                id="switch-size-sm",
                size="sm",
            ),
            field.label(
                "Small",
                html_for="switch-size-sm",
            ),
            orientation="horizontal",
        ),
        field.root(
            switch.root(
                id="switch-size-default",
                size="default",
            ),
            field.label(
                "Default",
                html_for="switch-size-default",
            ),
            orientation="horizontal",
        ),
        class_name="w-full max-w-[10rem]",
    )
```

## Invalid

An invalid or error state signaling form validation failures. The switch track highlights structural errors through `aria-invalid`, and the parent `field.root` dynamically updates text styling to the system's destructive state.

**Props used:** `invalid` on `switch.root`; `data-invalid="true"` on `field.root`.

```python
def switch_invalid() -> rx.Component:
    return field.root(
        field.content(
            field.label(
                "Accept terms and conditions",
                html_for="switch-terms",
            ),
            field.description("You must accept the terms and conditions to continue."),
        ),
        switch.root(
            id="switch-terms",
            aria_invalid="true",
        ),
        orientation="horizontal",
        data_invalid="true",
        class_name="max-w-sm",
    )
```

## Disabled

A disabled switch control with interaction constraints. Disabling cascades visually and functionally down to the control via structural `group-has-[:disabled]` selectors, lowering control opacity and locking out all user inputs.

**Props used:** `disabled` on `switch.root`; `data-disabled="true"` on `field.root`.

```python
def switch_disabled() -> rx.Component:

    return field.root(
        switch.root(
            id="switch-disabled-unchecked",
            disabled=True,
        ),
        field.label(
            "Disabled",
            html_for="switch-disabled-unchecked",
        ),
        orientation="horizontal",
        data_disabled="true",
        class_name="w-full max-w-[10rem]",
    )
```

# API Reference

## switch.root

The main switch control component. Renders an accessible, zero-latency toggle using a native hidden checkbox input element wrapped in a clickable semantic label layout block.

```python
switch.root("Enable notifications", id="notify", size="default")
```

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `label_text` | `str` | `""` | Optional descriptive label string inserted directly alongside the switch. |
| `size` | `Literal["default", "sm"]` | `"default"` | Sets the physical width/height scaling of the track and thumb elements. |
| `invalid` | `bool` | `False` | Sets `aria-invalid="true"` to trigger error styling. |
| `disabled` | `bool` | `False` | Disables interaction and drops opacity. |
| `checked` | `bool` |  | Controlled component state binding. |
| `default_checked` | `bool` |  | Uncontrolled default initial state setting. |
| `track_class_name` | `str` | `""` | Fine-grain custom Tailwind class overrides directly injected onto the track. |
| `thumb_class_name` | `str` | `""` | Fine-grain custom Tailwind class overrides directly injected onto the thumb. |
| `id` | `str` |  | Unique identifier assigned directly to the inner hidden input peer. |
| `name` | `str` |  | Form submission parameter identifier. |
| `on_change` | `EventHandler` |  | Fired instantly as soon as the switch toggle changes state. |

Any other attribute accepted by a standard HTML `<input type="checkbox">` (`required`, `value`, etc.) will pass straight through to the inner input control peer.
