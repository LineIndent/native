import reflex as rx
from components.ui.menu import menu
from components.ui.button import button_variants

def menu_shortcuts() -> rx.Component:
    return menu.root(
        menu.trigger("Workspace Actions Menu", class_name=button_variants(variant="outline")),
        menu.content(
            menu.item("New Tab", menu.shortcut("⌘T")),
            menu.item("New Window", menu.shortcut("⌘N")),
            menu.separator(),
            menu.item("Save Project", menu.shortcut("⌘S")),
        )
    )
