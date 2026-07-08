from typing import Literal

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn

LiteralOrientation = Literal["horizontal", "vertical"]


class ClassNames:
    ROOT = (
        "flex max-w-64 w-full items-center select-none "
        "data-[orientation=vertical]:h-64 data-[orientation=vertical]:w-auto"
    )

    INPUT = (
        "w-full h-1 appearance-none rounded-lg bg-secondary cursor-pointer "
        "disabled:cursor-not-allowed disabled:opacity-50 "
        "focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/50 "
        # thumb
        "[&::-webkit-slider-thumb]:appearance-none "
        "[&::-webkit-slider-thumb]:size-3 "
        "[&::-webkit-slider-thumb]:rounded-full "
        "[&::-webkit-slider-thumb]:bg-white "
        "[&::-webkit-slider-thumb]:outline [&::-webkit-slider-thumb]:outline-1 [&::-webkit-slider-thumb]:outline-black "
        "[&::-webkit-slider-thumb]:transition-[height,width] "
        "hover:[&::-webkit-slider-thumb]:size-4.5 "
        "[&::-moz-range-thumb]:size-3 "
        "[&::-moz-range-thumb]:rounded-full "
        "[&::-moz-range-thumb]:border-0 "
        "[&::-moz-range-thumb]:bg-white "
        "[&::-moz-range-thumb]:outline [&::-moz-range-thumb]:outline-1 [&::-moz-range-thumb]:outline-black "
        # track (webkit needs explicit transparent track, moz fills automatically via range-progress below)
        "[&::-webkit-slider-runnable-track]:h-1 "
        "[&::-webkit-slider-runnable-track]:rounded-lg "
        "[&::-webkit-slider-runnable-track]:bg-transparent "
        "[&::-moz-range-track]:h-1 "
        "[&::-moz-range-track]:rounded-lg "
        "[&::-moz-range-track]:bg-secondary "
        "[&::-moz-range-progress]:h-1 "
        "[&::-moz-range-progress]:rounded-lg "
        "[&::-moz-range-progress]:bg-primary"
    )

    VALUE = "text-sm text-primary font-medium"


class SliderRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        orientation = props.pop("orientation", "horizontal")
        props["data-slot"] = "slider"
        props["data-orientation"] = orientation
        cls.set_class_name(cn(ClassNames.ROOT, custom_classes), props)
        return rx.el.div(*children, **props)


class SliderInput(CoreComponent):
    @classmethod
    def create(cls, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        default_value = props.get("default_value", props.get("value"))
        min_val = props.get("min", 0)
        max_val = props.get("max", 100)

        props.setdefault("type", "range")
        props.setdefault("min", min_val)
        props.setdefault("max", max_val)
        props["data-slot"] = "slider-input"

        # one-time percentage fill for Chrome/Edge/Safari (static, non-reactive)
        if isinstance(default_value, (int, float)):
            try:
                pct = (
                    (float(default_value) - float(min_val))
                    / (float(max_val) - float(min_val))
                    * 100
                )
                props["style"] = {
                    "background": f"linear-gradient(to right, var(--primary) {pct}%, var(--secondary) {pct}%)",
                    **props.get("style", {}),
                }
            except ZeroDivisionError:
                pass

        cls.set_class_name(cn(ClassNames.INPUT, custom_classes), props)
        return rx.el.input(**props)


class SliderValue(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "slider-value"
        cls.set_class_name(ClassNames.VALUE, props)
        return rx.el.span(*children, **props)


class Slider(ComponentNamespace):
    root = staticmethod(SliderRoot.create)
    input = staticmethod(SliderInput.create)
    value = staticmethod(SliderValue.create)
    class_names = ClassNames


slider = Slider()
