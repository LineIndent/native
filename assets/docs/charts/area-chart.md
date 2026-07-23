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

```python
def area_chart_basic_type():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Area Chart",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.area_chart(
                chart_tooltip(label="show"),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.area(
                    data_key="desktop",
                    fill="var(--chart-1)",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    interval="preserveStartEnd",
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
                ),
                data=data,
                width="100%",
                height=250,
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month",
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
        class_name=chart_tooltip_content([1], "border")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Linear

Uses a linear interpolation curve between points.

**Props used:** `type_="linear"` on `area`.

```python
def area_chart_linear_type():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Area Chart - Linear",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.area_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.area(
                    data_key="desktop",
                    fill="var(--chart-1)",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    type_="linear",
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    interval="preserveStartEnd",
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
                ),
                data=data,
                width="100%",
                height=250,
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month",
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

## Step

Uses stepped interpolation to emphasize discrete changes between values.

**Props used:** `type_="step"` on `area`.

```python
def area_chart_step_type():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Area Chart - Step",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.area_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.area(
                    data_key="desktop",
                    fill="var(--chart-1)",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    type_="step",
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    interval="preserveStartEnd",
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
                ),
                data=data,
                width="100%",
                height=250,
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month",
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

## Stacked

Displays multiple datasets stacked on top of each other to show combined totals.

**Props used:** `stack_id` on `area`.

```python
def area_chart_stacked():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Area Chart - Stacked",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.area_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.area(
                    data_key="desktop",
                    fill="var(--chart-1)",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    stack_id="a",
                    is_animation_active=False,
                ),
                rx.recharts.area(
                    data_key="mobile",
                    fill="var(--chart-2)",
                    stroke="var(--chart-2)",
                    stroke_width=2,
                    stack_id="a",
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    interval="preserveStartEnd",
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
                ),
                data=data,
                width="100%",
                height=250,
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "Trending up by 5.2% this month",
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

## Dynamic

Demonstrates updating chart data from application state.

**Props used:** `data`, `ClientStateVar`, and dynamic chart updates.

```python
def area_chart_dynamic():
    select_options = [
        ("Last 3 Months", data),
        ("Last 30 Days", data[-30:]),
        ("Last 7 Days", data[-7:]),
    ]

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Area Chart - Dynamic",
                        class_name="text-lg font-semibold",
                    ),
                    rx.el.p(
                        "Showing total visitors for the last 6 months",
                        class_name="text-sm text-muted-foreground",
                    ),
                    class_name="flex flex-col gap-y-1.5",
                ),
                rx.el.select(
                    *[
                        rx.el.option(
                            label,
                            on_click=SelectedRange.set_value(value),
                        )
                        for label, value in select_options
                    ],
                    default_value="Last 3 Months",
                    class_name="relative flex items-center whitespace-nowrap justify-center gap-2 py-2 rounded-lg shadow-sm px-3 bg-secondary border border-input",
                ),
                class_name="flex flex-row flex-wrap gap-y-4 items-center justify-between",
            ),
        ),
        rx.el.div(
            rx.recharts.area_chart(
                rx.el.svg.defs(
                    gradient("desktop", "chart-1"),
                    gradient("mobile", "chart-2"),
                ),
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                area("mobile", "chart-2"),
                area("desktop", "chart-1"),
                rx.recharts.x_axis(
                    data_key="date",
                    axis_line=False,
                    min_tick_gap=32,
                    tick_size=10,
                    tick_line=False,
                    interval="preserveStartEnd",
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
                ),
                data=SelectedRange.value,
                width="100%",
                height=250,
            ),
            rx.el.div(
                *[
                    rx.el.div(
                        rx.el.div(
                            class_name=f"h-2 w-2 shrink-0 rounded-[2px] bg-chart-{index + 1}"
                        ),
                        rx.el.p(
                            device,
                            class_name="text-sm text-foreground",
                        ),
                        class_name="flex flex-row items-center gap-x-2",
                    )
                    for index, device in enumerate(["Desktop", "Mobile"])
                ],
                class_name="py-4 px-4 flex w-full justify-center gap-8",
            ),
            class_name="flex flex-col items-center",
        ),
        class_name=chart_tooltip_content([1, 2], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Legend

Shows multiple series with a chart legend.

**Props used:** `legend`, multiple `area` components.

```python
def area_chart_with_legend():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Area Chart - Legend",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-1.5",
        ),
        rx.el.div(
            rx.recharts.area_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.area(
                    data_key="mobile",
                    fill="var(--chart-1)",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    stack_id="a",
                    is_animation_active=False,
                ),
                rx.recharts.area(
                    data_key="desktop",
                    fill="var(--chart-2)",
                    stroke="var(--chart-2)",
                    stroke_width=2,
                    stack_id="a",
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
                    interval="preserveStartEnd",
                ),
                rx.recharts.legend(),
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

## Axis

Customizes axis appearance and tick formatting.

**Props used:** `x_axis`, `y_axis`, `tick`, `min_tick_gap`, `tick_size`.

```python
def area_chart_with_axis():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Area Chart - Axes",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-1.5",
        ),
        rx.el.div(
            rx.recharts.area_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.area(
                    data_key="mobile",
                    fill="var(--chart-1)",
                    stroke="var(--chart-1)",
                    stroke_width=2,
                    stack_id="a",
                    is_animation_active=False,
                ),
                rx.recharts.area(
                    data_key="desktop",
                    fill="var(--chart-2)",
                    stroke="var(--chart-2)",
                    stroke_width=2,
                    stack_id="a",
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
                    interval="preserveStartEnd",
                ),
                rx.recharts.y_axis(
                    width=30,
                    axis_line=False,
                    min_tick_gap=50,
                    tick_size=10,
                    tick_line=False,
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
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

## Gradient

Uses SVG gradients to create filled area effects.

**Props used:** `svg.defs`, `svg.linear_gradient`, `fill="url(#...)"`.

```python
def area_chart_with_gradient():
    series = [
        ("desktop", "Desktop", "--chart-1"),
        ("mobile", "Mobile", "--chart-2"),
    ]

    def create_gradient(var_name):
        return rx.el.svg.linear_gradient(
            rx.el.svg.stop(
                stop_color=f"var({var_name})",
                offset="5%",
                stop_opacity=0.8,
            ),
            rx.el.svg.stop(
                stop_color=f"var({var_name})",
                offset="95%",
                stop_opacity=0.1,
            ),
            x1=0,
            x2=0,
            y1=0,
            y2=1,
            id=var_name.strip("-"),
        )

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Area Chart - Gradient",
                        class_name="font-semibold",
                    ),
                    rx.el.p(
                        "Showing total visitors for the last 6 months",
                        class_name="text-sm text-muted-foreground",
                    ),
                    class_name="flex flex-col gap-y-1.5",
                ),
                rx.el.div(
                    *[
                        rx.el.div(
                            rx.el.div(
                                class_name="h-2 w-2 shrink-0 rounded-[2px]",
                                style={
                                    "backgroundColor": f"var({s[2]})",
                                },
                            ),
                            rx.el.p(
                                s[1],
                                class_name="text-xs font-medium",
                            ),
                            class_name="flex items-center gap-2",
                        )
                        for s in series
                    ],
                    class_name="flex items-center gap-4 w-full justify-end",
                ),
                class_name="flex flex-row flex-wrap gap-4 items-center justify-between w-full",
            ),
        ),
        rx.el.div(
            rx.recharts.area_chart(
                rx.el.svg.defs(
                    *(create_gradient(s[2]) for s in series),
                ),
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                *[
                    rx.recharts.area(
                        data_key=s[0],
                        fill=f"url(#{s[2].strip('-')})",
                        stroke=f"var({s[2]})",
                        stroke_width=2,
                        stack_id="1",
                        is_animation_active=False,
                    )
                    for s in series
                ],
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
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
