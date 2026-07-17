import reflex as rx

from components.core.hugeicon import hi
from components.ui.tabs import tabs


def tabs_icons() -> rx.Component:
    return tabs.root(
        tabs.list(
            tabs.trigger(
                hi("BrowserIcon"),
                "Preview",
                value="preview",
            ),
            tabs.trigger(
                hi("CodeIcon"),
                "Code",
                value="code",
            ),
        ),
        default_value="preview",
    )
