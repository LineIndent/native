---
title: "Badge"
description: "Displays a badge or a component that looks like a badge."
order: 2
---

--INTRO([Badge, Displays a badge or a component that looks like a badge.])--

--USAGE(badge)--

--SOURCE(badge)--

# Examples

## Variants

Use the `variant` prop to change the badge's style.

**Props used:** `variant` on `badge`.

--DEMO(badge_with_variants)--

## With Icons

Render an icon inside the badge. Add `data-icon="inline-start"` or `data-icon="inline-end"` to the icon to position it correctly (adjusts padding automatically).

**Props used:** `data_icon` on the icon child.

--DEMO(badge_with_icon)--

## With Spinner

Render a `spinner` inside the badge — same `data-icon` positioning convention as icons.

**Props used:** `data_icon` on the spinner child.

--DEMO(badge_with_spinner)--

## Link

Pass `rx.el.a` as the badge's child to turn it into a link. `badge` accepts `*children`, so any interactive element works.

**Props used:** none required — pass `rx.el.a(...)` as a child.

--DEMO(badge_as_link)--

## Custom Colors

Override colors by passing extra classes via `class_name`.

**Props used:** `class_name` on `badge`.

--DEMO(badge_custom_colors)--

# API Reference

## badge

```python
badge("New", variant="secondary")
```

| Prop         | Type                                                                                   | Default     |
| ------------ | --------------------------------------------------------------------------------------- | ----------- |
| `variant`    | `Literal["default", "secondary", "destructive", "outline", "ghost", "link"]`           | `"default"` |
| `class_name` | `str`                                                                                    | `""`        |

Any other prop accepted by a native `<span>` is also passed straight through.
