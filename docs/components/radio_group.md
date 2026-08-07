---
title: "Radio Group"
description: "A set of checkable buttons—known as radio buttons—where no more than one of the buttons can be checked at a time."
order: 0
---

--INTRO([Radio Group, A set of checkable buttons—known as radio buttons—where no more than one of the buttons can be checked at a time.])--

--USAGE(radio_group)--

--SOURCE(radio_group)--

# Examples

## Description

Radio group items with a description using the `Field` component.

--DEMO(radio_group_description)--

## Choice Card

Use `field.label` to wrap the entire `Field` for a clickable card-style selection.

--DEMO(radio_group_choice_card)--

## Fieldset

Use `field.set` and `field.legend` to group radio items with a label and description.

--DEMO(radio_group_fieldset)--

## Disabled

Use the `disabled` prop on `radio.root` to disable all items.

--DEMO(radio_group_disabled)--

## Invalid

Use `aria-invalid` on `radio.item` and `data-invalid` on `field.root` to show validation errors.

--DEMO(radio_group_invalid)--

# API Reference

## radio_group.root

The container element for a set of radio options. Renders a native `<fieldset role="radiogroup">`. Setting `disabled=True` on the root automatically disables all descendant radio controls without needing to set it on each item individually.

```python
radio_group.root(
    radio_group.item(name="plan", value="free", id_="plan-free"),
    radio_group.item(name="plan", value="pro", id_="plan-pro"),
    disabled=False,
)
```

| Prop         | Type   | Default         |
| ------------ | ------ | --------------- |
| `disabled`   | `bool` | `False`         |
| `class_name` | `str`  | `""`            |
| `data_slot`  | `str`  | `"radio-group"` |
| `role`       | `str`  | `"radiogroup"`  |

Any additional HTML props passed to `radio_group.root` are forwarded directly to the underlying `<fieldset>`.

## radio_group.item

Represents an individual radio control wrapped in a native `<label>`. Automatically extracts native form input attributes (`name`, `value`, `checked`, `disabled`, `aria-*`, `data-*`, etc.) and attaches them to an internal sr-only `<input type="radio">`. If no children are passed, it automatically renders a `radio_group.indicator`.

```python
radio_group.item(
    name="framework",
    value="reflex",
    id_="framework-reflex",
    default_checked=True,
)
```

| Prop              | Type   | Default              |
| ----------------- | ------ | -------------------- |
| `name`            | `str`  | _(required)_         |
| `value`           | `str`  | _(required)_         |
| `id` / `id_`      | `str`  |                      |
| `checked`         | `bool` |                      |
| `default_checked` | `bool` |                      |
| `disabled`        | `bool` | `False`              |
| `required`        | `bool` | `False`              |
| `class_name`      | `str`  | `""`                 |
| `data_slot`       | `str`  | `"radio-group-item"` |

Event handlers (e.g., `on_change`, `on_click`), accessibility attributes (`aria_*`), and state attributes (`data_*`) are automatically routed to the inner `<input>`.

## radio_group.indicator

Renders the visual selection state inside the radio item. Controlled purely via peer CSS rules (`peer-checked`). If called without children, it defaults to rendering a centered styled dot (`ITEM_INDICATOR_DOT`).

```python
radio_group.indicator()

radio_group.indicator(
    rx.el.span(class_name="size-2 rounded-full bg-accent")
)
```

| Prop         | Type  | Default                        |
| ------------ | ----- | ------------------------------ |
| `class_name` | `str` | `""`                           |
| `data_slot`  | `str` | `"radio-group-item-indicator"` |
