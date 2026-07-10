import reflex as rx

from components.ui.select import select


def select_sizes() -> rx.Component:
    return rx.el.div(
        select(
            select.option("Small", value="sm"),
            select.option("Medium", value="md"),
            select.option("Large", value="lg"),
            default_value="md",
            size="sm",
        ),
        select(
            select.option("Small", value="sm"),
            select.option("Medium", value="md"),
            select.option("Large", value="lg"),
            default_value="md",
        ),
        class_name="mx-auto flex max-w-sm items-center gap-4",
    )
