import reflex as rx

from components.ui.button import button
from components.ui.card import card
from components.ui.input import input
from components.ui.input_group import input_group
from native.templates.masonary import masonry_card


@masonry_card(label="General")
def card_07() -> rx.Component:
    return card.root(
        card.header(
            card.title("Standard Actions"),
            card.description("Basic component variants"),
        ),
        card.content(
            rx.el.div(
                rx.el.div(
                    button("Default", variant="default", size="sm"),
                    button("Secondary", variant="secondary", size="sm"),
                    button("Outline", variant="outline", size="sm"),
                    class_name="w-full grid grid-cols-3 items-center gap-x-2",
                ),
                rx.el.div(
                    input(placeholder="name"),
                    input_group.root(
                        input_group.textarea(
                            id="block-end-textarea",
                            placeholder="Write a comment...",
                        ),
                        input_group.addon(
                            input_group.text("0/280"),
                            align="block-end",
                        ),
                    ),
                    class_name="flex flex-col gap-y-2",
                ),
                class_name="flex flex-col gap-y-4",
            )
        ),
        card.footer(
            button("Close", variant="default", size="sm"),
            button("Send Text", variant="outline", size="sm"),
            class_name="w-full grid grid-cols-2 items-center gap-x-2",
        ),
        class_name="mx-auto w-full max-w-sm",
    )
