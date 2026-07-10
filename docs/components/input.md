---
title: "Input"
description: "A text input component for forms and user data entry with built-in styling and accessibility features."
order: 11
---

--INTRO([Input, A text input component for forms and user data entry with built-in styling and accessibility features.])--

--USAGE(input)--

--SOURCE(input)--

# Examples

## Basic Demo

The default appearance and behavior. `type` defaults to `"text"` if not set.

**Props used:** none required beyond default `input(...)`.

--DEMO(input_basic_demo)--

## Email

**Props used:** `type="email"` on `input`.

--DEMO(input_email)--

## Password

**Props used:** `type="password"` on `input`.

--DEMO(input_password)--

## Disabled

**Props used:** `disabled` on `input`.

--DEMO(input_disabled)--

## File Input

Native file styling (`file:` classes) is already baked into the base input styles.

**Props used:** `type="file"` on `input`.

--DEMO(input_file_input)--

## Custom Input

**Props used:** `class_name` on `input`.

--DEMO(input_custom_input)--

# API Reference

## input

```python
input(id="email", type="email", placeholder="you@example.com")
```

| Prop         | Type  | Default  |
| ------------ | ----- | -------- |
| `type`       | `str` | `"text"` |
| `disabled`   | `bool`| `False`  |
| `value` / `default_value` | `str` |    |
| `id`         | `str` |          |
| `name`       | `str` |          |
| `on_change`  | `EventHandler` |  |
| `class_name` | `str` | `""`     |

Any other prop accepted by a native `<input>` is also passed straight through.
