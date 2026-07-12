import reflex as rx

from components.ui.button import button
from components.ui.card import card
from native.templates.masonary import masonry_card

savings_goals = [
    {
        "category": "RETIREMENT",
        "target": "$420,000",
        "percent": 65,
        "achieved": "$273,000",
    },
    {
        "category": "REAL ESTATE",
        "target": "$85,000",
        "percent": 32,
        "achieved": "$27,200",
    },
]


@masonry_card(label="Finance")
def card_04() -> rx.Component:

    def goal_item(goal: dict) -> rx.Component:
        return rx.el.div(
            rx.el.div(
                rx.el.p(
                    goal["category"],
                    class_name="text-xs font-semibold tracking-widest text-muted-foreground uppercase",
                ),
                rx.el.p(
                    goal["target"],
                    class_name="text-4xl font-bold tracking-tight text-foreground",
                ),
                class_name="flex flex-col gap-y-1",
            ),
            rx.el.div(
                rx.el.div(
                    class_name="h-full bg-primary rounded-lg",
                    style={"width": f"{goal['percent']}%"},
                ),
                class_name="w-full h-1 bg-input rounded-lg overflow-hidden",
            ),
            rx.el.div(
                rx.el.p(
                    f"{goal['percent']}% achieved",
                    class_name="text-sm font-light text-muted-foreground",
                ),
                rx.el.p(
                    goal["achieved"],
                    class_name="text-sm font-medium text-foreground",
                ),
                class_name="w-full flex flex-row items-center justify-between",
            ),
            class_name="w-full flex flex-col gap-y-3 bg-secondary rounded-lg p-4",
        )

    return card.root(
        card.header(
            rx.el.div(
                rx.el.p(
                    "Savings Targets",
                    class_name="text-lg font-semibold text-foreground",
                ),
                rx.el.p(
                    "Active milestones for 2024",
                    class_name="text-sm font-light text-muted-foreground",
                ),
                class_name="flex flex-col gap-y-0.5",
            ),
            button("New Goal", variant="outline"),
            class_name="w-full flex flex-row items-start justify-between",
        ),
        card.content(
            rx.el.div(
                *[goal_item(g) for g in savings_goals],
                class_name="w-full flex flex-col gap-y-3",
            )
        ),
        card.footer(
            rx.el.p(
                "You have not met your targets for this year.",
                class_name="text-sm font-light text-muted-foreground",
            ),
            class_name="w-full",
        ),
        class_name="mx-auto w-full max-w-sm",
    )
