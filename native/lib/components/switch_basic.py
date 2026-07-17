import reflex as rx

from components.ui.field import field
from components.ui.switch import switch


def switch_basic() -> rx.Component:
    return field.root(
        field.content(
            field.title("Strict Mode"),
            field.description(
                "Enable strict validation protocols across all incoming API payloads."
            ),
        ),
        switch.root(id="strict-mode"),
        orientation="horizontal",
        class_name="justify-between items-center border rounded-lg p-4 w-full max-w-md",
    )
