---
title: "Area Chart"
description: "A versatile chart for visualizing quantitative data trends over time or categories, supporting gradients, stacking, and custom legends."
order: 0
---

# Area Chart

A versatile chart for visualizing quantitative data trends over time or categories, supporting gradients, stacking, and custom legends.

>Reflex wraps **[Recharts](https://recharts.github.io/)** under the hood. This means you build your own charts using Recharts components and only bring in your theme tokens and custom components like chart_tooltip when and where you need it.

# Examples

## Basic

A simple area chart showing a single data series over time.

**Props used:** `data_key`, `fill`, `stroke`, `stroke_width`, `type_`, `is_animation_active` on `area`; `data_key`, `axis_line`, `tick_size`, `tick_line`, `tick` on `x_axis`.

--DEMO(area_chart_basic_type)--

## Linear

Uses a linear interpolation curve between points.

**Props used:** `type_="linear"` on `area`.

--DEMO(area_chart_linear_type)--

## Step

Uses stepped interpolation to emphasize discrete changes between values.

**Props used:** `type_="step"` on `area`.

--DEMO(area_chart_step_type)--

## Stacked

Displays multiple datasets stacked on top of each other to show combined totals.

**Props used:** `stack_id` on `area`.

--DEMO(area_chart_stacked)--

## Dynamic

Demonstrates updating chart data from application state.

**Props used:** `data`, `ClientStateVar`, and dynamic chart updates.

--DEMO(area_chart_dynamic)--

## Legend

Shows multiple series with a chart legend.

**Props used:** `legend`, multiple `area` components.

--DEMO(area_chart_with_legend)--

## Axis

Customizes axis appearance and tick formatting.

**Props used:** `x_axis`, `y_axis`, `tick`, `min_tick_gap`, `tick_size`.

--DEMO(area_chart_with_axis)--

## Gradient

Uses SVG gradients to create filled area effects.

**Props used:** `svg.defs`, `svg.linear_gradient`, `fill="url(#...)"`.

--DEMO(area_chart_with_gradient)--


# API Reference

## area_chart

The main chart container. Handles layout, sizing, and coordinates for child chart components.

```python
rx.recharts.area_chart(
    rx.recharts.area(
        data_key="desktop",
    ),
    data=data,
    width="100%",
    height=250,
)
```

| Prop         | Type         | Default |
| ------------ | ------------ | ------- |
| `data`       | `list[dict]` |         |
| `width`      | `str \| int` |         |
| `height`     | `str \| int` |         |
| `margin`     | `dict`       |         |
| `responsive` | `bool`       |         |


## area

Represents a filled data series.

```python
rx.recharts.area(
    data_key="desktop",
    fill="var(--chart-1)",
    stroke="var(--chart-1)",
    stroke_width=2,
)
```

| Prop                  | Type   | Default      |
| --------------------- | ------ | ------------ |
| `data_key`            | `str`  |              |
| `fill`                | `str`  |              |
| `stroke`              | `str`  |              |
| `stroke_width`        | `int`  |              |
| `type_`               | `str`  | `"monotone"` |
| `stack_id`            | `str`  |              |
| `is_animation_active` | `bool` | `True`       |
| `active_dot`          | `dict` |              |

## x_axis

Controls horizontal axis rendering and labels.

```python
rx.recharts.x_axis(
    data_key="month",
    axis_line=False,
    tick={
        "fill": "var(--foreground)",
        "fontSize": 10,
    },
)
```

| Prop           | Type   | Default |
| -------------- | ------ | ------- |
| `data_key`     | `str`  |         |
| `axis_line`    | `bool` | `True`  |
| `tick_line`    | `bool` | `True`  |
| `tick_size`    | `int`  |         |
| `tick`         | `dict` |         |
| `interval`     | `str`  |         |
| `min_tick_gap` | `int`  |         |


## y_axis

Controls vertical axis rendering.

```python
rx.recharts.y_axis(
    width=30,
    axis_line=False,
)
```

| Prop           | Type   | Default |
| -------------- | ------ | ------- |
| `width`        | `int`  |         |
| `axis_line`    | `bool` | `True`  |
| `tick_line`    | `bool` | `True`  |
| `tick_size`    | `int`  |         |
| `tick`         | `dict` |         |
| `min_tick_gap` | `int`  |         |


## cartesian_grid

Adds background grid lines.

```python
rx.recharts.cartesian_grid(
    horizontal=True,
    vertical=False,
)
```

| Prop         | Type   | Default |
| ------------ | ------ | ------- |
| `horizontal` | `bool` | `True`  |
| `vertical`   | `bool` | `True`  |
| `class_name` | `str`  |         |


## tooltip

Displays hover information.

```python
chart_tooltip()
```

| Prop     | Type   | Default |
| -------- | ------ | ------- |
| `label`  | `str`  |         |
| `cursor` | `bool` |         |
