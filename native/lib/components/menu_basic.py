import reflex as rx

from components.ui.button import button_variants
from components.ui.menu import menu


def menu_basic() -> rx.Component:
    return menu.root(
        menu.trigger("Open Menu", class_name=button_variants(variant="outline")),
        menu.content(
            menu.group_label("My Account"),
            menu.item("Profile"),
            menu.item("Billing"),
            menu.item("Settings"),
        ),
    )
