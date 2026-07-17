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
                    class_name="flex items-center gap-4",
                ),
                class_name="flex items-center justify-between w-full",
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
