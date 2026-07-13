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

A standard multiline text input. Auto-grows with content via `field-sizing-content`.

**Props used:** none required beyond default `textarea(...)`.

```python
def textarea_basic_demo():
    return textarea(placeholder="Type your message here.", class_name="max-w-xs")
```

## Field

Pair with `field.root`, `field.label`, and `field.description` for a structured, labeled field.

**Props used:** `id` on `textarea`; `html_for` on `field.label`.

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

Use `disabled` on `textarea`. Add `data_invalid`/disabled state to `field.root` to propagate consistent visual styling across the label and description too.

**Props used:** `disabled` on `textarea`.

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

Use `aria_invalid` on `textarea` to mark it invalid, and `data_invalid="true"` on `field.root` to style the whole field block accordingly.

**Props used:** `aria_invalid` on `textarea`; `data_invalid` on `field.root`.

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

# API Reference

## textarea

Native browser autocomplete/spellcheck attributes are disabled by default (`autoComplete`, `autoCapitalize`, `autoCorrect`, `spellCheck`) — override via `custom_attrs` if you want them back for a specific field.

```python
textarea(id="comment", placeholder="Leave a comment...")
```

| Prop         | Type   | Default |
| ------------ | ------ | ------- |
| `disabled`   | `bool` | `False` |
| `aria_invalid` | `bool` | `False` |
| `value` / `default_value` | `str` |  |
| `id`         | `str`  |         |
| `name`       | `str`  |         |
| `on_change`  | `EventHandler` |  |
| `class_name` | `str`  | `""`    |

Any other prop accepted by a native `<textarea>` is also passed straight through.
