import reflex as rx

from components.ui.field import field
from components.ui.switch import switch


def switch_with_label() -> rx.Component:
    return field.label(
        rx.el.div(
            field.content(
                field.title("Enterprise Pipeline"),
                field.description(
                    "Deploy dedicated runners, isolated networks, and unlimited concurrency."
                ),
            ),
            switch.root(id="enterprise-plan"),
            class_name="flex items-start justify-between gap-4 max-w-sm",
        ),
        html_for="enterprise-plan",
    )
