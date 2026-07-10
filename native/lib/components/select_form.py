import reflex as rx

from components.ui.field import field
from components.ui.select import select


def select_form() -> rx.Component:
    return field.set(
        field.legend("Shipping details"),
        field.group(
            field.root(
                field.label("Country", html_for="shipping-country"),
                select(
                    select.option("United States", value="us"),
                    select.option("Canada", value="ca"),
                    select.option("United Kingdom", value="uk"),
                    select.option("Germany", value="de"),
                    id="shipping-country",
                    name="country",
                    default_value="us",
                    wrapper_class_name="w-full",
                ),
            ),
            field.root(
                field.label("Timezone", html_for="shipping-timezone"),
                select(
                    select.option("Pacific Time (PT)", value="pt"),
                    select.option("Mountain Time (MT)", value="mt"),
                    select.option("Central Time (CT)", value="ct"),
                    select.option("Eastern Time (ET)", value="et"),
                    id="shipping-timezone",
                    name="timezone",
                    default_value="et",
                    wrapper_class_name="w-full",
                ),
            ),
        ),
        class_name="mx-auto max-w-sm",
    )
