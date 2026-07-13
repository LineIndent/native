---
title: "Input"
description: "A text input component for forms and user data entry with built-in styling and accessibility features."
order: 11
---


## Input, A Text Input Component For Forms And User Data Entry With Built-In Styling And Accessibility Features.



> Error processing `usage`: module, class, method, function, traceback, frame, or code object was expected, got Input


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
from reflex.components.component import ComponentNamespace
from reflex_components_core.el import Input as BaseInput

from ..core.core import CoreComponent, cn


class ClassNames:
    INPUT = (
        "w-full file:text-foreground placeholder:text-muted-foreground "
        "selection:bg-primary selection:text-primary-foreground "
        "dark:bg-input/30 border-input "
        "h-8 w-full min-w-0 rounded-lg border bg-transparent px-3 py-1 text-base "
        "outline-none "
        "file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium "
        "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 "
        "md:text-sm "
        "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] "
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 "
        "aria-invalid:border-destructive"
    )


class InputComponent(BaseInput, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> BaseInput:

        existing_class = props.get("class_name", "")

        props["class_name"] = cn(ClassNames.INPUT, existing_class)

        props.setdefault("data_slot", "input")

        if "type" not in props:
            props["type"] = "text"

        return super().create(*children, **props)


class Input(ComponentNamespace):
    __call__ = staticmethod(InputComponent.create)
    class_name = ClassNames


input = Input()
```

# Examples

## Basic Demo

The default appearance and behavior. `type` defaults to `"text"` if not set.

**Props used:** none required beyond default `input(...)`.

```python
def input_basic_demo():
    return rx.el.div(
        rx.el.p("Text Input", class_name="text-sm font-medium mb-2"),
        input(
            type="text",
            placeholder="Enter your name",
        ),
        class_name="w-full max-w-md p-8",
    )
```

## Email

**Props used:** `type="email"` on `input`.

```python
def input_email():
    return rx.el.div(
        rx.el.p("Email Input", class_name="text-sm font-medium mb-2"),
        input(
            type="email",
            placeholder="name@example.com",
        ),
        class_name="w-full max-w-md p-8",
    )
```

## Password

**Props used:** `type="password"` on `input`.

```python
def input_password():
    return rx.el.div(
        rx.el.p("Password Input", class_name="text-sm font-medium mb-2"),
        input(
            type="password",
            placeholder="Enter your password",
        ),
        class_name="w-full max-w-md p-8",
    )
```

## Disabled

**Props used:** `disabled` on `input`.

```python
def input_disabled():
    return rx.el.div(
        rx.el.p("Disabled Input", class_name="text-sm font-medium mb-2"),
        input(
            type="text",
            placeholder="Disabled input",
            disabled=True,
        ),
        class_name="w-full max-w-md p-8",
    )
```

## File Input

Native file styling (`file:` classes) is already baked into the base input styles.

**Props used:** `type="file"` on `input`.

```python
def input_file_input():
    return rx.el.div(
        rx.el.p("File Input", class_name="text-sm font-medium mb-2"),
        input(
            type="file",
        ),
        class_name="w-full max-w-md p-8",
    )
```

## Custom Input

**Props used:** `class_name` on `input`.

```python
def input_custom_input():
    return rx.el.div(
        rx.el.p("Custom Width", class_name="text-sm font-medium mb-2"),
        input(
            type="text",
            placeholder="Max width 300px",
            class_name="max-w-[300px]",
        ),
        class_name="w-full max-w-md p-8",
    )
```

# API Reference

## input

```python
input(id="email", type="email", placeholder="you@example.com")
```

| Prop         | Type  | Default  |
| ------------ | ----- | -------- |
| `type`       | `str` | `"text"` |
| `disabled`   | `bool`| `False`  |
| `value` / `default_value` | `str` |    |
| `id`         | `str` |          |
| `name`       | `str` |          |
| `on_change`  | `EventHandler` |  |
| `class_name` | `str` | `""`     |

Any other prop accepted by a native `<input>` is also passed straight through.
