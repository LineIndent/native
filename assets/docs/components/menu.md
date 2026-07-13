---
title: "Menu"
description: "Displays a menu to the user — such as a set of actions or functions — triggered by a button."
order: 0
---


## Menu, Displays A Menu To The User — Such As A Set Of Actions Or Functions — Triggered By A Button.


```python
from components.ui.menu import Menu
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
import itertools

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn

_menu_id_counter = itertools.count()
_menu_item_counter = itertools.count()


class ClassNames:
    TRIGGER = "inline-block list-none cursor-pointer [&::-webkit-details-marker]:hidden"
    TRIGGER_INNER = "flex w-fit items-center"
    CONTENT = (
        "absolute z-50 min-w-32 rounded-lg bg-popover p-1 text-popover-foreground "
        "shadow-md ring-1 ring-foreground/10 outline-none"
    )
    ITEM = (
        "group/menu-item relative flex cursor-default items-center gap-1.5 "
        "rounded-lg px-1.5 py-1 text-sm outline-hidden select-none "
        "hover:bg-accent hover:text-accent-foreground "
        "data-[variant=destructive]:text-destructive "
        "data-[variant=destructive]:hover:bg-destructive/10 "
        "data-[variant=destructive]:hover:text-destructive "
        "data-disabled:pointer-events-none data-disabled:opacity-50 "
        "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4"
    )
    SEPARATOR = "-mx-1 my-1 h-px bg-border"
    GROUP_LABEL = "px-1.5 py-1 text-xs font-medium text-muted-foreground"
    SHORTCUT = "ml-auto text-xs tracking-widest text-muted-foreground"
    SIDE_OFFSETS = {
        "bottom": "top-full",
        "top": "bottom-full",
        "right": "left-full",
        "left": "right-full",
    }


class MenuRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props.setdefault("id", f"menu-{next(_menu_id_counter)}")
        props["data-slot"] = "menu"
        cls.set_class_name("relative inline-block", props)

        props["on_mount"] = rx.call_script(
            """
            if (!window.__menuGlobalHandlersAttached) {
                window.__menuGlobalHandlersAttached = true;

                document.addEventListener('keydown', function (e) {
                    if (e.key === 'Escape') {
                        document
                            .querySelectorAll('details[data-slot="menu"][open]')
                            .forEach(function (el) { el.open = false; });
                    }
                });

                document.addEventListener('click', function (e) {
                    document
                        .querySelectorAll('details[data-slot="menu"][open]')
                        .forEach(function (el) {
                            if (!el.contains(e.target)) {
                                el.open = false;
                            }
                        });
                });
            }
            """
        )

        return rx.el.details(*children, **props)


class MenuTrigger(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "menu-trigger"
        cls.set_class_name(ClassNames.TRIGGER, props)
        return rx.el.summary(
            rx.el.div(*children, class_name=ClassNames.TRIGGER_INNER),
            **props,
        )


class MenuContent(CoreComponent):
    @classmethod
    def create(
        cls,
        *children,
        side: str = "bottom",
        side_offset: int = 4,
        align: str = "start",
        **props,
    ) -> rx.Component:
        props["data-slot"] = "menu-content"
        props["data-side"] = side

        margin_key = {
            "bottom": "marginTop",
            "top": "marginBottom",
            "left": "marginRight",
            "right": "marginLeft",
        }.get(side, "marginTop")
        props["style"] = {margin_key: f"{side_offset}px", **props.get("style", {})}

        position_class = ClassNames.SIDE_OFFSETS.get(side, "top-full")
        align_class = {
            "start": "left-0",
            "end": "right-0",
            "center": "left-1/2 -translate-x-1/2",
        }.get(align, "left-0")

        cls.set_class_name(cn(ClassNames.CONTENT, position_class, align_class), props)
        return rx.el.div(*children, **props)


class MenuItem(CoreComponent):
    """
    Note: if rendered inside rx.foreach, the auto-generated sequential ID is baked in
    once at template-build time and shared across all rendered items. Pass
    an explicit `id` derived from your loop data in that case, e.g.
    id=f"menu-item-{item.id}".
    """

    @classmethod
    def create(cls, *children, close_on_click: bool = True, **props) -> rx.Component:
        props["data-slot"] = "menu-item"
        cls.set_class_name(ClassNames.ITEM, props)

        # 0. Pop out the variant prop so we can apply the data-variant attribute
        variant = props.pop("variant", "default")
        props["data-variant"] = variant  # This maps to your Tailwind: data-[variant=destructive]

        item_id = props.get("id") or f"menu-item-{next(_menu_item_counter)}"
        props["id"] = item_id

        # 1. Pop out any existing user on_click triggers
        user_on_click = props.pop("on_click", None)
        click_events = []

        # 2. Append the user's custom event(s) if they provided any
        if user_on_click is not None:
            if isinstance(user_on_click, list):
                click_events.extend(user_on_click)
            else:
                click_events.append(user_on_click)

        # 3. If close_on_click is active, append the parent-closing script
        if close_on_click:
            close_script = rx.call_script(
                f"""
                const item = document.getElementById('{item_id}');
                const root = item ? item.closest('[data-slot="menu"]') : null;
                if (root) root.open = false;
                """
            )
            click_events.append(close_script)

        # 4. Bind the combined chain back to props if there's anything to execute
        if click_events:
            props["on_click"] = click_events

        return rx.el.div(*children, **props)


class MenuClose(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "menu-close"
        props.setdefault("type", "button")

        close_id = props.get("id") or f"menu-item-{next(_menu_item_counter)}"
        props["id"] = close_id

        props["on_click"] = rx.call_script(
            f"""
            const btn = document.getElementById('{close_id}');
            const root = btn ? btn.closest('[data-slot="menu"]') : null;
            if (root) root.open = false;
            """
        )

        cls.set_class_name(ClassNames.ITEM, props)
        return rx.el.div(*children, **props)


class MenuSeparator(CoreComponent):
    @classmethod
    def create(cls, **props) -> rx.Component:
        props["data-slot"] = "menu-separator"
        cls.set_class_name(ClassNames.SEPARATOR, props)
        return rx.el.div(**props)


class MenuGroupLabel(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "menu-group-label"
        cls.set_class_name(ClassNames.GROUP_LABEL, props)
        return rx.el.div(*children, **props)


class MenuShortcut(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "menu-shortcut"
        cls.set_class_name(ClassNames.SHORTCUT, props)
        return rx.el.span(*children, **props)


class Menu(ComponentNamespace):
    root = staticmethod(MenuRoot.create)
    trigger = staticmethod(MenuTrigger.create)
    content = staticmethod(MenuContent.create)
    item = staticmethod(MenuItem.create)
    close = staticmethod(MenuClose.create)
    separator = staticmethod(MenuSeparator.create)
    group_label = staticmethod(MenuGroupLabel.create)
    shortcut = staticmethod(MenuShortcut.create)
    class_names = ClassNames


menu = Menu()
```

# Examples

## Basic

A clean dropdown menu with organizational group labels and visual dividers.

**Props used:** None.

```python
def menu_basic() -> rx.Component:
    return menu.root(
        menu.trigger("Open Menu", class_name=button_variants(variant="outline")),
        menu.content(
            menu.group_label("My Account"),
            menu.item("Profile"),
            menu.item("Billing"),
            menu.item("Settings"),
        )
    )
```

## Shortcuts

Dropdown items with right-aligned keyboard command hints built into the row layout.

**Props used:** `menu.shortcut` as a child wrapper element.

```python
def menu_shortcuts() -> rx.Component:
    return menu.root(
        menu.trigger("Workspace Actions Menu", class_name=button_variants(variant="outline")),
        menu.content(
            menu.item("New Tab", menu.shortcut("⌘T")),
            menu.item("New Window", menu.shortcut("⌘N")),
            menu.separator(),
            menu.item("Save Project", menu.shortcut("⌘S")),
        )
    )
```

## Icons

Row entries decorated with left-side action icons for clean visual scanning.

**Props used:** `hi <hugeicon>` as an inline child prefix element.

```python
def menu_icons() -> rx.Component:
    return menu.root(
        menu.trigger("Options", class_name=button_variants(variant="outline")),
        menu.content(
            menu.item(hi("UserIcon"), "Profile"),
            menu.item(hi("CreditCardIcon"), "Billing"),
            menu.item(hi("Setting07Icon"), "Settings"),
        )
    )
```

## Destructive

Incorporate warning styles into individual items for irreversible actions.

**Props used:** `variant="destructive"` on `menu.item`.

```python
def menu_destructive() -> rx.Component:
    return menu.root(
        menu.trigger("Danger Zone", class_name=button_variants(variant="outline")),
        menu.content(
            menu.item("Account Settings"),
            menu.separator(),
            menu.item("Delete Repository", variant="destructive"),
            class_name="w-[10rem]"
        )
    )
```

# API Reference

## menu.root

Instantiates a positioning context container built around a native HTML `<details>` disclosure component. Includes automated JavaScript listeners for document keydowns (Escape) and window click-away dismissals.

```python
menu.root(
    menu.trigger(...),
    menu.content(...)
)
```

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `id` | `str` | *Auto-generated* | Stable HTML identifier used for tracking open disclosure windows. |
| `class_name` | `str` | `""` | Additional Tailwind styles injected onto the details container block. |

## menu.trigger

> **Nested Interactivity Constraint:** Do not pass fully interactive components (like standard `button(...)` blocks) as children inside `menu.trigger`. Nesting interactive elements intercepts DOM click events and prevents the menu from opening. To style your trigger like a button, pass raw strings/icons and apply button classes directly to the trigger component.

The target control wrapper that toggles the open visibility state of the menu list container. Generates a native HTML `<summary>` element.

```python
menu.trigger(button("Open"))
```

## menu.content

> **Layout Boundaries**: This component utilizes pure CSS absolute positioning instead of DOM portaling. The popup menu remains nested deep inside its localized DOM tree node. Ensure that no parent container layouts above this component enforce **overflow: hidden** or **overflow: auto** constraints, as this will physically clip or crop the floating dropdown menu box.

The relative positioning wrapper box holding the collection of links or action rows.

```python
menu.content(..., side="bottom", align="start")
```

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `side` | `Literal["bottom", "top", "left", "right"]` | `"bottom"` | Anchoring edge side for positioning the content box. |
| `side_offset` | `int` | `4` | Distance buffer (in pixels) relative to the menu trigger target. |
| `align` | `Literal["start", "end", "center"]` | `"start"` | Structural alignment offset adjustment for positioning axes. |

## menu.item

An action selection row component. Injects a DOM traversal action snippet that walks up to collapse the parent menu immediately upon clicking.

```python
menu.item("Profile Item", variant="default", close_on_click=True)
```

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `variant` | `Literal["default", "destructive"]` | `"default"` | Toggles destructive textual accents and item highlight colors. |
| `close_on_click` | `bool` | `True` | Instructs the item to close the menu container window instantly on click. |
| `id` | `str` | *Auto-generated* | Custom tracking string. Required if rendering within `rx.foreach`. |
| `on_click` | `EventHandler` |  | Trigger callback executed instantly when the item is pressed. |
