import reflex as rx

from components.ui.button import button_variants
from components.ui.menu import menu


def menu_destructive() -> rx.Component:
    return menu.root(
        menu.trigger("Danger Zone", class_name=button_variants(variant="outline")),
        menu.content(
            menu.item("Account Settings"),
            menu.separator(),
            menu.item("Delete Repository", variant="destructive"),
            class_name="w-[10rem]",
        ),
    )
