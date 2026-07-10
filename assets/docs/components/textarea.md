---
title: "Textarea"
description: "Displays a form textarea or a component that looks like a textarea."
order: 23
---


## Textarea, Displays A Form Textarea Or A Component That Looks Like A Textarea.


```python
from components.ui.textarea import textarea
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
from reflex_components_core.el import Textarea

from ..core.core import CoreComponent


class ClassNames:
    ROOT = (
        "flex field-sizing-content min-h-16 w-full rounded-lg border border-input bg-transparent "
        "px-2.5 py-2 text-base transition-colors outline-none placeholder:text-muted-foreground "
        "focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 disabled:cursor-not-allowed "
        "disabled:bg-input/50 disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 "
        "aria-invalid:ring-destructive/20 md:text-sm dark:bg-input/30 dark:disabled:bg-input/80 "
        "dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40"
    )


class TextAreaComponent(Textarea, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Textarea:
        props.setdefault(
            "custom_attrs",
            {
                "autoComplete": "off",
                "autoCapitalize": "none",
                "autoCorrect": "off",
                "spellCheck": "false",
            },
        )
        props.setdefault("data_slot", "textarea")
        cls.set_class_name(ClassNames.ROOT, props)
        return super().create(*children, **props)


textarea = TextAreaComponent.create
```

# Examples

## Basic
A standard multiline text area for general text input.

```python
def textarea_basic_demo():
    return textarea(placeholder="Type your message here.", class_name="max-w-xs")
```

## Field
Use `field.root`, `field.label`, and `field.description` together with a form control (such as textarea) to build a structured field with a label and helper text.

```python
def textarea_field():
    return field.root(
        field.label(
            "Message",
            html_for="textarea-message",
        ),
        field.description(
            "Enter your message below.",
        ),
        textarea(
            id="textarea-message",
            placeholder="Type your message here.",
        ),
        class_name="max-w-xs",
    )
```

## Disabled
Use the `disabled` prop on textarea to disable user input. Apply `data-disabled` on `field.root` to propagate disabled styling to all field-related elements and ensure consistent visual state handling.

```python
def textarea_disabled():
    return field.root(
        field.label(
            "Message",
            html_for="textarea-disabled",
        ),
        textarea(
            id="textarea-disabled",
            placeholder="Type your message here.",
            disabled=True,
        ),
        **{"data-disabled": True},
        class_name="max-w-xs",
    )
```

## Invalid
Use the `aria-invalid` prop to mark the textarea as invalid. To style the invalid state, add the `data-invalid` attribute to the `field.root` component.

```python
def textarea_invalid():
    return field.root(
        field.label(
            "Message",
            html_for="textarea-invalid",
        ),
        textarea(
            id="textarea-invalid",
            placeholder="Type your message here.",
            **{"aria-invalid": True},
        ),
        field.description(
            "Please enter a valid message.",
        ),
        **{"data-invalid": True},
        class_name="max-w-xs",
    )
```
