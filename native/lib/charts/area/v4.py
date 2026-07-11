import reflex as rx

from components.chart.chart_tooltip import chart_tooltip, chart_tooltip_content


data = [
    {"month": "Jan", "desktop": 186, "mobile": 80},
    {"month": "Feb", "desktop": 305, "mobile": 200},
    {"month": "Mar", "desktop": 237, "mobile": 120},
    {"month": "Apr", "desktop": 73, "mobile": 190},
    {"month": "May", "desktop": 209, "mobile": 130},
    {"month": "Jun", "desktop": 214, "mobile": 140},
]


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
                    horizontal=True, vertical=False,
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
