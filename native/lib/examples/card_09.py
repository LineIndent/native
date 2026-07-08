import reflex as rx

from components.core.hugeicon import hi
from components.ui.button import button
from components.ui.card import card
from native.templates.masonary import masonry_card


@masonry_card(label="Finance")
def card_09() -> rx.Component:
    return card.root(
        card.header(
            rx.el.div(
                hi("CreditCardIcon", class_name="size-6 text-foreground"),
                class_name="p-3 rounded-xl bg-secondary flex items-center justify-center w-fit mx-auto mb-2",
            ),
            card.title("Connect Bank"),
            card.description(
                "Link your payout method to receive monthly royalty distributions automatically."
            ),
            class_name="flex flex-col items-center text-center",
        ),
        card.footer(
            button("Set Up Payouts", variant="default", size="sm", class_name="w-full"),
            class_name="w-full",
        ),
        class_name="mx-auto w-full max-w-sm",
    )
