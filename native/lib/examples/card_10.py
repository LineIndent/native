import reflex as rx

from components.button import button
from components.card import card
from components.checkbox import checkbox
from native.templates.masonary import masonry_card


@masonry_card(label="General")
def card_10() -> rx.Component:
    notification_items = [
        {
            "label": "Transaction alerts",
            "description": "Deposits, withdrawals, and transfers.",
            "default": True,
        },
        {
            "label": "Security alerts",
            "description": "Login attempts and account changes.",
            "default": True,
        },
        {
            "label": "Goal milestones",
            "description": "Updates at 25%, 50%, 75%, and 100%.",
            "default": False,
        },
        {
            "label": "Market updates",
            "description": "Daily portfolio summary and price alerts.",
            "default": False,
        },
    ]

    def checkbox_row(item: dict) -> rx.Component:
        return rx.el.label(
            checkbox.root(
                checkbox.indicator(),
                default_checked=item["default"],
                class_name="mt-1",
            ),
            rx.el.div(
                rx.el.p(
                    item["label"], class_name="text-sm font-semibold text-foreground"
                ),
                rx.el.p(
                    item["description"],
                    class_name="text-xs font-light text-muted-foreground",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex flex-row items-start gap-x-3 cursor-pointer",
        )

    return card.root(
        card.header(
            card.title("Notifications"),
            card.description("Choose what you want to be notified about."),
        ),
        card.content(
            rx.el.div(
                rx.el.div(
                    *[checkbox_row(item) for item in notification_items],
                    class_name="w-full flex flex-col gap-y-4",
                ),
                class_name="flex flex-col",
            )
        ),
        card.footer(
            button(
                "Save Preferences", variant="default", size="sm", class_name="w-full"
            ),
            class_name="w-full",
        ),
        class_name="mx-auto w-full max-w-sm shadow-sm",
    )
