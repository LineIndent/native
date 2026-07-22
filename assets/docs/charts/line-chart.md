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

```python
def line_chart_basic():
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Line Chart", class_name="text-lg font-semibold"),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.line(
                    data_key="desktop",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    type_="natural",
                    dot=False,
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={"fill": "var(--foreground)", "fontSize": 10},
                    interval="preserveStartEnd",
                ),
                data=data,
                width="100%",
                height=250,
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month ",
                    class_name="flex items-center gap-2 leading-none font-medium",
                ),
                rx.el.div(
                    "January - June 2024",
                    class_name="flex items-center gap-2 leading-none text-muted-foreground",
                ),
                class_name="grid gap-2",
            ),
            class_name="flex w-full items-start gap-2 text-sm",
        ),
        class_name=chart_tooltip_content([1], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Linear

Uses linear point-to-point interpolation paths rather than a smoothed natural curve.

**Props used:** `type_="linear"` on `line`.

```python
def line_chart_linear():
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Line Chart - Linear", class_name="text-lg font-semibold"),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.line(
                    data_key="desktop",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    type_="linear",
                    dot=False,
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={"fill": "var(--foreground)", "fontSize": 10},
                    interval="preserveStartEnd",
                ),
                data=data,
                width="100%",
                height=250,
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month ",
                    class_name="flex items-center gap-2 leading-none font-medium",
                ),
                rx.el.div(
                    "January - June 2024",
                    class_name="flex items-center gap-2 leading-none text-muted-foreground",
                ),
                class_name="grid gap-2",
            ),
            class_name="flex w-full items-start gap-2 text-sm",
        ),
        class_name=chart_tooltip_content([1], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Label

Adds standard baseline numeric annotations directly above each individual data node.

**Props used:** `label_list` inside `line` component container; `position`, `offset`, `fill`, `font_size` on `label_list`.

```python
def line_chart_label():
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Line Chart - Label", class_name="text-lg font-semibold"),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.line(
                    rx.recharts.label_list(
                        position="top",
                        offset=20,
                        fill="var(--foreground)",
                        font_size=12,
                    ),
                    data_key="desktop",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    type_="linear",
                    dot=True,
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={"fill": "var(--foreground)", "fontSize": 10},
                    interval="preserveStartEnd",
                ),
                data=data,
                width="100%",
                height=250,
                margin={"left": 20, "right": 20, "top": 25},
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month ",
                    class_name="flex items-center gap-2 leading-none font-medium",
                ),
                rx.el.div(
                    "January - June 2024",
                    class_name="flex items-center gap-2 leading-none text-muted-foreground",
                ),
                class_name="grid gap-2",
            ),
            class_name="flex w-full items-start gap-2 text-sm",
        ),
        class_name=chart_tooltip_content([1], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Multiple

Plots multiple independent data tracks simultaneously on a single shared grid timeline.

**Props used:** Multiple `line` components; `data_key`, `stroke` configurations mapping unique values.

```python
def line_chart_multiple():
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Line Chart - Multiple", class_name="text-lg font-semibold"),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.line(
                    data_key="desktop",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    type_="natural",
                    dot=False,
                    is_animation_active=False,
                ),
                rx.recharts.line(
                    data_key="mobile",
                    stroke="var(--chart-2)",
                    stroke_width=2,
                    type_="natural",
                    dot=False,
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={"fill": "var(--foreground)", "fontSize": 10},
                    interval="preserveStartEnd",
                ),
                data=data,
                width="100%",
                height=250,
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month ",
                    class_name="flex items-center gap-2 leading-none font-medium",
                ),
                rx.el.div(
                    "January - June 2024",
                    class_name="flex items-center gap-2 leading-none text-muted-foreground",
                ),
                class_name="grid gap-2",
            ),
            class_name="flex w-full items-start gap-2 text-sm",
        ),
        class_name=chart_tooltip_content([1, 2], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Title Label

Combines data tracking nodes with custom semantic text bindings extracted dynamically directly out of individual metadata collections.

**Props used:** `label_list` rendering a specific secondary `data_key` attribute from data rows.

```python
def line_chart_custom_label():
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Line Chart - Title Label", class_name="text-lg font-semibold"),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                chart_tooltip("hide"),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.line(
                    rx.recharts.label_list(
                        position="top",
                        offset=20,
                        fill="var(--foreground)",
                        custom_attrs={"fontSize": 11},
                        data_key="browser",
                    ),
                    data_key="visitors",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    type_="natural",
                    dot=True,
                    is_animation_active=False,
                    active_dot={"fill": "var(--chart-1)"},
                ),
                data=data,
                width="100%",
                height=250,
                margin={"left": 25, "right": 20, "top": 25},
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month ",
                    class_name="flex items-center gap-2 leading-none font-medium",
                ),
                rx.el.div(
                    "January - June 2024",
                    class_name="flex items-center gap-2 leading-none text-muted-foreground",
                ),
                class_name="grid gap-2",
            ),
            class_name="flex w-full items-start gap-2 text-sm",
        ),
        class_name=chart_tooltip_content([1], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Minimal

Cleans up layout clutter by hiding dots entirely to emphasize clean structural trends.

**Props used:** `dot=False` on `line`.

```python
def line_chart_minimal():
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Line Chart - Minimal", class_name="text-lg font-semibold"),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.line(
                    data_key="visitors",
                    type_="natural",
                    dot=False,
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    is_animation_active=False,
                ),
                data=data,
                width="100%",
                height=250,
                margin={"left": 20, "right": 20, "top": 25},
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month ",
                    class_name="flex items-center gap-2 leading-none font-medium",
                ),
                rx.el.div(
                    "January - June 2024",
                    class_name="flex items-center gap-2 leading-none text-muted-foreground",
                ),
                class_name="grid gap-2",
            ),
            class_name="flex w-full items-start gap-2 text-sm",
        ),
        class_name=chart_tooltip_content([1], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Interactive

Demonstrates time-series layout optimization combining multi-day boundaries with dense categorical intervals.

**Props used:** `min_tick_gap`, `interval="preserveStartEnd"` on `x_axis`.

```python
def line_chart_interactive():
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Line Chart - Interactive", class_name="text-lg font-semibold"),
            rx.el.p(
                "Showing total visitors for the last 3 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.line(
                    data_key="desktop",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    type_="natural",
                    is_animation_active=False,
                    dot=False,
                    active_dot={"fill": "var(--chart-1)"},
                ),
                rx.recharts.y_axis(type_="number", hide=True),
                rx.recharts.x_axis(
                    data_key="date",
                    axis_line=False,
                    min_tick_gap=32,
                    tick_size=10,
                    tick_line=False,
                    tick={"fill": "var(--foreground)", "fontSize": 10},
                    interval="preserveStartEnd",
                ),
                data=formatted_data,
                width="100%",
                height=250,
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month ",
                    class_name="flex items-center gap-2 leading-none font-medium",
                ),
                rx.el.div(
                    "January - June 2024",
                    class_name="flex items-center gap-2 leading-none text-muted-foreground",
                ),
                class_name="grid gap-2",
            ),
            class_name="flex w-full items-start gap-2 text-sm",
        ),
        class_name=chart_tooltip_content([1], "line")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Footer Legend

Integrates multiple line series data layouts with a custom styled responsive inline flex-row footer legend.

**Props used:** Pure python `*[]` list comprehensions alongside semantic tracking containers mapping series identifications.

```python
def line_chart_footer_legend():
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3("Line Chart - Multiple", class_name="text-lg font-semibold"),
                rx.el.p(
                    "Showing total visitors for the last 6 months",
                    class_name="text-sm text-muted-foreground",
                ),
                class_name="flex flex-col gap-y-1.5",
            ),
            class_name="flex flex-row items-center justify-between w-full",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.line(
                    data_key="desktop",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    type_="natural",
                    dot=False,
                    is_animation_active=False,
                ),
                rx.recharts.line(
                    data_key="mobile",
                    stroke="var(--chart-2)",
                    stroke_width=2,
                    type_="natural",
                    dot=False,
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={"fill": "var(--foreground)", "fontSize": 10},
                    interval="preserveStartEnd",
                ),
                data=data,
                width="100%",
                height=210,
            ),
            rx.el.div(
                *[
                    rx.el.div(
                        rx.el.div(
                            class_name=f"w-3 h-3 rounded-sm bg-chart-{index + 1}"
                        ),
                        rx.el.p(device, class_name="text-sm text-foreground"),
                        class_name="flex flex-row items-center gap-x-2",
                    )
                    for index, device in enumerate(["Desktop", "Mobile"])
                ],
                class_name="py-4 px-4 flex w-full justify-center gap-8",
            ),
            class_name="flex flex-col gap-y-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month ",
                    class_name="flex items-center gap-2 leading-none font-medium",
                ),
                rx.el.div(
                    "January - June 2024",
                    class_name="flex items-center gap-2 leading-none text-muted-foreground",
                ),
                class_name="grid gap-2",
            ),
            class_name="flex w-full items-start gap-2 text-sm",
        ),
        class_name=chart_tooltip_content([1, 2], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```


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
