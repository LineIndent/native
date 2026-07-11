from datetime import datetime

import reflex as rx

from reflex.experimental import ClientStateVar
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
    {"date": "2024-04-11", "desktop": 327, "mobile": 350},
    {"date": "2024-04-12", "desktop": 292, "mobile": 210},
    {"date": "2024-04-13", "desktop": 342, "mobile": 380},
    {"date": "2024-04-14", "desktop": 137, "mobile": 220},
    {"date": "2024-06-02", "desktop": 470, "mobile": 410},
    {"date": "2024-06-03", "desktop": 103, "mobile": 160},
    {"date": "2024-06-04", "desktop": 439, "mobile": 380},
    {"date": "2024-06-05", "desktop": 88, "mobile": 140},
    {"date": "2024-06-06", "desktop": 294, "mobile": 250},
    {"date": "2024-06-07", "desktop": 323, "mobile": 370},
    {"date": "2024-06-08", "desktop": 385, "mobile": 320},
    {"date": "2024-06-09", "desktop": 438, "mobile": 480},
    {"date": "2024-06-10", "desktop": 155, "mobile": 200},
    {"date": "2024-06-11", "desktop": 92, "mobile": 150},
    {"date": "2024-06-12", "desktop": 492, "mobile": 420},
    {"date": "2024-06-13", "desktop": 81, "mobile": 130},
    {"date": "2024-06-14", "desktop": 426, "mobile": 380},
    {"date": "2024-06-15", "desktop": 307, "mobile": 350},
]

formatted_data = [
    {
        "date": datetime.strptime(item["date"], "%Y-%m-%d").strftime("%b %d"),
        "desktop": item["desktop"],
        "mobile": item["mobile"],
    }
    for item in data
]

SelectedType = ClientStateVar.create("bar_selected", "mobile")

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
