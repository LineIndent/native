---
title: "Spinner"
description: "An indicator that can be used to show a loading state."
order: 0
---

--INTRO([Spinner, An indicator that can be used to show a loading state.])--

--USAGE(spinner)--

--SOURCE(spinner)--

# Examples

## Size

Use a `size-*` utility class to change the spinner's size.

**Props used:** `class_name` on `spinner`.

--DEMO(spinner_size)--

## Button

Add a spinner to a button for a loading state. Add `data-icon="inline-start"` to position it before the label.

**Props used:** `data_icon` on `spinner`.

--DEMO(spinner_button)--

## Badge

Add a spinner to a badge for a loading/syncing state.

**Props used:** `data_icon` on `spinner`.

--DEMO(spinner_badge)--

## Marker

Combine `spinner` with `marker` and the `shimmer` utility for animated streaming status indicators. Set `role="status"` so assistive technology announces updates.

**Props used:** `role` on `spinner`.

--DEMO(spinner_marker)--

# API Reference

## spinner

```python
spinner(class_name="size-5")
```

| Prop         | Type   | Default | Description                                                          |
| ------------ | ------ | ------- | ---------------------------------------------------------------------- |
| `class_name` | `str`  | `""`    | Additional classes applied to the icon (e.g. `size-*` to resize).      |

Any other prop accepted by a native `<svg>` (`role`, `aria_label`, `data_icon`, etc.) is also passed straight through. `role="status"` is set by default.
