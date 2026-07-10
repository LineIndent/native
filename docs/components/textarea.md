---
title: "Textarea"
description: "Displays a form textarea or a component that looks like a textarea."
order: 23
---

--INTRO([Textarea, Displays a form textarea or a component that looks like a textarea.])--

--USAGE(textarea)--

--SOURCE(textarea)--

# Examples

## Basic

A standard multiline text input. Auto-grows with content via `field-sizing-content`.

**Props used:** none required beyond default `textarea(...)`.

--DEMO(textarea_basic_demo)--

## Field

Pair with `field.root`, `field.label`, and `field.description` for a structured, labeled field.

**Props used:** `id` on `textarea`; `html_for` on `field.label`.

--DEMO(textarea_field)--

## Disabled

Use `disabled` on `textarea`. Add `data_invalid`/disabled state to `field.root` to propagate consistent visual styling across the label and description too.

**Props used:** `disabled` on `textarea`.

--DEMO(textarea_disabled)--

## Invalid

Use `aria_invalid` on `textarea` to mark it invalid, and `data_invalid="true"` on `field.root` to style the whole field block accordingly.

**Props used:** `aria_invalid` on `textarea`; `data_invalid` on `field.root`.

--DEMO(textarea_invalid)--

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
