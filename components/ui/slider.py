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

    # Sizing/axis differs by orientation, so this is picked at runtime rather
    # than expressed as a data-[orientation=] variant — same convention used
    # in button_group.py / field.py for orientation-dependent classes.
    INPUT_ORIENTATIONS = {
        "horizontal": "w-full h-1",
        "vertical": "h-64 w-1 [writing-mode:vertical-lr] [direction:rtl]",
    }

    # Everything except axis-sizing: thumb + track pseudo-element styling,
    # shared by both horizontal and vertical.
    INPUT_BASE = (
        "appearance-none rounded-lg bg-secondary cursor-pointer "
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

    # Used for BOTH thumbs in dual-range mode. pointer-events-none on the
    # input body (so the two stacked inputs don't block each other), with
    # pointer-events re-enabled ONLY on the thumb pseudo-elements — the
    # standard technique for overlapping native range inputs. Track/progress
    # are fully transparent since the shared RANGE_FILL div (see below)
    # renders the visible colored bar between the two thumbs instead.
    INPUT_RANGE_THUMB = (
        "absolute inset-0 w-full appearance-none bg-transparent pointer-events-none "
        "focus-visible:outline-none "
        "[&::-webkit-slider-runnable-track]:bg-transparent "
        "[&::-moz-range-track]:bg-transparent "
        "[&::-moz-range-progress]:bg-transparent "
        "[&::-webkit-slider-thumb]:pointer-events-auto "
        "[&::-webkit-slider-thumb]:appearance-none "
        "[&::-webkit-slider-thumb]:size-3 "
        "[&::-webkit-slider-thumb]:rounded-full "
        "[&::-webkit-slider-thumb]:bg-white "
        "[&::-webkit-slider-thumb]:outline [&::-webkit-slider-thumb]:outline-1 [&::-webkit-slider-thumb]:outline-black "
        "hover:[&::-webkit-slider-thumb]:size-4.5 "
        "[&::-moz-range-thumb]:pointer-events-auto "
        "[&::-moz-range-thumb]:size-3 "
        "[&::-moz-range-thumb]:rounded-full "
        "[&::-moz-range-thumb]:border-0 "
        "[&::-moz-range-thumb]:bg-white "
        "[&::-moz-range-thumb]:outline [&::-moz-range-thumb]:outline-1 [&::-moz-range-thumb]:outline-black"
    )

    RANGE_WRAPPER = "relative w-full h-1"
    RANGE_FILL = "absolute h-1 rounded-lg bg-primary top-1/2 -translate-y-1/2 pointer-events-none"

    VALUE = "text-sm text-primary font-medium"


def _normalize_values(props: dict):
    """
    Accepts default_value/value as a bare scalar, a 1-element list, or a
    2-element list. Returns (kind, values) where kind is "single" or
    "range". Mutates props in place: for "single" it collapses back to a
    scalar (matching the original scalar-based API); for "range" it pops
    default_value/value out entirely, since the caller (_create_range)
    handles wiring them directly to the two underlying inputs.
    """
    raw = props.get("default_value", props.get("value"))
    if not isinstance(raw, (list, tuple)):
        return "single", raw

    if len(raw) == 1:
        if "default_value" in props:
            props["default_value"] = raw[0]
        if "value" in props:
            props["value"] = raw[0]
        return "single", raw[0]

    if len(raw) == 2:
        props.pop("default_value", None)
        props.pop("value", None)
        return "range", tuple(raw)

    raise ValueError(
        "slider default_value/value must be a scalar, or a list of 1 "
        f"(single thumb) or 2 (range) elements — got {len(raw)}."
    )


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
        kind, _ = _normalize_values(props)
        if kind == "range":
            return cls._create_range(**props)
        return cls._create_single(**props)

    @classmethod
    def _create_single(cls, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        default_value = props.get("default_value", props.get("value"))
        min_val = props.get("min", 0)
        max_val = props.get("max", 100)
        orientation = props.pop("orientation", "horizontal")

        props.setdefault("type", "range")
        props.setdefault("min", min_val)
        props.setdefault("max", max_val)
        props["data-slot"] = "slider-input"
        props["data-orientation"] = orientation

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

        size_classes = ClassNames.INPUT_ORIENTATIONS.get(
            orientation, ClassNames.INPUT_ORIENTATIONS["horizontal"]
        )
        cls.set_class_name(
            cn(size_classes, ClassNames.INPUT_BASE, custom_classes), props
        )
        return rx.el.input(**props)

    @classmethod
    def _create_range(cls, **props) -> rx.Component:
        """
        Two native <input type="range"> stacked on top of each other, with
        pointer-events restricted to just their thumbs (see
        ClassNames.INPUT_RANGE_THUMB) so both remain independently
        draggable. A separate fill div renders the colored bar between the
        two values and is kept in sync via a script on the native 'input'
        event.

        Known limitations: vertical orientation isn't wired up for range
        mode yet (only single-thumb), and if both thumbs land on the exact
        same value, the one later in the DOM (the max thumb) sits on top —
        a common, generally-acceptable default in dual-range sliders.
        """
        custom_classes = props.pop("class_name", "")
        lo_val, hi_val = props.pop(
            "default_value", props.pop("value", (0, 100))
        )
        min_val = props.get("min", 0)
        max_val = props.get("max", 100)
        step = props.get("step", 1)
        disabled = props.get("disabled")

        group_id = props.get("id") or f"slider-range-{uuid.uuid4().hex[:8]}"
        min_id, max_id, fill_id = f"{group_id}-min", f"{group_id}-max", f"{group_id}-fill"

        shared = {"type": "range", "min": min_val, "max": max_val, "step": step}
        if disabled is not None:
            shared["disabled"] = disabled

        min_input = rx.el.input(
            id=min_id,
            data_slot="slider-input-min",
            default_value=lo_val,
            class_name=ClassNames.INPUT_RANGE_THUMB,
            **shared,
        )
        max_input = rx.el.input(
            id=max_id,
            data_slot="slider-input-max",
            default_value=hi_val,
            class_name=ClassNames.INPUT_RANGE_THUMB,
            **shared,
        )
        fill = rx.el.div(
            id=fill_id, data_slot="slider-range-fill", class_name=ClassNames.RANGE_FILL
        )

        props["data-slot"] = "slider-input-group"
        props["id"] = group_id
        cls.set_class_name(cn(ClassNames.RANGE_WRAPPER, custom_classes), props)

        props["on_mount"] = rx.call_script(
            f"""
            (function() {{
                var minEl = document.getElementById('{min_id}');
                var maxEl = document.getElementById('{max_id}');
                var fillEl = document.getElementById('{fill_id}');
                if (!minEl || !maxEl || !fillEl || minEl.__rangeSliderAttached) return;
                minEl.__rangeSliderAttached = true;

                var lo = parseFloat(minEl.min), hi = parseFloat(minEl.max);
                function update() {{
                    var a = parseFloat(minEl.value), b = parseFloat(maxEl.value);
                    var pctA = ((a - lo) / (hi - lo)) * 100;
                    var pctB = ((b - lo) / (hi - lo)) * 100;
                    fillEl.style.left = pctA + '%';
                    fillEl.style.right = (100 - pctB) + '%';
                }}
                // keep the two thumbs from crossing each other
                minEl.addEventListener('input', function () {{
                    if (parseFloat(minEl.value) > parseFloat(maxEl.value)) {{
                        minEl.value = maxEl.value;
                    }}
                    update();
                }});
                maxEl.addEventListener('input', function () {{
                    if (parseFloat(maxEl.value) < parseFloat(minEl.value)) {{
                        maxEl.value = minEl.value;
                    }}
                    update();
                }});
                update();
            }})()
            """
        )

        return rx.el.div(min_input, max_input, fill, **props)


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
