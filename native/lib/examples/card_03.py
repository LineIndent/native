import reflex as rx

from components.ui.card import card
from native.templates.masonary import masonry_card

summary_rows = [
    {"label": "Net Royalties", "value": "$0.00", "bold": False, "divider": False},
    {"label": "Processing Fee", "value": "-$0.00", "bold": False, "divider": True},
    {
        "label": "Total Ready to Claim",
        "value": "$0.00 USD",
        "bold": True,
        "divider": False,
    },
]


@masonry_card(label="Finance")
def card_03() -> rx.Component:

    return card.root(
        card.header(
            rx.el.div(
                rx.el.p(
                    "Claimable Balance",
                    class_name="text-sm font-light text-muted-foreground",
                ),
                rx.el.p(
                    "$0.00",
                    class_name="text-5xl font-bold tracking-tight text-foreground",
                ),
                class_name="flex flex-col gap-y-1",
            ),
            rx.el.div(
                rx.el.div(class_name="size-2 rounded-full bg-yellow-400 shrink-0"),
                rx.el.p(
                    "Pending Setup",
                    class_name="text-xs font-medium text-foreground",
                ),
                class_name="flex flex-row items-center gap-x-2 px-3 py-1.5 rounded-lg border border-input bg-secondary w-fit",
            ),
            class_name="w-full flex flex-col gap-y-3",
        ),
        card.content(
            rx.el.div(
                *[
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                row["label"],
                                class_name="text-sm text-muted-foreground font-light",
                            ),
                            rx.el.p(
                                row["value"],
                                class_name=f"text-sm {'font-bold text-foreground' if row['bold'] else 'font-medium text-foreground'}",
                            ),
                            class_name="w-full flex flex-row items-center justify-between py-2.5",
                        ),
                        rx.el.div(class_name="w-full h-px bg-input")
                        if row["divider"]
                        else rx.fragment(),
                        class_name="w-full flex flex-col",
                    )
                    for row in summary_rows
                ],
                class_name="w-full flex flex-col bg-secondary rounded-lg px-3",
            ),
            class_name="w-full flex flex-col gap-y-3",
        ),
        card.footer(
            rx.el.p(
                "Once your bank is connected, balances over $10.00 are automatically "
                "eligible for monthly distribution on the 15th of each month.",
                class_name="text-sm font-light text-muted-foreground leading-relaxed",
            ),
            class_name="w-full",
        ),
        class_name="mx-auto w-full max-w-sm",
    )
