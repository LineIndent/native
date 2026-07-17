from components.ui.dialog import dialog

COMPOSITION = dialog.root(
    dialog.trigger(),
    dialog.popup(
        dialog.title(),
        dialog.description(),
        dialog.close(),
    ),
)
