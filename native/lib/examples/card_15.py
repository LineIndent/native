import reflex as rx

from components.ui.card import card
from native.templates.masonary import masonry_card


@masonry_card(label="General")
def card_15() -> rx.Component:
    colors = [
        {"bg": "bg-background", "label": "-background", "border": True},
        {"bg": "bg-foreground", "label": "-foreground"},
        {"bg": "bg-primary", "label": "-primary"},
        {"bg": "bg-secondary", "label": "-secondary", "border": True},
        {"bg": "bg-muted", "label": "-muted", "border": True},
        {"bg": "bg-accent", "label": "-accent", "border": True},
        {"bg": "bg-border", "label": "-border", "border": True},
        {"bg": "bg-chart-1", "label": "-chart-1"},
        {"bg": "bg-chart-2", "label": "-chart-2"},
        {"bg": "bg-chart-3", "label": "-chart-3"},
        {"bg": "bg-chart-4", "label": "-chart-4"},
        {"bg": "bg-chart-5", "label": "-chart-5"},
    ]

    def swatch(color: dict) -> rx.Component:
        border_class = "border border-input" if color.get("border") else ""
        return rx.el.div(
            rx.el.div(
                class_name=f"rounded-lg {color['bg']} {border_class} size-12 flex-shrink-0",
            ),
            rx.el.p(
                color["label"],
                class_name="text-xs text-muted-foreground font-theme truncate w-full text-center",
            ),
            class_name="flex flex-col items-center gap-y-2 flex-1 min-w-0",
        )

    rows = [colors[:6], colors[6:]]

    return card.root(
        card.header(
            card.title(
                "Theme Colors",
                class_name="text-lg font-semibold text-foreground text-center",
            ),
            card.description(
                "Dynamic palette variants",
                class_name="text-sm font-light text-muted-foreground text-center",
            ),
        ),
        card.content(
            rx.el.div(
                *[
                    rx.el.div(
                        *[swatch(c) for c in row],
                        class_name="w-full flex flex-row gap-x-2",
                    )
                    for row in rows
                ],
                class_name="flex flex-col gap-y-4",
            ),
        ),
        class_name="mx-auto w-full max-w-sm",
    )
