import reflex as rx

from components.chart.chart_tooltip import chart_tooltip, chart_tooltip_content

data = [
    {"browser": "Chrome", "visitors": 275},
    {"browser": "Safari", "visitors": 200},
    {"browser": "Firefox", "visitors": 187},
    {"browser": "Edge", "visitors": 173},
    {"browser": "Other", "visitors": 90},
]


def line_chart_custom_label():
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Line Chart - Title Label", class_name="text-lg font-semibold"),
            rx.el.p("Showing total visitors for the last 6 months", class_name="text-sm text-muted-foreground"),
            class_name="flex flex-col gap-y-1.5",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                chart_tooltip("hide"),
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False,
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
        class_name=chart_tooltip_content([1], "square") + " w-full p-0 flex flex-col gap-y-6",
    )
