---
title: "Bar Chart"
description: "A comprehensive chart for visualizing categorized quantitative data, supporting vertical/horizontal layouts, stacking, custom legends, and dynamic state filtering."
order: 1
---

# Bar Chart

A comprehensive chart for visualizing categorized quantitative data, supporting vertical/horizontal layouts, stacking, custom legends, and dynamic state filtering.

>Reflex wraps **[Recharts](https://recharts.github.io/)** under the hood. This means you build your own charts using Recharts components and only bring in your theme tokens and custom components like chart_tooltip when and where you need it.

# Examples

## Multiple

A multi-series vertical bar chart showing a comparison of discrete datasets side-by-side.

**Props used:** `data_key`, `fill`, `radius`, `is_animation_active` on `bar`; `data_key`, `axis_line`, `tick_size`, `tick_line`, `tick` on `x_axis`.

--DEMO(bar_chart_multiple)--

## Horizontal

A horizontal bar chart layout ideal for ranking categories or displaying long text labels.

**Props used:** `layout="vertical"` on `bar_chart`; `type_="number"`, `hide=True` on `x_axis`; `type_="category"`, `data_key` on `y_axis`.

--DEMO(bar_chart_horizontal)--

## Legend

A stacked vertical bar chart with built-in legend rendering for multi-series comparisons.

**Props used:** `stack_id`, `radius` on `bar`; `legend` component container.

--DEMO(bar_chart_with_legend)--

## Labeled

Displays numeric or text labels directly above individual bars using inline tracking.

**Props used:** `label_list` inside `bar` component container; `position`, `offset`, `fill`, `font_size` on `label_list`.

--DEMO(bar_chart_labeled)--

## Dynamic

Demonstrates dynamic data streaming and filtering utilizing interactive dropdown components and client-side application state variables.

**Props used:** `ClientStateVar`, dynamic `data_key` binding on `bar`.

--DEMO(bar_chart_dynamic)--

## Active

Highlights an individual bar node using distinct stroke attributes based on interactive selections or active data filtering flags.

**Props used:** `stroke`, `stroke_width` mapped dynamically on `bar`.

--DEMO(bar_chart_active)--

## Mixed

Applies explicit unique color configurations per bar instance directly parsed from properties mapped inside individual data structures.

**Props used:** `fill` bound directly to a data dictionary key rather than a static string.

--DEMO(bar_chart_mixed)--

## Multiple Tracks

Renders multiple custom-colored tracking datasets concurrently and integrates a custom grid-aligned multi-device responsive footer legend.

**Props used:** Triple `bar` tracks with corresponding `bg-chart-*` tracking utilities.

--DEMO(bar_chart_multiple_tracks)--


# API Reference

## bar_chart

The main wrapper container handling grid alignment coordinate mappings and responsive bounds for bar graphs.

```python
rx.recharts.bar_chart(
    rx.recharts.bar(
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
| `layout` | `str` | `"horizontal"` |

## bar

Defines individual geometric rect bars mapped to a specific series.

```python
rx.recharts.bar(
    data_key="desktop",
    fill="var(--chart-1)",
    radius=4,
    is_animation_active=False,
)
```

| Prop | Type | Default |
| --- | --- | --- |
| `data_key` | `str` |  |
| `fill` | `str` |  |
| `stroke` | `str` |  |
| `stroke_width` | `int` |  |
| `radius` | `int | list` |  |
| `stack_id` | `str` |  |
| `is_animation_active` | `bool` | `True` |

## label_list

Enables inline annotations rendered automatically beside or within bar nodes.

```python
rx.recharts.label_list(
    data_key="desktop",
    position="top",
    offset=10,
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

Renders horizontal baseline metadata and category text lines.

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
| `type_` | `str` | `"category"` |
| `hide` | `bool` | `False` |
| `axis_line` | `bool` | `True` |
| `tick_line` | `bool` | `True` |
| `tick_size` | `int` |  |
| `tick` | `dict` |  |
| `interval` | `str | int` |  |

## y_axis

Renders vertical tracking axes and baseline ranges.

```python
rx.recharts.y_axis(
    data_key="month",
    type_="category",
    axis_line=False,
)
```

| Prop | Type | Default |
| --- | --- | --- |
| `data_key` | `str` |  |
| `type_` | `str` | `"number"` |
| `hide` | `bool` | `False` |
| `axis_line` | `bool` | `True` |
| `tick_line` | `bool` | `True` |
| `tick_size` | `int` |  |
| `tick` | `dict` |  |

## cartesian_grid

Adds coordinate guiding alignment lines to the chart viewport background.

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

## legend

Adds standard series identifying tracking boxes automatically.

```python
rx.recharts.legend()
```

| Prop | Type | Default |
| --- | --- | --- |
| `align` | `str` | `"center"` |
| `layout` | `str` | `"horizontal"` |

## tooltip

Injects rich interactive popup elements during element hovering events.

```python
chart_tooltip()
```

| Prop | Type | Default |
| --- | --- | --- |
| `label` | `str` |  |
| `cursor` | `bool` |  |
