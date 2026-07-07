from components.ui.popover import popover

COMPOSITION = popover.root(
    popover.trigger(),
    popover.portal(
        popover.backdrop(),
        popover.positioner(
            popover.popup(
                popover.header(
                    popover.title(),
                    popover.description(),
                ),
                popover.close(),
            ),
        ),
    ),
)
