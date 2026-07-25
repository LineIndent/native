import reflex as rx

from components.chart.chart_tooltip import chart_tooltip_content

data = [
    {"hour": "00:00", "temperature": 12.8},
    {"hour": "01:00", "temperature": 12.4},
    {"hour": "02:00", "temperature": 12.2},
    {"hour": "03:00", "temperature": 11.9},
    {"hour": "04:00", "temperature": 11.7},
    {"hour": "05:00", "temperature": 11.5},
    {"hour": "06:00", "temperature": 11.3},
    {"hour": "07:00", "temperature": 11.2},
    {"hour": "08:00", "temperature": 11.5},
    {"hour": "09:00", "temperature": 12.0},
    {"hour": "10:00", "temperature": 13.0},
    {"hour": "11:00", "temperature": 14.2},
    {"hour": "12:00", "temperature": 15.5},
    {"hour": "13:00", "temperature": 16.8},
    {"hour": "14:00", "temperature": 17.5},
    {"hour": "15:00", "temperature": 18.1},
    {"hour": "16:00", "temperature": 18.2},
    {"hour": "17:00", "temperature": 17.8},
    {"hour": "18:00", "temperature": 17.2},
    {"hour": "19:00", "temperature": 16.5},
    {"hour": "20:00", "temperature": 15.8},
    {"hour": "21:00", "temperature": 14.9},
    {"hour": "22:00", "temperature": 14.2},
    {"hour": "23:00", "temperature": 13.5},
]


def _chart(show_y_axis: bool) -> rx.Component:
    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(
            horizontal=True,
            vertical=False,
            stroke="color-mix(in oklab, var(--muted-foreground) 15%, transparent)",
        ),
        rx.recharts.x_axis(
            data_key="hour",
            tick_line=False,
            axis_line=False,
            interval="preserveStartEnd",
            height=50,
            tick={
                "fill": "var(--foreground)",
                "fontSize": 11,
            },
            label={
                "value": "24H Temperature Readout (Zurich)",
                "position": "insideBottom",
                "style": {
                    "fill": "var(--muted-foreground)",
                    "fontSize": "12px",
                },
            },
        ),
        rx.recharts.y_axis(
            width=20,
            tick_line=False,
            axis_line=False,
            tick={
                "fill": "var(--foreground)",
                "fontSize": 11,
            },
            hide=not show_y_axis,
        ),
        rx.recharts.bar(
            data_key="temperature",
            fill="var(--chart-1)",
            is_animation_active=False,
        ),
        data=data,
        width="100%",
        height=320,
    )


def bar_chart_04():
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Temperature",
                class_name="text-base leading-snug font-medium",
            ),
            rx.el.p(
                "Zurich — 24 hour readout",
                class_name="text-sm text-muted-foreground",
            ),
        ),
        rx.el.div(
            rx.el.div(_chart(show_y_axis=False), class_name="sm:hidden"),
            rx.el.div(_chart(show_y_axis=True), class_name="hidden sm:block"),
        ),
        class_name=chart_tooltip_content([1], "square") + " w-full flex flex-col gap-6",
    )
