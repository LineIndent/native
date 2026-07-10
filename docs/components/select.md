---
title: "Select"
description: "A styled native HTML select element with consistent design system integration."
order: 13
---

--INTRO([Select, A styled native HTML select element with consistent design system integration.])--

--USAGE(select)--

--SOURCE(select)--

# Examples

## Basic

A single native `<select>` paired with a `field.label`. Uses `wrapper_class_name` to stretch the select to the full width of its container.

**Props used:** `id`, `name`, `default_value`, `wrapper_class_name` on `select`; `value` on `select.option`; `html_for` on `field.label`.

--DEMO(select_basic)--

## Grouped options

Options organized under `select.optgroup` headings, with a disabled, hidden first option acting as a placeholder — the standard way to show placeholder text in a native select without a real empty value being selectable.

**Props used:** `label` on `select.optgroup`; `value`, `disabled`, `hidden` on `select.option`; `id`, `name`, `default_value`, `wrapper_class_name` on `select`.

--DEMO(select_optgroup)--

## Sizes

Two size variants side by side — `sm` for compact layouts (toolbars, table cells) and the `default` size for standalone form fields.

**Props used:** `size`, `default_value` on `select`; `value` on `select.option`.

--DEMO(select_sizes)--

## Form layout

Two selects grouped under a shared `field.set` with a `field.legend`, showing how selects compose inside a larger form section.

**Props used:** `id`, `name`, `default_value`, `wrapper_class_name` on `select`; `value` on `select.option`; `html_for` on `field.label`.

--DEMO(select_form)--

## Disabled

A disabled select with a `field.description` explaining why it's locked. Disabling cascades visually to the whole control via the wrapper's `has-[select:disabled]` styling.

**Props used:** `id`, `default_value`, `disabled`, `wrapper_class_name` on `select`; `value` on `select.option`.

--DEMO(select_disabled)--

# API Reference
 
## select
 
The main select component. Calling `select(...)` directly renders the native `<select>` wrapped in a positioning `div` with the chevron icon — `select` is itself callable (via `NativeSelect.__call__`), so no separate `.root` is needed.
 
```python
select(
    select.option("Option 1", value="option1"),
    select.option("Option 2", value="option2"),
)
```
 
| Prop                 | Type                    | Default          |
| -------------------- | ----------------------- | ---------------- |
| `size`                | `Literal["default", "sm"]` | `"default"`   |
| `wrapper_class_name`  | `str`                   | `""`              |
| `class_name`          | `str`                   | `""`              |
| `data_slot`           | `str`                   | `"native-select"` |
| `disabled`            | `bool`                  | `False`           |
| `value` / `default_value` | `str`               |                   |
| `name`                | `str`                   |                   |
| `id`                  | `str`                   |                   |
| `on_change`           | `EventHandler`          |                   |
 
Any other prop accepted by a native HTML `<select>` (`required`, `aria-invalid`, etc.) is also passed straight through.
 
## select.option
 
Represents an individual option within the select.
 
```python
select.option("Apple", value="apple")
select.option("Sold out", value="oos", disabled=True)
```
 
| Prop       | Type   | Default |
| ---------- | ------ | ------- |
| `value`    | `str`  |         |
| `disabled` | `bool` | `False` |
| `hidden`   | `bool` | `False` |
 
## select.optgroup
 
Groups related options together under a labeled heading.
 
```python
select.optgroup(
    select.option("Apple", value="apple"),
    select.option("Banana", value="banana"),
    label="Fruits",
)
```
 
| Prop       | Type   | Default |
| ---------- | ------ | ------- |
| `label`    | `str`  |         |
| `disabled` | `bool` | `False` |
