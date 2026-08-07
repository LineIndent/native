import reflex as rx

from components.ui.field import field
from components.ui.radio_group import radio_group

PLANS = [
    ("plus", "Plus", "For individuals and small teams."),
    ("pro", "Pro", "For growing businesses."),
    ("enterprise", "Enterprise", "For large teams and enterprises."),
]


def radio_group_choice_card() -> rx.Component:
    return radio_group.root(
        *[
            field.label(
                field.root(
                    field.content(
                        field.title(title),
                        field.description(description),
                    ),
                    radio_group.item(
                        name="plan",
                        value=value,
                        id=f"{value}-plan",
                        default_checked=(value == "plus"),
                    ),
                    orientation="horizontal",
                ),
                html_for=f"{value}-plan",
            )
            for value, title, description in PLANS
        ],
        class_name="max-w-sm",
    )
