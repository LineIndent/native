---
title: "Separator"
description: "Visually or semantically separates content."
order: 0
---

--INTRO([Separator, Visually or semantically separates content.])--

--USAGE(separator)--

--SOURCE(separator)--

# Examples

## Default

The default `orientation` is `"horizontal"`.

**Props used:** none required — `orientation="horizontal"` is the default.

--DEMO(separator_horizontal)--

## Vertical

**Props used:** `orientation="vertical"` on `separator`.

--DEMO(separator_vertical)--

## Menu

Vertical separators between menu items with descriptions.

**Props used:** `orientation="vertical"` on `separator`.

--DEMO(separator_menu)--

## List

Horizontal separators between list items.

**Props used:** none required — `orientation="horizontal"` is the default.

--DEMO(separator_list)--

# API Reference

## separator

```python
separator(orientation="vertical")
```

| Prop          | Type                                 | Default        |
| ------------- | -------------------------------------- | -------------- |
| `orientation` | `Literal["horizontal", "vertical"]`   | `"horizontal"` |
| `decorative`  | `bool`                                 | `True`         |
| `class_name`  | `str`                                  | `""`            |

When `decorative=True` (the default), `aria-hidden="true"` is set — the separator is treated as purely visual. Set `decorative=False` to render it as a semantic `role="separator"` for assistive technology instead.
