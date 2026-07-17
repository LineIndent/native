from datetime import datetime

import reflex as rx

from components.chart.chart_tooltip import chart_tooltip, chart_tooltip_content

data = [
    {"date": "2024-04-01", "desktop": 222, "mobile": 150},
    {"date": "2024-04-02", "desktop": 97, "mobile": 180},
    {"date": "2024-04-03", "desktop": 167, "mobile": 120},
    {"date": "2024-04-04", "desktop": 242, "mobile": 260},
    {"date": "2024-04-05", "desktop": 373, "mobile": 290},
    {"date": "2024-04-06", "desktop": 301, "mobile": 340},
    {"date": "2024-04-07", "desktop": 245, "mobile": 180},
    {"date": "2024-04-08", "desktop": 409, "mobile": 320},
    {"date": "2024-04-09", "desktop": 59, "mobile": 110},
    {"date": "2024-04-10", "desktop": 261, "mobile": 190},
]

formatted_data = [
    {**item, "date": datetime.strptime(item["date"], "%Y-%m-%d").strftime("%b %d")}
    for item in data
]


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
