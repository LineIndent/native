from components.ui.tabs import tabs

COMPOSITION = tabs.root(
    tabs.list(
        tabs.tab(),
        tabs.indicator(),
    ),
    tabs.panel(),
)
