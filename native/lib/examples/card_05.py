import reflex as rx

from components.button import button
from components.card import card
from native.templates.masonary import masonry_card

items = [
    {
        "title": "Change transfer limit",
        "description": "Adjust how much you can send from your balance.",
    },
    {
        "title": "Scheduled transfers",
        "description": "Set up a transfer to send at a later date.",
    },
    {
        "title": "Direct Debits",
        "description": "Set up and manage regular payments.",
    },
    {
        "title": "Recurring card payments",
        "description": "Manage your repeated card transactions.",
    },
]


@masonry_card(label="Finance")
def card_05() -> rx.Component:

    def menu_item(item: dict) -> rx.Component:
        return button(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        item["title"],
                        class_name="text-sm font-semibold text-foreground text-left",
                    ),
                    rx.el.p(
                        item["description"],
                        class_name="text-sm font-light text-muted-foreground text-left whitespace-normal",
                    ),
                    class_name="flex flex-col gap-y-0.5 flex-1",
                ),
                class_name="w-full flex flex-row items-center gap-x-3",
            ),
            variant="secondary",
            class_name="w-full h-auto py-3 px-4",
        )

    return card.root(
        card.header(
            card.title("Account Controls"),
            card.description("Limits and recurring payments"),
        ),
        card.content(
            rx.el.div(
                *[menu_item(i) for i in items],
                class_name="w-full flex flex-col gap-y-2",
            )
        ),
        class_name="mx-auto w-full max-w-sm",
    )
