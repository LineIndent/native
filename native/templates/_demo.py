import reflex as rx

from components.accordion import accordion
from native.templates._copy_btn import create_copy_button


def demo(component: rx.Component, source: str) -> rx.Component:

    return rx.el.div(
        rx.el.div(
            component,
            class_name="w-full min-h-[250px] flex items-center justify-center !p-2 !sm:p-6 my-10",
        ),
        rx.el.div(
            rx.el.div(
                create_copy_button(content=source),
                class_name="absolute top-2 right-2 z-10 bg-secondary dark:bg-card",
            ),
            rx.el.div(
                rx.el.pre(
                    rx.el.code(
                        source,
                        class_name="language-python !text-[15px]",
                        on_mount=rx.call_script("Prism.highlightAll()"),
                    ),
                    style={
                        "padding": "1rem 0.75rem",
                        "white-space": "pre",
                        "display": "block",
                    },
                    class_name="w-full h-full !bg-secondary dark:!bg-card",
                ),
                class_name="max-h-[150px] overflow-auto scrollbar-none",
            ),
            class_name="border-t border-input/80 bg-secondary dark:bg-card relative overflow-hidden",
        ),
        class_name="w-full border border-input/80 flex flex-col mb-8 !overflow-hidden",
    )
