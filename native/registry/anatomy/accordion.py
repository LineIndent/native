from components.ui.accordion import accordion

COMPOSITION = accordion.root(
    accordion.item(
        accordion.trigger(),
        accordion.panel(),
    ),
    accordion.item(
        accordion.trigger(),
        accordion.panel(),
    ),
)
