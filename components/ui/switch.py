import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn


class ClassNames:
    ROOT = "inline-flex items-center gap-3 cursor-pointer select-none group/switch"

    INPUT = "peer sr-only"

    TRACK = (
        "relative rounded-full bg-muted "
        "outline-none "
        "group-data-[size=default]/switch:h-[18.4px] group-data-[size=default]/switch:w-[32px] "
        "group-data-[size=sm]/switch:h-[14px] group-data-[size=sm]/switch:w-[24px] "
        "group-has-[input:checked]/switch:bg-primary "
        "peer-focus-visible:ring-3 peer-focus-visible:ring-ring/50 peer-focus-visible:outline-1 peer-focus-visible:outline-ring "
        "group-aria-[invalid=true]/switch:border-destructive group-aria-[invalid=true]/switch:ring-3 group-aria-[invalid=true]/switch:ring-destructive/20 "
        "group-has-[:disabled]/switch:opacity-50 group-has-[:disabled]/switch:pointer-events-none group-has-[:disabled]/switch:cursor-not-allowed"
    )

    THUMB = (
        "pointer-events-none block rounded-full bg-background shadow-sm ring-0 transition-transform duration-200 "
        "group-data-[size=default]/switch:size-4 group-data-[size=sm]/switch:size-3 "
        "translate-x-0.5 "
        "group-has-[input:checked]/switch:group-data-[size=default]/switch:translate-x-[14px] "
        "group-has-[input:checked]/switch:group-data-[size=sm]/switch:translate-x-[10px] "
        "group-has-[input:checked]/switch:dark:bg-primary-foreground "
        "dark:bg-foreground"
    )

    LABEL = "text-sm font-medium leading-none text-foreground"


class NativeSwitch(CoreComponent):
    @classmethod
    def create(cls, label_text: str = "", **props) -> rx.Component:
        props["data-slot"] = "switch"

        size = props.pop("size", "default")
        props["data-size"] = size

        invalid = props.pop("invalid", False)
        if invalid:
            props["aria-invalid"] = "true"

        track_class_name = props.pop("track_class_name", "")
        thumb_class_name = props.pop("thumb_class_name", "")

        input_props = {}
        for key in (
            "id",
            "checked",
            "default_checked",
            "disabled",
            "required",
            "name",
            "value",
            "on_change",
            "custom_attrs",
        ):
            if key in props:
                input_props[key] = props.pop(key)

        cls.set_class_name(ClassNames.ROOT, props)

        return rx.el.label(
            rx.el.input(
                type="checkbox", class_name=ClassNames.INPUT, **input_props
            ),
            rx.el.div(
                rx.el.span(
                    # Dynamically merge custom thumb classes
                    class_name=cn(ClassNames.THUMB, thumb_class_name)
                ),
                # Dynamically merge custom track classes
                class_name=cn(ClassNames.TRACK, track_class_name),
            ),
            rx.el.span(label_text, class_name=ClassNames.LABEL)
            if label_text
            else rx.fragment(),
            **props,
        )


class SwitchNamespace(ComponentNamespace):
    root = staticmethod(NativeSwitch.create)
    class_names = ClassNames


switch = SwitchNamespace()
