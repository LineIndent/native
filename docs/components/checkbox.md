---
title: "Checkbox"
description: "A control that allows the user to toggle between checked and not checked."
order: 5
---

--INTRO([Checkbox, A control that allows the user to toggle between checked and not checked.])--

--USAGE(checkbox)--

--SOURCE(checkbox)--

# Examples

## Basic

Pair the checkbox with `field.root` and `field.label` for proper layout and labeling. `checkbox.root`'s `id` is what `html_for` should point to.

**Props used:** `id`, `default_checked` on `checkbox.root`; `html_for` on `field.label`.

--DEMO(checkbox_basic)--

## Description

Use `field.description` for helper text underneath the label.

**Props used:** `id`, `default_checked` on `checkbox.root`; `html_for` on `field.label`.

--DEMO(checkbox_description)--

## Disabled

Use the `disabled` prop to prevent interaction — the wrapper's `has-[:disabled]` styling dims it automatically, no extra data attribute needed.

**Props used:** `id`, `disabled` on `checkbox.root`; `html_for` on `field.label`.

--DEMO(checkbox_disabled)--

## Group

Use multiple `field.root`s inside a `fieldset` to build a checkbox list.

**Props used:** `id`, `default_checked` on `checkbox.root`; `html_for` on `field.label`.

--DEMO(checkbox_group)--

# API Reference

## checkbox.root

Renders a `<label>` wrapping a visually-hidden `<input type="checkbox">` and the indicator — clicking anywhere in the root toggles it, with no extra JS wiring required.

```python
checkbox.root(
    checkbox.indicator(),
    id="terms",
    default_checked=True,
)
```

| Prop              | Type            | Default          |
| ----------------- | --------------- | ---------------- |
| `id`               | `str`           | auto-passed to input |
| `checked`          | `bool`          |                   |
| `default_checked`  | `bool`          |                   |
| `disabled`         | `bool`          | `False`           |
| `required`         | `bool`          | `False`           |
| `name`             | `str`           |                   |
| `value`            | `str`           |                   |
| `on_change`        | `EventHandler`  |                   |
| `class_name`       | `str`           | `""`              |

If no children are passed, a default `checkbox.indicator()` (tick icon) is rendered automatically.

## checkbox.indicator

The tick icon shown when the checkbox is checked, via `peer-checked:grid` — no `fallback_id`/`menu_id`-style wiring needed, it's a direct sibling of the input.

```python
checkbox.indicator(hi("Tick02Icon"))
```

| Prop         | Type  | Default              |
| ------------ | ----- | -------------------- |
| `class_name` | `str` | `""`                  |

If no children are passed, `hi("Tick02Icon")` is used by default.
