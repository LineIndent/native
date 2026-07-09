import reflex as rx

from components.core.hugeicon import hi
from components.ui.button import button
from components.ui.button_group import button_group
from components.ui.menu import menu


def button_group_dropdown() -> rx.Component:
    return button_group.root(
        button("Follow", variant="outline"),
        menu.root(
            menu.trigger(
                button(
                    hi("ArrowDown01Icon"),
                    variant="outline",
                    class_name="pl-2!",
                ),
            ),
            menu.content(
                menu.item("Mute Conversation"),
                menu.item("Mark as Read"),
                menu.item("Report Conversation"),
                menu.item("Block User"),
                menu.item("Share Conversation"),
                menu.item("Copy Conversation"),
            ),
            menu.separator(),
            menu.content(
                menu.item("Delete Conversation", variant="destructive"),
            ),
        ),
    )
