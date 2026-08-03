---
title: "Collapsible"
description: "An interactive component which expands/collapses a panel."
order: 0
---


## Collapsible, An Interactive Component Which Expands/Collapses A Panel. 


```python
from components.ui.collapsible import collapsible
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
from reflex.components.component import Component, ComponentNamespace
from reflex_components_core.el import Div

from ..core.core import CoreComponent


class ClassNames:
    ROOT = "flex flex-col justify-center text-secondary-12"
    TRIGGER = (
        "flex items-center gap-2 cursor-pointer select-none list-none rounded-md "
        "marker:content-none [&::-webkit-details-marker]:hidden "
        "[details[open]>&]:bg-muted/50"
    )
    PANEL = "text-sm"


class CollapsibleRoot(CoreComponent):
    @classmethod
    def create(cls, *children, default_open: bool = False, **props) -> Component:
        props["data-slot"] = "collapsible"
        if default_open:
            props.setdefault("open", True)
        cls.set_class_name(ClassNames.ROOT, props)
        return rx.el.details(*children, **props)


class CollapsibleTrigger(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Component:
        props["data-slot"] = "collapsible-trigger"
        cls.set_class_name(ClassNames.TRIGGER, props)
        return rx.el.summary(*children, **props)


class CollapsiblePanel(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        props["data-slot"] = "collapsible-panel"
        cls.set_class_name(ClassNames.PANEL, props)
        return super().create(*children, **props)


class Collapsible(ComponentNamespace):
    root = staticmethod(CollapsibleRoot.create)
    trigger = staticmethod(CollapsibleTrigger.create)
    panel = staticmethod(CollapsiblePanel.create)
    class_names = ClassNames


collapsible = Collapsible()
```

# Examples

## Basic

Built on native `<details>`/`<summary>`, expand/collapse and keyboard support come from the browser, no JS required. The chevron rotation and open-state highlight use a structural selector (`[details[open]>&]`) rather than Tailwind's `group-open:`, since `group-open:` matches _any_ open ancestor rather than the nearest one — harmless here, but matters once collapsibles nest (see below).

**Props used:** `default_open` on `collapsible.root` (starts the panel expanded).

```python
def collapsible_basic() -> rx.Component:
    return rx.el.div(
        collapsible.root(
            collapsible.trigger(
                rx.el.div(
                    rx.el.p("How do I update my billing information?"),
                    hi(
                        "ArrowDown01Icon",
                        class_name="size-4 ml-auto [details[open]>summary_&]:rotate-180",
                    ),
                    class_name="w-full flex flex-row items-center justify-between",
                ),
                class_name=cn(
                    "w-full py-3 text-left border-b border-input",
                    button_variants(variant="ghost"),
                ),
            ),
            collapsible.panel(
                rx.el.div(
                    "You can update your card details directly inside your account settings dashboard under the billing tab.",
                    class_name="py-3 text-sm text-muted-foreground leading-relaxed px-3",
                ),
            ),
            default_open=False,
        ),
        class_name="w-full max-w-sm",
    )
```

## Nested

Collapsibles nest freely, each `<details>` is fully independent, so there's no coordination needed between levels (multiple folders can be open at once). The one thing that _does_ need care when nesting: chevron/highlight styling must use the structural `[details[open]>...]` selector, not `group-open:`. `group-open:` would match an open ancestor several folders up, which makes every icon inside it look rotated even if that specific folder is still closed.

**Props used:** none beyond `collapsible.root` / `collapsible.trigger` / `collapsible.panel` — the tree is just `folder_item` calling itself recursively.

```python
def collapsible_nested() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "WORKSPACE EXPLORER",
                class_name="text-[10px] font-bold tracking-wider text-muted-foreground",
            ),
            class_name="px-2 pb-2 mb-1 border-b border-border/40",
        ),
        folder_item(
            "src",
            folder_item(
                "components",
                folder_item(
                    "ui",
                    file_item("button.py"),
                    file_item("card.py"),
                    file_item("collapsible.py"),
                ),
                file_item("navbar.py"),
                file_item("sidebar.py"),
            ),
            folder_item(
                "state",
                file_item("base_state.py"),
                file_item("auth_state.py"),
            ),
            file_item("main.py"),
        ),
        folder_item(
            "public",
            file_item("favicon.ico"),
            file_item("logo.svg"),
        ),
        file_item("rxconfig.py", root_level=True),
        file_item("requirements.txt", root_level=True),
        class_name="w-full max-w-xs p-3 bg-background border border-input rounded-xl shadow-xs select-none",
    )
```

# API Reference

## collapsible.root

Renders a native `<details>` element. `default_open` sets the initial `open` attribute on first render. Since it's a real `<details>`, controlled usage also works without any extra plumbing — pass `open=State.is_open` and `on_toggle=State.handle_toggle` to drive or react to it from Reflex state, same as any other native attribute/event.

```python
collapsible.root(
    collapsible.trigger(...),
    collapsible.panel(...),
    default_open=False,
)
```

| Prop           | Type           | Default |
| -------------- | -------------- | ------- |
| `default_open` | `bool`         | `False` |
| `open`         | `bool`         | `None`  |
| `on_toggle`    | `EventHandler` | `None`  |
| `class_name`   | `str`          | `""`    |

## collapsible.trigger

Renders a `<summary>`. Unlike a typical accordion trigger, it doesn't append a chevron for you — pass your own icon (and any other trigger content) as children, and drive its rotation off the parent's open state yourself.

```python
collapsible.trigger(
    rx.el.p("How do I update my billing information?"),
    hi("ArrowDown01Icon", class_name="[details[open]>summary_&]:rotate-180"),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## collapsible.panel

```python
collapsible.panel(
    "You can update your card details directly inside your account settings dashboard.",
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## Styling based on open state

`collapsible.root` renders the actual `<details>`, so any open-state styling on the trigger or its children should key off that element directly rather than a Tailwind `group`:

| Target                                      | Selector                               |
| ------------------------------------------- | -------------------------------------- |
| The trigger itself (e.g. a highlight)       | `[details[open]>&]:bg-muted/50`        |
| Something inside the trigger (e.g. an icon) | `[details[open]>summary_&]:rotate-180` |

Both are scoped to _that_ collapsible's own `<details>` — never a distant open ancestor — which is what makes them safe to reuse inside recursively nested collapsibles like the file-tree example above.
