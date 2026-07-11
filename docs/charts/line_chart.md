---
title: "Line Chart"
description: "A versatile chart for visualizing continuous quantitative data trends over time or categories, supporting custom curves, annotations, multi-series tracking, and interactive bounds."
order: 2
---

# Line Chart

A versatile chart for visualizing continuous quantitative data trends over time or categories, supporting custom curves, annotations, multi-series tracking, and interactive bounds.

>Reflex wraps **[Recharts](https://recharts.github.io/)** under the hood. This means you build your own charts using Recharts components and only bring in your theme tokens and custom components like chart_tooltip when and where you need it.

# Examples

## Basic

A simple line chart showing a single quantitative data series over time with natural smoothing curves.

**Props used:** `data_key`, `stroke`, `stroke_width`, `type_`, `dot`, `is_animation_active` on `line`; `data_key`, `axis_line`, `tick_size`, `tick_line`, `tick`, `interval` on `x_axis`.

--DEMO(line_chart_basic)--

## Linear

Uses linear point-to-point interpolation paths rather than a smoothed natural curve.

**Props used:** `type_="linear"` on `line`.

--DEMO(line_chart_linear)--

## Label

Adds standard baseline numeric annotations directly above each individual data node.

**Props used:** `label_list` inside `line` component container; `position`, `offset`, `fill`, `font_size` on `label_list`.

--DEMO(line_chart_label)--

## Multiple

Plots multiple independent data tracks simultaneously on a single shared grid timeline.

**Props used:** Multiple `line` components; `data_key`, `stroke` configurations mapping unique values.

--DEMO(line_chart_multiple)--

## Title Label

Combines data tracking nodes with custom semantic text bindings extracted dynamically directly out of individual metadata collections.

**Props used:** `label_list` rendering a specific secondary `data_key` attribute from data rows.

--DEMO(line_chart_custom_label)--

## Minimal

Cleans up layout clutter by hiding dots entirely to emphasize clean structural trends.

**Props used:** `dot=False` on `line`.

--DEMO(line_chart_minimal)--

## Interactive

Demonstrates time-series layout optimization combining multi-day boundaries with dense categorical intervals.

**Props used:** `min_tick_gap`, `interval="preserveStartEnd"` on `x_axis`.

--DEMO(line_chart_interactive)--

## Footer Legend

Integrates multiple line series data layouts with a custom styled responsive inline flex-row footer legend.

**Props used:** Pure python `*[]` list comprehensions alongside semantic tracking containers mapping series identifications.

--DEMO(line_chart_footer_legend)--


# API Reference

## line_chart

The core layout container coordinate mapping viewport for drawing linear graphs.

```python
rx.recharts.line_chart(
    rx.recharts.line(
        data_key="desktop",
    ),
    data=data,
    width="100%",
    height=250,
)
```

| Prop | Type | Default |
| --- | --- | --- |
| `data` | `list[dict]` |  |
| `width` | `str | int` |  |
| `height` | `str | int` |  |
| `margin` | `dict` |  |

## line

Defines an individual linear path stroke segment mapped onto a dataset.

```python
rx.recharts.line(
    data_key="desktop",
    stroke="var(--chart-1)",
    stroke_width=2,
    type_="natural",
    dot=False,
    is_animation_active=False,
)
```

| Prop | Type | Default |
| --- | --- | --- |
| `data_key` | `str` |  |
| `stroke` | `str` |  |
| `stroke_width` | `int` |  |
| `type_` | `str` | `"text"` |
| `dot` | `bool | dict` | `True` |
| `active_dot` | `dict` |  |
| `is_animation_active` | `bool` | `True` |

## label_list

Appends context descriptive floating tags immediately following line graph nodes.

```python
rx.recharts.label_list(
    data_key="desktop",
    position="top",
    offset=20,
    fill="var(--foreground)",
    font_size=12,
)
```

| Prop | Type | Default |
| --- | --- | --- |
| `data_key` | `str` |  |
| `position` | `str` |  |
| `offset` | `int` |  |
| `fill` | `str` |  |
| `font_size` | `int` |  |

## x_axis

Builds horizontal grid tracking indicators.

```python
rx.recharts.x_axis(
    data_key="month",
    axis_line=False,
    tick={"fill": "var(--foreground)", "fontSize": 10},
)
```

| Prop | Type | Default |
| --- | --- | --- |
| `data_key` | `str` |  |
| `hide` | `bool` | `False` |
| `axis_line` | `bool` | `True` |
| `tick_line` | `bool` | `True` |
| `tick_size` | `int` |  |
| `tick` | `dict` |  |
| `min_tick_gap` | `int` |  |
| `interval` | `str | int` |  |

## y_axis

Builds vertical tracking grids and value thresholds.

```python
rx.recharts.y_axis(
    type_="number",
    hide=True,
)
```

| Prop | Type | Default |
| --- | --- | --- |
| `type_` | `str` | `"number"` |
| `hide` | `bool` | `False` |
| `axis_line` | `bool` | `True` |
| `tick_line` | `bool` | `True` |
| `tick_size` | `int` |  |
| `tick` | `dict` |  |

## cartesian_grid

Provides clean backdrop grid intersections.

```python
rx.recharts.cartesian_grid(
    horizontal=True,
    vertical=False,
)
```

| Prop | Type | Default |
| --- | --- | --- |
| `horizontal` | `bool` | `True` |
| `vertical` | `bool` | `True` |
| `class_name` | `str` |  |

## tooltip

Hover actions triggering beautiful popover layout summaries.

```python
chart_tooltip()
```

| Prop | Type | Default |
| --- | --- | --- |
| `label` | `str` |  |
| `cursor` | `bool` |  |
