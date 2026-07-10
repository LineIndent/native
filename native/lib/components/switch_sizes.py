# import reflex as rx
# from components.ui.field import field
# from components.ui.switch import switch

# def switch_sizes() -> rx.Component:
#     return field.group(
#         field.root(
#             field.label(
#                 "Testing",
#                 switch.root(id="test-plan"),
#                 html_for="test-plan",
#             ),
#         ),
#         field.root(
#             field.label(
#                 switch.root(id="size-sm", size="sm"),
#                 "Small Tweak", html_for="size-sm", class_name="text-xs w-full",
#             ),
#             orientation="horizontal",
#         ),
#         # field.root(
#         #     switch.root(id="size-default", size="default"),
#         #     field.label("Default Scale", html_for="size-default"),
#         #     orientation="horizontal",
#         # ),
#         class_name="w-full flex justify-center items-center"
#     )

import reflex as rx

from components.ui.field import field
from components.ui.switch import switch


def switch_sizes() -> rx.Component:
    return field.group(
        field.root(
            switch.root(
                id="switch-size-sm",
                size="sm",
            ),
            field.label(
                "Small",
                html_for="switch-size-sm",
            ),
            orientation="horizontal",
        ),
        field.root(
            switch.root(
                id="switch-size-default",
                size="default",
            ),
            field.label(
                "Default",
                html_for="switch-size-default",
            ),
            orientation="horizontal",
        ),
        class_name="w-full max-w-[10rem]",
    )
