from components.ui.dialog import dialog

COMPOSITION = dialog.root(
    dialog.trigger(),
    dialog.portal(
        dialog.backdrop(),
        dialog.popup(
            dialog.title(),
            dialog.description(),
            dialog.close(),
        ),
    ),
)
