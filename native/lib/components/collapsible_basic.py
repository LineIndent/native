import reflex as rx

from components.core.core import cn
from components.core.hugeicon import hi
from components.ui.button import button_variants
from components.ui.collapsible import collapsible


def collapsible_basic() -> rx.Component:
    return rx.el.div(
        collapsible.root(
            collapsible.trigger(
                rx.el.div(
                    rx.el.p("How do I update my billing information?"),
                    hi(
                        "ArrowDown01Icon",
                        class_name="size-4 ml-auto [details[open]>summary_&]:rotate-180",
                    ),
                    class_name="w-full flex flex-row items-center justify-between",
                ),
                class_name=cn(
                    "w-full py-3 text-left border-b border-input",
                    button_variants(variant="ghost"),
                ),
            ),
            collapsible.panel(
                rx.el.div(
                    "You can update your card details directly inside your account settings dashboard under the billing tab.",
                    class_name="py-3 text-sm text-muted-foreground leading-relaxed px-3",
                ),
            ),
            default_open=False,
        ),
        class_name="w-full max-w-sm",
    )
