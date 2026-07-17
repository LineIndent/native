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
