import reflex as rx

from components.card import card
from components.input_group import input_group
from native.templates.masonary import masonry_card


@masonry_card(label="General")
def card_08() -> rx.Component:
    return card.root(
        card.header(
            card.title("404 - Not Found"),
            card.description(
                "The page you're looking for doesn't exist. Try searching for what you need below."
            ),
            class_name="flex flex-col items-center text-center",
        ),
        card.content(
            rx.el.div(
                input_group.root(
                    input_group.input(
                        placeholder="example.com",
                        read_only=True,
                    ),
                ),
                class_name="w-full max-w-md mx-auto",
            )
        ),
        card.footer(
            rx.el.button(
                "Go to homepage",
                class_name="text-sm font-semibold text-foreground hover:opacity-70 transition-opacity cursor-pointer bg-transparent border-none",
            ),
            class_name="flex justify-center w-full",
        ),
        class_name="mx-auto w-full max-w-sm",
    )
