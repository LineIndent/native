import reflex as rx

from components.ui.tabs import tabs


def tabs_line() -> rx.Component:
    return tabs.root(
        tabs.list(
            tabs.trigger("Overview", value="overview"),
            tabs.trigger("Analytics", value="analytics"),
            tabs.trigger("Reports", value="reports"),
            variant="line",
        ),
        default_value="overview",
    )
