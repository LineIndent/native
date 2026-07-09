import reflex as rx
from components.ui.slider import slider


def slider_vertical():
    return rx.el.div(
        slider.root(
            slider.input(
                default_value=50,
                min=0,
                max=100,
                step=1,
            ),
            orientation="vertical",
            class_name="h-40",
        ),
        slider.root(
            slider.input(
                default_value=25,
                min=0,
                max=100,
                step=1,
            ),
            orientation="vertical",
            class_name="h-40",
        ),
        class_name="h-full mx-auto flex w-full max-w-xs items-center justify-center gap-6",
    )
