from components.ui.accordion import accordion

COMPOSITION = accordion.root(
    accordion.item(
        accordion.header(
            accordion.trigger(),
        ),
        accordion.panel(),
    ),
    accordion.item(
        accordion.header(
            accordion.trigger(),
        ),
        accordion.panel(),
    ),
)
