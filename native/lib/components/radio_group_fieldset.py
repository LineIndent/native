import reflex as rx

from components.ui.field import field
from components.ui.radio_group import radio_group

PLANS = [
    ("monthly", "Monthly ($9.99/month)"),
    ("yearly", "Yearly ($99.99/year)"),
    ("lifetime", "Lifetime ($299.99)"),
]


def radio_group_fieldset() -> rx.Component:
    return field.set(
        field.legend("Subscription Plan", variant="label"),
        field.description("Yearly and lifetime plans offer significant savings."),
        radio_group.root(
            *[
                field.root(
                    radio_group.item(
                        name="plan",
                        value=value,
                        id=f"plan-{value}",
                        default_checked=(value == "monthly"),
                    ),
                    field.label(
                        label, html_for=f"plan-{value}", class_name="font-normal"
                    ),
                    orientation="horizontal",
                )
                for value, label in PLANS
            ],
        ),
        class_name="w-full max-w-xs",
    )
