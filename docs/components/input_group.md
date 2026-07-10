---
title: "Input Group"
description: "Add addons, buttons, and helper content to inputs."
order: 0
---

--INTRO([Input Group, Add addons, buttons, and helper content to inputs.])--

--USAGE(input_group)--

--SOURCE(input_group)--

# Align

Use `align` on `input_group.addon` to position it relative to the input.

> For proper focus management, `input_group.addon` should always be placed **after** `input_group.input` or `input_group.textarea` in the DOM. Use `align` to visually position it instead of reordering the DOM.

## inline-start

The default — positions the addon at the start of the input.

**Props used:** `align="inline-start"` on `input_group.addon`.

--DEMO(input_group_inline_start)--

## inline-end

**Props used:** `align="inline-end"` on `input_group.addon`.

--DEMO(input_group_inline_end)--

## block-start

Positions the addon above the input — typically used with `input_group.textarea`.

**Props used:** `align="block-start"` on `input_group.addon`.

--DEMO(input_group_block_start)--

## block-end

**Props used:** `align="block-end"` on `input_group.addon`.

--DEMO(input_group_block_end)--

# Examples

## Icons

**Props used:** `align` on `input_group.addon`.

--DEMO(input_group_icons)--

## Text

**Props used:** none required beyond default `input_group.text` composition.

--DEMO(input_group_text)--

## Button

**Props used:** `size` on `input_group.button`.

--DEMO(input_group_button)--

## Spinner

**Props used:** `align` on `input_group.addon`.

--DEMO(input_group_spinner)--

## Dropdown

**Props used:** see the [Menu](/docs/components/menu) docs for menu-specific props.

--DEMO(input_group_dropdown)--

# API Reference

## input_group.root

The main wrapper around inputs and addons.

```python
input_group.root(
    input_group.addon(hi("Search01Icon")),
    input_group.input(placeholder="Search..."),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## input_group.addon

Displays icons, text, buttons, or other content alongside the input. Can contain multiple `input_group.button`s.

```python
input_group.addon(hi("Search01Icon"), align="inline-start")
```

| Prop         | Type                                                                     | Default          |
| ------------ | --------------------------------------------------------------------------| ---------------- |
| `align`      | `Literal["inline-start", "inline-end", "block-start", "block-end"]`      | `"inline-start"` |
| `class_name` | `str`                                                                     | `""`              |

Use `inline-start`/`inline-end` with `input_group.input`, and `block-start`/`block-end` with `input_group.textarea`.

## input_group.button

A `button` pre-styled for input group contexts. See the [Button](/docs/components/button) docs for the rest of `button`'s props.

```python
input_group.addon(
    input_group.button(hi("X01Icon"), aria_label="Clear"),
    align="inline-end",
)
```

| Prop         | Type                                                                          | Default   |
| ------------ | -------------------------------------------------------------------------------| --------- |
| `size`       | `Literal["xs", "icon-xs", "sm", "icon-sm"]`                                   | `"xs"`    |
| `variant`    | `Literal["default", "destructive", "outline", "secondary", "ghost", "link"]` | `"ghost"` |
| `class_name` | `str`                                                                          | `""`      |

## input_group.input

Drop-in replacement for `input()` inside an input group — pre-styled and tagged with the shared `data-slot="input-group-control"` used for group-wide focus states.

```python
input_group.input(placeholder="Search...")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

Any other prop accepted by `input()` is passed straight through.

## input_group.textarea

Drop-in replacement for `textarea()` inside an input group — same `data-slot="input-group-control"` convention as `input_group.input`.

```python
input_group.textarea(placeholder="Leave a comment...")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

Any other prop accepted by `textarea()` is passed straight through.
