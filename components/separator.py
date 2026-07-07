from typing import Literal

import reflex as rx

from .core import CoreComponent

LiteralOrientation = Literal["horizontal", "vertical"]


class ClassNames:
    SEPARATOR = (
        "shrink-0 bg-input "
        "data-[orientation=horizontal]:h-px data-[orientation=horizontal]:w-full "
        "data-[orientation=vertical]:w-px data-[orientation=vertical]:self-stretch"
    )


class SeparatorComponent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        orientation: str = props.pop("orientation", "horizontal")
        decorative = props.pop("decorative", True)
        data_slot = props.pop("data_slot", "separator")

        props["data-slot"] = data_slot
        props["data-orientation"] = orientation

        if decorative:
            props["aria-hidden"] = "true"
        else:
            props["role"] = "separator"
            props["aria-orientation"] = orientation

        cls.set_class_name(ClassNames.SEPARATOR, props)
        return rx.el.div(*children, **props)


separator = SeparatorComponent.create
