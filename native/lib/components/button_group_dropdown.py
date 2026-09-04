import reflex as rx

from components.core.hugeicon import hi
from components.ui.button import button, button_variants
from components.ui.button_group import button_group
from components.ui.menu import menu


def button_group_dropdown() -> rx.Component:
    return button_group.root(
        button("Follow", variant="outline"),
        menu.root(
            menu.trigger(
                hi("ArrowDown01Icon"),
                class_name=f"""{button_variants("outline")} rounded-l-none border-l-0""",
            ),
            menu.content(
                menu.item("Mute Conversation"),
                menu.item("Mark as Read"),
                menu.item("Report Conversation"),
                class_name="w-[180px]",
            ),
        ),
    )
