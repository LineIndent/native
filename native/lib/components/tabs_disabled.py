from components.ui.tabs import tabs


def tabs_disabled():
    return tabs.root(
        tabs.list(
            tabs.trigger("Home", value="home"),
            tabs.trigger(
                "Disabled",
                value="settings",
                disabled=True,
            ),
        ),
        default_value="home",
    )
