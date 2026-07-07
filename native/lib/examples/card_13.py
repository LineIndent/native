import reflex as rx

from components.badge import badge
from components.button import button
from components.card import card
from native.templates.masonary import masonry_card


@masonry_card(label="General")
def card_13() -> rx.Component:
    return card.root(
        rx.el.div(
            class_name="absolute inset-0 z-30 aspect-video",
        ),
        rx.el.img(
            src="/buridan.webp",
            alt="Event cover",
            class_name="relative z-20 aspect-video w-full object-cover border-b border-input",
        ),
        card.header(
            card.action(
                badge("Featured", variant="secondary"),
            ),
            card.title("Design systems meetup"),
            card.description(
                "A practical talk on component APIs, accessibility, and shipping faster."
            ),
        ),
        card.footer(
            button("View Event", class_name="w-full"),
        ),
        class_name="relative mx-auto w-full max-w-sm pt-0",
    )
