import reflex as rx

from components.ui.card import card
from components.ui.tabs import tabs


def tabs_basic() -> rx.Component:
    return tabs.root(
        tabs.list(
            tabs.trigger("Overview", value="overview"),
            tabs.trigger("Analytics", value="analytics"),
            tabs.trigger("Reports", value="reports"),
            tabs.trigger("Settings", value="settings"),
        ),
        tabs.content(
            card.root(
                card.header(
                    card.title("Overview"),
                    card.description(
                        "View your key metrics and recent project activity. Track progress "
                        "across all your active projects."
                    ),
                ),
                card.content(
                    "You have 12 active projects and 3 pending tasks.",
                    class_name="text-sm text-muted-foreground",
                ),
            ),
            value="overview",
        ),
        tabs.content(
            card.root(
                card.header(
                    card.title("Analytics"),
                    card.description(
                        "Track performance and user engagement metrics. Monitor trends and "
                        "identify growth opportunities."
                    ),
                ),
                card.content(
                    "Page views are up 25% compared to last month.",
                    class_name="text-sm text-muted-foreground",
                ),
            ),
            value="analytics",
        ),
        tabs.content(
            card.root(
                card.header(
                    card.title("Reports"),
                    card.description(
                        "Generate and download your detailed reports. Export data in "
                        "multiple formats for analysis."
                    ),
                ),
                card.content(
                    "You have 5 reports ready and available to export.",
                    class_name="text-sm text-muted-foreground",
                ),
            ),
            value="reports",
        ),
        tabs.content(
            card.root(
                card.header(
                    card.title("Settings"),
                    card.description(
                        "Manage your account preferences and options. Customize your "
                        "experience to fit your needs."
                    ),
                ),
                card.content(
                    "Configure notifications, security, and themes.",
                    class_name="text-sm text-muted-foreground",
                ),
            ),
            value="settings",
        ),
        default_value="overview",
        class_name="w-[400px]",
    )
