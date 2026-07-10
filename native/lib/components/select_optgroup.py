import reflex as rx

from components.ui.field import field
from components.ui.select import select


def select_optgroup() -> rx.Component:
    return rx.el.div(
        field.root(
            field.label("Ingredient", html_for="ingredient-select"),
            select(
                select.option(
                    "Select an ingredient", value="", disabled=True, hidden=True
                ),
                select.optgroup(
                    select.option("Apple", value="apple"),
                    select.option("Banana", value="banana"),
                    select.option("Blueberry", value="blueberry"),
                    label="Fruits",
                ),
                select.optgroup(
                    select.option("Carrot", value="carrot"),
                    select.option("Potato", value="potato"),
                    select.option("Broccoli", value="broccoli"),
                    label="Vegetables",
                ),
                id="ingredient-select",
                name="ingredient",
                default_value="",
                wrapper_class_name="w-full",
            ),
        ),
        class_name="mx-auto max-w-sm",
    )
