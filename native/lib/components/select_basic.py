import reflex as rx

from components.ui.field import field
from components.ui.select import select


def select_basic() -> rx.Component:
    return rx.el.div(
        field.root(
            field.label("Favorite fruit", html_for="fruit-basic"),
            select(
                select.option("Apple", value="apple"),
                select.option("Banana", value="banana"),
                select.option("Blueberry", value="blueberry"),
                select.option("Grapes", value="grapes"),
                select.option("Pineapple", value="pineapple"),
                id="fruit-basic",
                name="fruit",
                default_value="apple",
                wrapper_class_name="w-full",
            ),
        ),
        class_name="mx-auto max-w-sm",
    )
