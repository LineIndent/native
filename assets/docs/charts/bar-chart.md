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

```python
def bar_chart_multiple():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Bar Chart - Multiple",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.bar(
                    data_key="desktop",
                    fill="var(--chart-1)",
                    radius=4,
                    is_animation_active=False,
                ),
                rx.recharts.bar(
                    data_key="mobile",
                    fill="var(--chart-2)",
                    radius=4,
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

## Horizontal

A horizontal bar chart layout ideal for ranking categories or displaying long text labels.

**Props used:** `layout="vertical"` on `bar_chart`; `type_="number"`, `hide=True` on `x_axis`; `type_="category"`, `data_key` on `y_axis`.

```python
def bar_chart_horizontal():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Bar Chart - Horizontal",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                chart_tooltip(),
                rx.recharts.bar(
                    data_key="desktop",
                    fill="var(--chart-1)",
                    radius=4,
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    type_="number",
                    hide=True,
                    tick_size=0,
                ),
                rx.recharts.y_axis(
                    data_key="month",
                    type_="category",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
                ),
                data=data,
                layout="vertical",
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

## Legend

A stacked vertical bar chart with built-in legend rendering for multi-series comparisons.

**Props used:** `stack_id`, `radius` on `bar`; `legend` component container.

```python
def bar_chart_with_legend():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Bar Chart - Legend",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.bar(
                    data_key="desktop",
                    fill="var(--chart-1)",
                    stack_id="a",
                    radius=[0, 0, 4, 4],
                    is_animation_active=False,
                ),
                rx.recharts.bar(
                    data_key="mobile",
                    fill="var(--chart-2)",
                    stack_id="a",
                    radius=[4, 4, 0, 0],
                    is_animation_active=False,
                ),
                rx.recharts.y_axis(
                    type_="number",
                    hide=True,
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

## Labeled

Displays numeric or text labels directly above individual bars using inline tracking.

**Props used:** `label_list` inside `bar` component container; `position`, `offset`, `fill`, `font_size` on `label_list`.

```python
def bar_chart_labeled():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Bar Chart - Labeled",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.bar(
                    rx.recharts.label_list(
                        data_key="desktop",
                        position="top",
                        offset=10,
                        fill="var(--foreground)",
                        font_size=12,
                    ),
                    data_key="desktop",
                    fill="var(--chart-1)",
                    radius=4,
                    is_animation_active=False,
                ),
                rx.recharts.y_axis(
                    type_="number",
                    hide=True,
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
                margin={"top": 20},
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

## Dynamic

Demonstrates dynamic data streaming and filtering utilizing interactive dropdown components and client-side application state variables.

**Props used:** `ClientStateVar`, dynamic `data_key` binding on `bar`.

```python
def bar_chart_dynamic():

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Bar Chart - Dynamic",
                    class_name="text-lg font-semibold",
                ),
                rx.el.p(
                    "Showing total visitors for the last 6 months",
                    class_name="text-sm text-muted-foreground",
                ),
                class_name="flex flex-col gap-y-1.5",
            ),
            rx.el.select(
                rx.el.option("Mobile", on_click=SelectedType.set_value("mobile")),
                rx.el.option("Desktop", on_click=SelectedType.set_value("desktop")),
                default_value="Mobile",
                class_name="relative flex items-center whitespace-nowrap justify-center gap-2 py-2 rounded-lg shadow-sm px-3",
            ),
            class_name="w-full flex flex-row items-center justify-between"
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                chart_tooltip("hide"),
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.bar(
                    data_key=SelectedType.value,
                    fill="var(--chart-1)",
                    radius=[2, 2, 0, 0],
                    is_animation_active=False,
                ),
                rx.recharts.y_axis(
                    type_="number",
                    hide=True,
                ),
                rx.recharts.x_axis(
                    data_key="date",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    interval="preserveStartEnd",
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
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
        class_name=chart_tooltip_content([1], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```

## Active

Highlights an individual bar node using distinct stroke attributes based on interactive selections or active data filtering flags.

**Props used:** `stroke`, `stroke_width` mapped dynamically on `bar`.

```python
def bar_chart_active():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Bar Chart - Active",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.bar(
                    data_key="desktop",
                    fill="var(--chart-1)",
                    stack_id="a",
                    radius=4,
                    stroke="stroke",
                    stroke_width=2,
                    is_animation_active=False,
                ),
                rx.recharts.y_axis(
                    type_="number",
                    hide=True,
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
                data=modified_data,
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

## Mixed

Applies explicit unique color configurations per bar instance directly parsed from properties mapped inside individual data structures.

**Props used:** `fill` bound directly to a data dictionary key rather than a static string.

```python
def bar_chart_mixed():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Bar Chart - Mixed",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                chart_tooltip(),
                rx.recharts.bar(
                    data_key="visitors",
                    fill="fill",
                    radius=4,
                    is_animation_active=False,
                ),
                rx.recharts.x_axis(
                    type_="number",
                    hide=True,
                    tick_size=0,
                ),
                rx.recharts.y_axis(
                    data_key="browser",
                    type_="category",
                    axis_line=False,
                    tick_size=10,
                    tick_line=False,
                    tick={
                        "fill": "var(--foreground)",
                        "fontSize": 10,
                    },
                ),
                data=data,
                layout="vertical",
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

## Multiple Tracks

Renders multiple custom-colored tracking datasets concurrently and integrates a custom grid-aligned multi-device responsive footer legend.

**Props used:** Triple `bar` tracks with corresponding `bg-chart-*` tracking utilities.

```python
def bar_chart_multiple_tracks():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Bar Chart - Multiple",
                class_name="text-lg font-semibold",
            ),
            rx.el.p(
                "Showing total visitors for the last 6 months",
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                chart_tooltip(),
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False,
                    stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
                ),
                rx.recharts.bar(
                    data_key="desktop",
                    fill="var(--chart-1)",
                    radius=4,
                    is_animation_active=False,
                ),
                rx.recharts.bar(
                    data_key="mobile",
                    fill="var(--chart-2)",
                    radius=4,
                    is_animation_active=False,
                ),
                rx.recharts.bar(
                    data_key="tablet",
                    fill="var(--chart-3)",
                    radius=4,
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
                height=230,
            ),
            rx.el.div(
                *[
                    rx.el.div(
                        rx.el.div(
                            class_name=f"h-3 w-3 rounded-sm bg-chart-{index + 1}"
                        ),
                        rx.el.p(device, class_name="text-xs text-foreground"),
                        class_name="flex flex-row items-center gap-x-2",
                    ) for index, device in enumerate(["Desktop", "Mobile", "Tablet"])
                ],
                class_name="flex items-center gap-4 justify-center",
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
        class_name=chart_tooltip_content([1, 2, 3], "square")
        + " w-full p-0 flex flex-col gap-y-6",
    )
```


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
