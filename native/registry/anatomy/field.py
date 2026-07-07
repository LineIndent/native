from components.ui.field import field

COMPOSITION = field.root(
    field.content(
        field.label(),
        field.title(),
        field.description(),
    ),
    field.error(),
)
