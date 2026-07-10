---
title: "Button Group"
description: "A container that groups related buttons together with consistent styling."
order: 3
---

--INTRO([Button Group, A container that groups related buttons together with consistent styling.])--

--USAGE(button_group)--

--SOURCE(button_group)--

# Accessibility

- `button_group.root` sets `role="group"`.
- Use `Tab` to navigate between the buttons in the group.
- Use `aria-label` or `aria-labelledby` to label the button group.

# Examples

## Orientation

Set the `orientation` prop to change the layout.

**Props used:** `orientation` on `button_group.root`.

--DEMO(button_group_orientation)--

## Size

Control the size of buttons using the `size` prop on individual buttons.

**Props used:** `size` on `button`.

--DEMO(button_group_size)--

## Separator

`button_group.separator` visually divides buttons within a group. `outline`-variant buttons don't need one (they already have a border) — other variants benefit from it for visual hierarchy.

**Props used:** none required beyond default `button_group.separator`.

--DEMO(button_group_separator)--

## Split

Two buttons separated by a `button_group.separator`.

**Props used:** none required beyond default `button_group.separator`.

--DEMO(button_group_split)--

## Input

Wrap an `input` with buttons on either side.

**Props used:** none required — standard `button_group.root` composition.

--DEMO(button_group_input)--

## Dropdown Menu

A split button group with a `menu` as the second segment.

**Props used:** see the [Menu](/docs/components/menu) docs for menu-specific props.

--DEMO(button_group_dropdown)--

## Select

Pair with a `select` component.

**Props used:** see the [Select](/docs/components/select) docs for select-specific props.

--DEMO(button_group_select)--

# API Reference

## button_group.root

```python
button_group.root(
    button("Copy", variant="outline"),
    button("Paste", variant="outline"),
)
```

| Prop          | Type                                 | Default        |
| ------------- | -------------------------------------- | -------------- |
| `orientation` | `Literal["horizontal", "vertical"]`   | `"horizontal"` |
| `class_name`  | `str`                                  | `""`            |

## button_group.separator

```python
button_group.root(
    button("Bold", variant="ghost"),
    button_group.separator(),
    button("Italic", variant="ghost"),
)
```

| Prop          | Type                                 | Default      |
| ------------- | -------------------------------------- | ------------ |
| `orientation` | `Literal["horizontal", "vertical"]`   | `"vertical"` |
| `class_name`  | `str`                                  | `""`          |

## button_group.text

Accepts `*children`, so any component (including interactive ones) can be rendered as label content inside a group.

```python
button_group.text("Filter by")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |
