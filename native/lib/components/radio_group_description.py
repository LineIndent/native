import reflex as rx

from components.ui.field import field
from components.ui.radio_group import radio_group

OPTIONS = [
    ("default", "Default", "Standard spacing for most use cases."),
    ("comfortable", "Comfortable", "More space between elements."),
    ("compact", "Compact", "Minimal spacing for dense layouts."),
]


def radio_group_description() -> rx.Component:
    return radio_group.root(
        *[
            field.root(
                radio_group.item(
                    name="spacing",
                    value=value,
                    id=f"desc-{value}",
                    default_checked=(value == "comfortable"),
                ),
                field.content(
                    field.label(title, html_for=f"desc-{value}"),
                    field.description(description),
                ),
                orientation="horizontal",
            )
            for value, title, description in OPTIONS
        ],
        class_name="w-fit",
    )
