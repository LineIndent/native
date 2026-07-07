import reflex as rx

from components.button import button
from components.card import card
from components.hugeicon import hi
from native.templates.masonary import masonry_card


@masonry_card(label="General")
def card_02():

    return card.root(
        card.header(
            card.title("Scheduled reports"),
            card.description("Weekly snapshots. No more manual exports."),
        ),
        card.content(
            rx.el.ul(
                rx.el.li(
                    hi(
                        "ArrowRight01Icon",
                        class_name="mt-0.5 size-4 shrink-0 text-muted-foreground",
                    ),
                    rx.el.span("Choose a schedule (daily, or weekly)."),
                    class_name="flex gap-2",
                ),
                rx.el.li(
                    hi(
                        "ArrowRight01Icon",
                        class_name="mt-0.5 size-4 shrink-0 text-muted-foreground",
                    ),
                    rx.el.span("Send to channels or specific teammates."),
                    class_name="flex gap-2",
                ),
                rx.el.li(
                    hi(
                        "ArrowRight01Icon",
                        class_name="mt-0.5 size-4 shrink-0 text-muted-foreground",
                    ),
                    rx.el.span("Include charts, tables, and key metrics."),
                    class_name="flex gap-2",
                ),
                class_name="grid gap-2 py-2 text-sm",
            )
        ),
        card.footer(
            button(
                "Set up scheduled reports",
                size="sm",
                class_name="w-full",
            ),
            button(
                "See what's new",
                variant="outline",
                size="sm",
                class_name="w-full",
            ),
            class_name="flex-col gap-2",
        ),
        class_name="mx-auto w-full max-w-sm",
    )
