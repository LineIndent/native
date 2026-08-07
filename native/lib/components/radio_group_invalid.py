import reflex as rx

from components.ui.field import field
from components.ui.radio_group import radio_group

OPTIONS = [
    ("email", "invalid-email", "Email only"),
    ("sms", "invalid-sms", "SMS only"),
    ("both", "invalid-both", "Both Email & SMS"),
]


def radio_group_invalid() -> rx.Component:
    return field.set(
        field.legend("Notification Preferences", variant="label"),
        field.description("Choose how you want to receive notifications."),
        radio_group.root(
            *[
                field.root(
                    radio_group.item(
                        name="notification-preferences",
                        value=value,
                        id_=id_,
                        default_checked=(value == "email"),
                        aria_invalid=True,
                    ),
                    field.label(label, html_for=id_, class_name="font-normal"),
                    orientation="horizontal",
                    data_invalid=True,
                )
                for value, id_, label in OPTIONS
            ],
        ),
        class_name="w-full max-w-xs",
    )
