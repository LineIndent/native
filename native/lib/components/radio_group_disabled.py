import reflex as rx

from components.ui.field import field
from components.ui.radio_group import radio_group

OPTIONS = [
    ("option1", "disabled-1", "Disabled", True),
    ("option2", "disabled-2", "Option 2", False),
    ("option3", "disabled-3", "Option 3", False),
]


def radio_group_disabled() -> rx.Component:
    return radio_group.root(
        *[
            field.root(
                radio_group.item(
                    name="disabled-demo",
                    value=value,
                    id=id_,
                    disabled=is_disabled,
                    default_checked=(value == "option2"),
                ),
                field.label(label, html_for=id_, class_name="font-normal"),
                orientation="horizontal",
                **({"data-disabled": "true"} if is_disabled else {}),
            )
            for value, id_, label, is_disabled in OPTIONS
        ],
        class_name="w-fit",
    )
