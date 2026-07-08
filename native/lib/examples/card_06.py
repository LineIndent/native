import reflex as rx

from components.core.hugeicon import hi
from components.ui.button import button
from components.ui.card import card
from components.ui.input import input
from components.ui.input_group import input_group
from native.templates.masonary import masonry_card

members = [
    {"email": "alex@example.com", "role": "editor"},
    {"email": "sam@example.com", "role": "viewer"},
]


@masonry_card(label="General")
def card_06() -> rx.Component:

    def member_row(member: dict) -> rx.Component:
        return rx.el.div(
            input(
                default_value=member["email"],
                class_name="flex-1",
            ),
            class_name="w-full flex flex-row items-center gap-x-2",
        )

    return card.root(
        card.header(
            card.title("Invite Team"),
            card.description("Add members to your workspace"),
        ),
        card.content(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        *[member_row(m) for m in members],
                        class_name="w-full flex flex-col gap-y-2",
                    ),
                    button(
                        hi("PlusSignIcon", class_name="size-3.5"),
                        "Add another",
                        variant="outline",
                        size="sm",
                        class_name="w-full",
                    ),
                    class_name="flex flex-col gap-y-3",
                ),
                rx.el.div(class_name="w-full h-px bg-input my-1"),
                rx.el.div(
                    rx.el.p(
                        "Or share invite link",
                        class_name="text-sm font-semibold text-foreground",
                    ),
                    input_group.root(
                        input_group.input(
                            placeholder="https://app.co/invite/x8f2k",
                            read_only=True,
                        ),
                        input_group.addon(
                            input_group.button(
                                hi("Copy01Icon"),
                                aria_label="Copy",
                                title="Copy",
                                size="icon-xs",
                            ),
                            align="inline-end",
                        ),
                    ),
                    class_name="w-full flex flex-col gap-y-2",
                ),
                class_name="w-full flex flex-col gap-y-4",
            )
        ),
        card.footer(
            button("Send Invites", size="sm", class_name="w-full"),
            class_name="w-full",
        ),
        class_name="mx-auto w-full max-w-sm",
    )
