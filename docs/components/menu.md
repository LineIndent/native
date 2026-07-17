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

You have written a fantastic foundation for this markdown file. Your explicit callouts about the **Nested Interactivity Constraint** and **Layout Boundaries (Overflow Hidden)** are highly professional, real-world notes that prevent endless debugging for developers using your library.

Your reference is currently missing the rest of your sub-components (`menu.close`, `menu.separator`, `menu.group_label`, and `menu.shortcut`).

Here is the complete, fully updated API Reference adding the missing components, cleaning up the markdown formatting tables to match your style, and providing explicit composition blocks.

# API Reference

## menu.root

Instantiates a positioning context container built around a native HTML `<details>` disclosure component. Includes automated JavaScript listeners for document keydowns (Escape) and window click-away dismissals.

```python
menu.root(
    menu.trigger("Open Menu"),
    menu.content(...)
)
```

| Prop         | Type  | Default          | Description                                                           |
| ------------ | ----- | ---------------- | --------------------------------------------------------------------- |
| `id`         | `str` | _Auto-generated_ | Stable HTML identifier used for tracking open disclosure windows.     |
| `class_name` | `str` | `""`             | Additional Tailwind styles injected onto the details container block. |

## menu.trigger

> **Nested Interactivity Constraint:** Do not pass fully interactive components (like standard `button(...)` blocks) as children inside `menu.trigger`. Nesting interactive elements intercepts DOM click events and prevents the menu from opening. To style your trigger like a button, pass raw strings/icons and apply button classes directly to the trigger component.

The target control wrapper that toggles the open visibility state of the menu list container. Generates a native HTML `<summary>` element.

```python
menu.trigger("Click me")
```

| Prop         | Type  | Default | Description                                                   |
| ------------ | ----- | ------- | ------------------------------------------------------------- |
| `class_name` | `str` | `""`    | Injected class utilities for styling the outer trigger block. |

## menu.content

> **Layout Boundaries**: This component utilizes pure CSS absolute positioning instead of DOM portaling. The popup menu remains nested deep inside its localized DOM tree node. Ensure that no parent container layouts above this component enforce **overflow: hidden** or **overflow: auto** constraints, as this will physically clip or crop the floating dropdown menu box.

The relative positioning wrapper box holding the collection of links or action rows.

```python
menu.content(
    menu.item("Item 1"),
    side="bottom",
    align="start"
)
```

| Prop          | Type                                        | Default    | Description                                                           |
| ------------- | ------------------------------------------- | ---------- | --------------------------------------------------------------------- |
| `side`        | `Literal["bottom", "top", "left", "right"]` | `"bottom"` | Anchoring edge side for positioning the content box.                  |
| `side_offset` | `int`                                       | `4`        | Distance buffer (in pixels) relative to the menu trigger target.      |
| `align`       | `Literal["start", "end", "center"]`         | `"start"`  | Structural alignment offset adjustment for positioning axes.          |
| `class_name`  | `str`                                       | `""`       | Additional layout class styles applied to the floating content frame. |

## menu.item

An action selection row component. Injects a DOM traversal action snippet that walks up to collapse the parent menu immediately upon clicking.

> **Loop Context Warning:** If rendered inside an `rx.foreach`, pass an explicit `id` derived from your loop data (e.g. `id=f"menu-item-{item.id}"`) to prevent static template collisions.

```python
menu.item("Profile", variant="default", close_on_click=True)
```

| Prop             | Type                                | Default          | Description                                                               |
| ---------------- | ----------------------------------- | ---------------- | ------------------------------------------------------------------------- |
| `variant`        | `Literal["default", "destructive"]` | `"default"`      | Toggles destructive textual accents and item highlight colors.            |
| `close_on_click` | `bool`                              | `True`           | Instructs the item to close the menu container window instantly on click. |
| `id`             | `str`                               | _Auto-generated_ | Custom tracking string. Required if rendering within `rx.foreach`.        |
| `on_click`       | `Union[EventHandler, list]`         | `None`           | Trigger callbacks executed when the item row is pressed.                  |
| `class_name`     | `str`                               | `""`             | Additional item styling overrides.                                        |

## menu.close

An item selection layout button dedicated entirely to dismissing and closing the menu panel on click. Perfect for layout rows acting explicitly as "Cancel" buttons.

```python
menu.close("Cancel Action", class_name="text-center justify-center")
```

| Prop         | Type  | Default          | Description                                                              |
| ------------ | ----- | ---------------- | ------------------------------------------------------------------------ |
| `id`         | `str` | _Auto-generated_ | HTML selector element identity hook used by the internal layout manager. |
| `class_name` | `str` | `""`             | Visual styling definitions injected onto the close component row.        |

## menu.separator

A thematic breakout line used to separate distinct clusters of menu content actions horizontally.

```python
menu.separator()
```

| Prop         | Type  | Default | Description                                                       |
| ------------ | ----- | ------- | ----------------------------------------------------------------- |
| `class_name` | `str` | `""`    | Overrides for line weights or background coloring configurations. |

## menu.group_label

Renders an accessible, small, grayed-out header label row ideal for categorizing sets of items inside multi-tiered menus.

```python
menu.group_label("Workspace Actions")
```

| Prop         | Type  | Default | Description                                           |
| ------------ | ----- | ------- | ----------------------------------------------------- |
| `class_name` | `str` | `""`    | Custom labeling colors or spacing layout adjustments. |

## menu.shortcut

A right-aligned utility container used to cleanly position semantic keyboard shortcuts or button prompt hints inside a `menu.item`.

```python
menu.item(
    "Save Project",
    menu.shortcut("Ctrl + S")
)
```

| Prop         | Type  | Default | Description                                             |
| ------------ | ----- | ------- | ------------------------------------------------------- |
| `class_name` | `str` | `""`    | Custom typeface weighting or visual layout adjustments. |
