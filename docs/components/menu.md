---
title: "Menu"
description: "Displays a menu to the user — such as a set of actions or functions — triggered by a button."
order: 0
---

--INTRO([Menu, Displays a menu to the user — such as a set of actions or functions — triggered by a button.])--

--USAGE(menu)--

--SOURCE(menu)--

# Examples

## Basic

A clean dropdown menu with organizational group labels and visual dividers.

**Props used:** None.

--DEMO(menu_basic)--

## Shortcuts

Dropdown items with right-aligned keyboard command hints built into the row layout.

**Props used:** `menu.shortcut` as a child wrapper element.

--DEMO(menu_shortcuts)--

## Icons

Row entries decorated with left-side action icons for clean visual scanning.

**Props used:** `hi <hugeicon>` as an inline child prefix element.

--DEMO(menu_icons)--

## Destructive

Incorporate warning styles into individual items for irreversible actions.

**Props used:** `variant="destructive"` on `menu.item`.

--DEMO(menu_destructive)--

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
