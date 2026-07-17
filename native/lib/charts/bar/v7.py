import reflex as rx

from components.chart.chart_tooltip import chart_tooltip, chart_tooltip_content

data = [
    {"browser": "Chrome", "visitors": 275, "fill": "var(--chart-1)"},
    {"browser": "Safari", "visitors": 200, "fill": "var(--chart-2)"},
    {"browser": "Firefox", "visitors": 187, "fill": "var(--chart-3)"},
    {"browser": "Edge", "visitors": 173, "fill": "var(--chart-4)"},
    {"browser": "Other", "visitors": 90, "fill": "var(--chart-5)"},
]


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
