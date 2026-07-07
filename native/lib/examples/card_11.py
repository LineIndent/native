import reflex as rx

from components.button import button
from components.card import card
from components.hugeicon import hi
from components.input_group import input_group
from native.templates.masonary import masonry_card

summary_rows = [
    {"label": "Estimated arrival", "value": "Today, Apr 14", "bold": False},
    {"label": "Transaction fee", "value": "$0.00", "bold": False},
    {"label": "Total amount", "value": "$1,200.00", "bold": True},
]


@masonry_card(label="Finance")
def card_11() -> rx.Component:

    return card.root(
        card.header(
            rx.el.div(
                rx.el.p(
                    "Transfer Funds", class_name="text-lg font-semibold text-foreground"
                ),
                rx.el.p(
                    "Move money between your connected accounts.",
                    class_name="text-sm font-light text-muted-foreground",
                ),
                class_name="flex flex-col gap-y-1",
            ),
            button(
                hi("Cancel01Icon", class_name="size-4"),
                variant="ghost",
                size="sm",
                class_name="!px-2 !py-2 self-start",
            ),
            class_name="w-full flex flex-row items-start justify-between",
        ),
        card.content(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Amount to Transfer",
                        class_name="text-sm font-semibold text-foreground",
                    ),
                    input_group.root(
                        input_group.addon(
                            input_group.text("$"),
                            align="inline-start",
                        ),
                        input_group.input(placeholder="0.00"),
                        input_group.addon(
                            input_group.text("USD"),
                            align="inline-end",
                        ),
                    ),
                    class_name="w-full flex flex-col gap-y-2 relative",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "From Account",
                            class_name="text-sm font-semibold text-foreground",
                        ),
                        rx.el.select(
                            rx.el.option(
                                "Main Checking (--8402) — $12,450.00", value="checking"
                            ),
                            rx.el.option(
                                "Business Account (--3301) — $5,200.00",
                                value="business",
                            ),
                            class_name=(
                                "w-full rounded-lg border border-input bg-secondary "
                                "px-3 py-2 text-sm text-foreground appearance-none cursor-pointer "
                                "focus:outline-none focus:ring-1 focus:ring-input"
                            ),
                        ),
                        class_name="w-full flex flex-col gap-y-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "To Account",
                            class_name="text-sm font-semibold text-foreground",
                        ),
                        rx.el.select(
                            rx.el.option(
                                "High Yield Savings (··1192) — $42,100.00",
                                value="savings",
                            ),
                            rx.el.option("Roth IRA (··7745) — $18,300.00", value="ira"),
                            class_name=(
                                "w-full rounded-lg border border-input bg-secondary "
                                "px-3 py-2 text-sm text-foreground appearance-none cursor-pointer "
                                "focus:outline-none focus:ring-1 focus:ring-input"
                            ),
                        ),
                        class_name="w-full flex flex-col gap-y-2",
                    ),
                    class_name="flex flex-col gap-y-3",
                ),
                rx.el.div(
                    *[
                        rx.el.div(
                            rx.el.p(
                                row["label"],
                                class_name=f"text-sm text-muted-foreground {'font-semibold text-foreground' if row['bold'] else 'font-light'}",
                            ),
                            rx.el.p(
                                row["value"],
                                class_name=f"text-sm {'font-bold text-foreground' if row['bold'] else 'font-medium text-foreground'}",
                            ),
                            class_name="w-full flex flex-row items-center justify-between py-2.5 border-b border-input last:border-b-0",
                        )
                        for row in summary_rows
                    ],
                    class_name="w-full flex flex-col rounded-lg border border-input px-3",
                ),
                class_name="flex flex-col gap-y-4",
            )
        ),
        card.footer(
            button(
                "Confirm Transfer", variant="default", size="sm", class_name="w-full"
            ),
            class_name="w-full",
        ),
        class_name="mx-auto w-full max-w-sm shadow-sm",
    )
