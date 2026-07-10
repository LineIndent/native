---
title: "Slider"
description: "An input where the user selects a value from within a given range."
order: 20
---


## Slider, An Input Where The User Selects A Value From Within A Given Range.


```python
from components.ui.slider import Slider
```

```python
from typing import Any

from reflex.components.component import Component
from reflex.utils.imports import ImportVar
from reflex.vars import FunctionVar, Var
from reflex.vars.base import VarData

PACKAGE_CN = "clsx-for-tailwind@1.0.0"
CN = Var(
    "cn",
    _var_data=VarData(
        imports={
            PACKAGE_CN: ImportVar(tag="cn"),
        },
    ),
).to(FunctionVar)


class CoreComponent(Component):
    unstyled: Var[bool]

    @classmethod
    def set_class_name(
        cls, default_class_name: str | Var[str], props: dict[str, Any]
    ) -> None:

        if "render_" in props:
            return

        props_class_name = props.get("class_name", "")

        if props.pop("unstyled", False):
            props["class_name"] = props_class_name
            return

        props["class_name"] = cn(default_class_name, props_class_name)

    def _exclude_props(self) -> list[str]:
        return [
            *super()._exclude_props(),
            "unstyled",
        ]


def cn(*classes: Var | str | tuple | list | None) -> Var:
    return CN.call(*classes).to(str)
```

```python
# import uuid
# from typing import Literal

# import reflex as rx
# from reflex.components.component import ComponentNamespace

# from ..core.core import CoreComponent, cn

# LiteralOrientation = Literal["horizontal", "vertical"]


# class ClassNames:
#     ROOT = (
#         "flex max-w-64 w-full items-center select-none "
#         "data-[orientation=vertical]:h-64 data-[orientation=vertical]:w-auto"
#     )

#     INPUT = (
#         "w-full h-1 appearance-none rounded-lg bg-secondary cursor-pointer "
#         "disabled:cursor-not-allowed disabled:opacity-50 "
#         "focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/50 "
#         # thumb
#         "[&::-webkit-slider-thumb]:appearance-none "
#         "[&::-webkit-slider-thumb]:size-3 "
#         "[&::-webkit-slider-thumb]:rounded-full "
#         "[&::-webkit-slider-thumb]:bg-white "
#         "[&::-webkit-slider-thumb]:outline [&::-webkit-slider-thumb]:outline-1 [&::-webkit-slider-thumb]:outline-black "
#         "[&::-webkit-slider-thumb]:transition-[height,width] "
#         "hover:[&::-webkit-slider-thumb]:size-4.5 "
#         "[&::-moz-range-thumb]:size-3 "
#         "[&::-moz-range-thumb]:rounded-full "
#         "[&::-moz-range-thumb]:border-0 "
#         "[&::-moz-range-thumb]:bg-white "
#         "[&::-moz-range-thumb]:outline [&::-moz-range-thumb]:outline-1 [&::-moz-range-thumb]:outline-black "
#         # track (webkit needs explicit transparent track, moz fills automatically via range-progress below)
#         "[&::-webkit-slider-runnable-track]:h-1 "
#         "[&::-webkit-slider-runnable-track]:rounded-lg "
#         "[&::-webkit-slider-runnable-track]:bg-transparent "
#         "[&::-moz-range-track]:h-1 "
#         "[&::-moz-range-track]:rounded-lg "
#         "[&::-moz-range-track]:bg-secondary "
#         "[&::-moz-range-progress]:h-1 "
#         "[&::-moz-range-progress]:rounded-lg "
#         "[&::-moz-range-progress]:bg-primary"
#     )

#     VALUE = "text-sm text-primary font-medium"


# class SliderRoot(CoreComponent):
#     @classmethod
#     def create(cls, *children, **props) -> rx.Component:
#         custom_classes = props.pop("class_name", "")
#         orientation = props.pop("orientation", "horizontal")
#         props["data-slot"] = "slider"
#         props["data-orientation"] = orientation
#         cls.set_class_name(cn(ClassNames.ROOT, custom_classes), props)
#         return rx.el.div(*children, **props)


# class SliderInput(CoreComponent):
#     @classmethod
#     def create(cls, **props) -> rx.Component:
#         custom_classes = props.pop("class_name", "")
#         default_value = props.get("default_value", props.get("value"))
#         min_val = props.get("min", 0)
#         max_val = props.get("max", 100)

#         props.setdefault("type", "range")
#         props.setdefault("min", min_val)
#         props.setdefault("max", max_val)
#         props["data-slot"] = "slider-input"

#         input_id = props.get("id") or f"slider-input-{uuid.uuid4().hex[:8]}"
#         props["id"] = input_id

#         # initial percentage fill for Chrome/Edge/Safari, so the track shows
#         # the right fill on first paint before any interaction
#         if isinstance(default_value, (int, float)):
#             try:
#                 pct = (
#                     (float(default_value) - float(min_val))
#                     / (float(max_val) - float(min_val))
#                     * 100
#                 )
#                 props["style"] = {
#                     "background": f"linear-gradient(to right, var(--primary) {pct}%, var(--secondary) {pct}%)",
#                     **props.get("style", {}),
#                 }
#             except ZeroDivisionError:
#                 pass

#         # keep the fill LIVE while dragging. Firefox does this for free via
#         # ::-moz-range-progress, but Chrome/Safari have no equivalent
#         # pseudo-element — without this, the static style above only ever
#         # reflects default_value, so the visible fill freezes the instant
#         # you start dragging even though the thumb keeps moving.
#         existing_on_mount = props.pop("on_mount", None)
#         live_fill_script = rx.call_script(
#             f"""
#             (function() {{
#                 var el = document.getElementById('{input_id}');
#                 if (!el || el.__sliderFillAttached) return;
#                 el.__sliderFillAttached = true;
#                 var min = parseFloat(el.min || 0);
#                 var max = parseFloat(el.max || 100);
#                 el.addEventListener('input', function () {{
#                     var pct = ((parseFloat(el.value) - min) / (max - min)) * 100;
#                     el.style.background =
#                         'linear-gradient(to right, var(--primary) ' + pct +
#                         '%, var(--secondary) ' + pct + '%)';
#                 }});
#             }})()
#             """
#         )
#         if existing_on_mount is not None:
#             events = (
#                 existing_on_mount
#                 if isinstance(existing_on_mount, list)
#                 else [existing_on_mount]
#             )
#             props["on_mount"] = [*events, live_fill_script]
#         else:
#             props["on_mount"] = live_fill_script

#         cls.set_class_name(cn(ClassNames.INPUT, custom_classes), props)
#         return rx.el.input(**props)


# class SliderValue(CoreComponent):
#     @classmethod
#     def create(cls, *children, **props) -> rx.Component:
#         props["data-slot"] = "slider-value"
#         cls.set_class_name(ClassNames.VALUE, props)
#         return rx.el.span(*children, **props)


# class Slider(ComponentNamespace):
#     root = staticmethod(SliderRoot.create)
#     input = staticmethod(SliderInput.create)
#     value = staticmethod(SliderValue.create)
#     class_names = ClassNames


# slider = Slider()

import uuid
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

        input_id = props.get("id") or f"slider-input-{uuid.uuid4().hex[:8]}"
        props["id"] = input_id

        # initial percentage fill for Chrome/Edge/Safari, so the track shows
        # the right fill on first paint before any interaction
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

        # keep the fill LIVE while dragging. Firefox does this for free via
        # ::-moz-range-progress, but Chrome/Safari have no equivalent
        # pseudo-element — without this, the static style above only ever
        # reflects default_value, so the visible fill freezes the instant
        # you start dragging even though the thumb keeps moving.
        existing_on_mount = props.pop("on_mount", None)
        live_fill_script = rx.call_script(
            f"""
            (function() {{
                var el = document.getElementById('{input_id}');
                if (!el || el.__sliderFillAttached) return;
                el.__sliderFillAttached = true;
                var min = parseFloat(el.min || 0);
                var max = parseFloat(el.max || 100);
                el.addEventListener('input', function () {{
                    var pct = ((parseFloat(el.value) - min) / (max - min)) * 100;
                    el.style.background =
                        'linear-gradient(to right, var(--primary) ' + pct +
                        '%, var(--secondary) ' + pct + '%)';
                }});
            }})()
            """
        )
        if existing_on_mount is not None:
            events = (
                existing_on_mount
                if isinstance(existing_on_mount, list)
                else [existing_on_mount]
            )
            props["on_mount"] = [*events, live_fill_script]
        else:
            props["on_mount"] = live_fill_script

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
```

# Examples

## Basic
A basic low-level slider demo.
```python
def slider_demo():
    return rx.el.div(
        slider.root(
            slider.input(default_value=20),
        ),
        class_name="w-full max-w-md flex justify-center",
    )
```

## Range
Use an array with two values for a range slider.
```python
def slider_range():
    return rx.el.div(
        slider.root(
            slider.input(
                default_value=35,
                min=0,
                max=100,
                step=5,
            ),
        ),
        class_name="w-full max-w-xs mx-auto flex justify-center",
    )
```

## Vertical
Use `orientation="vertical"` for a vertical slider.
```python
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
```
