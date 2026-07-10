import reflex as rx

from components.ui.field import field
from components.ui.select import select


def select_disabled() -> rx.Component:
    return rx.el.div(
        field.root(
            field.label("Country", html_for="country-disabled"),
            select(
                select.option("United States", value="us"),
                select.option("Canada", value="ca"),
                select.option("Mexico", value="mx"),
                id="country-disabled",
                default_value="us",
                disabled=True,
                wrapper_class_name="w-full",
            ),
            field.description("This field is currently locked."),
        ),
        class_name="mx-auto max-w-sm",
    )
