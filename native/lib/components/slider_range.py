import reflex as rx

from components.ui.slider import slider


def slider_range():
    return rx.el.div(
        slider.root(
            slider.input(
                default_value=[25, 50],
                min=0,
                max=100,
                step=5,
            ),
        ),
        class_name="w-full max-w-xs mx-auto flex justify-center",
    )
