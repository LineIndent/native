import reflex as rx

from components.ui.avatar import avatar
from components.ui.menu import menu


def avatar_dropdown_menu() -> rx.Component:
    return menu.root(
        menu.trigger(
            rx.el.img(
                src="https://github.com/LineIndent.png",
                alt="lineindent",
                class_name=avatar.class_names.IMAGE,
            ),
            class_name=avatar.class_names.ROOT,
        ),
        menu.content(
            menu.item("Profile"),
            menu.item("Billing"),
            menu.item("Settings"),
        ),
    )
