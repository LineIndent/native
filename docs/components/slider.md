---
title: "Slider"
description: "An input where the user selects a value from within a given range."
order: 20
---

--INTRO([Slider, An input where the user selects a value from within a given range.])--

--USAGE(slider)--

--SOURCE(slider)--

# Examples

## Basic

A single-thumb slider backed by a native `<input type="range">` — free keyboard, touch, and screen-reader support.

**Props used:** `default_value` on `slider.input`.

--DEMO(slider_basic)--

## Range

Pass a 2-element list to `default_value` for a dual-thumb range slider. Internally this renders two overlapping native range inputs with pointer-events restricted to their thumbs, so both stay independently draggable.

**Props used:** `default_value`, `min`, `max`, `step` on `slider.input`.

--DEMO(slider_range)--

## Vertical

Pass `orientation="vertical"` to **both** `slider.root` and `slider.input` — the root controls the container's height, the input controls its own axis rotation.

**Props used:** `orientation` on `slider.root` and `slider.input`; `default_value`, `min`, `max`, `step` on `slider.input`.

--DEMO(slider_vertical)--

# API Reference

## slider.root

```python
slider.root(
    slider.input(default_value=20),
)
```

| Prop          | Type                              | Default        |
| ------------- | ---------------------------------- | -------------- |
| `orientation` | `Literal["horizontal", "vertical"]` | `"horizontal"` |
| `class_name`  | `str`                              | `""`            |

## slider.input

`default_value`/`value` accepts a bare scalar, a 1-element list, or a 2-element list — a 2-element list switches into range mode automatically.

```python
# single thumb
slider.input(default_value=20)

# range (dual thumb)
slider.input(default_value=[25, 50], min=0, max=100, step=5)

# vertical — orientation must also be set on slider.root
slider.input(default_value=50, orientation="vertical")
```

| Prop              | Type                                | Default        |
| ----------------- | ------------------------------------ | -------------- |
| `default_value` / `value` | `float \| list[float]`        |                |
| `min`              | `float`                             | `0`             |
| `max`              | `float`                             | `100`           |
| `step`             | `float`                             | `1`             |
| `orientation`      | `Literal["horizontal", "vertical"]` | `"horizontal"` |
| `disabled`         | `bool`                              | `False`         |
| `id`               | `str`                                | auto-generated  |
| `class_name`       | `str`                                | `""`            |

**Known limitations:** vertical orientation isn't currently supported in range mode (single-thumb only). If both thumbs of a range slider land on the exact same value, the max thumb sits on top by default.

## slider.value

A styled `<span>` for displaying the current value — not automatically wired to the input. To show a live value, bind it to `rx.State` yourself:

```python
class SliderState(rx.State):
    current: int = 20

slider.root(
    slider.input(default_value=20, on_change=SliderState.set_current),
    slider.value(SliderState.current),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |
