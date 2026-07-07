from components.ui.frame import frame

COMPOSITION = frame.root(
    frame.panel(
        frame.header(
            frame.title(),
            frame.description(),
        ),
        frame.footer(),
    ),
)
