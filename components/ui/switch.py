import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn


class ClassNames:
    # Root container layout
    ROOT = "inline-flex items-center gap-3 cursor-pointer select-none group/switch"

    INPUT = "sr-only"

    # TRACK locks down the background color state changes perfectly
    TRACK = (
        "relative rounded-full transition-colors duration-200 ease-in-out bg-muted "
        "outline-none "
        # Explicit sizes driven by data-size
        "group-data-[size=default]/switch:h-[18.4px] group-data-[size=default]/switch:w-[32px] "
        "group-data-[size=sm]/switch:h-[14px] group-data-[size=sm]/switch:w-[24px] "
        # Checks for the exact input child tag state for lighting up colors
        "group-has-[input:checked]/switch:bg-primary "
        # Focus rings
        # "group-focus-within/switch:ring-2 group-focus-within/switch:ring-ring group-focus-within/switch:ring-offset-2 "
        # Aria-invalid error layouts
        "group-aria-[invalid=true]/switch:border-destructive group-aria-[invalid=true]/switch:ring-3 group-aria-[invalid=true]/switch:ring-destructive/20 "
        # Disabled control states
        "group-has-[:disabled]/switch:opacity-50 group-has-[:disabled]/switch:pointer-events-none group-has-[:disabled]/switch:cursor-not-allowed"
    )

    # THUMB controls the circle's size and translation positions flawlessly
    THUMB = (
        "pointer-events-none block rounded-full bg-background shadow-sm ring-0 transition-transform duration-200 "
        # Size match scaling
        "group-data-[size=default]/switch:size-4 group-data-[size=sm]/switch:size-3 "
        # Starting offset positions
        "translate-x-0.5 "
        # Horizontal translation when checkbox input child is checked
        "group-has-[input:checked]/switch:group-data-[size=default]/switch:translate-x-[14px] "
        "group-has-[input:checked]/switch:group-data-[size=sm]/switch:translate-x-[10px] "
        # Dark mode variant match overrides
        "group-has-[input:checked]/switch:dark:bg-primary-foreground "
        "dark:bg-foreground"
    )

    LABEL = "text-sm font-medium leading-none text-foreground"


class NativeSwitch(CoreComponent):
    # Explicitly registering this on our component class hooks it right into Reflex's build cycle
    @classmethod
    def get_event_triggers(cls) -> dict[str, any]:
        return {
            **super().get_event_triggers(),
            "on_change": lambda checked: [checked],
        }

    @classmethod
    def create(cls, label_text: str = "", **props) -> rx.Component:
        props["data-slot"] = "switch"

        size = props.pop("size", "default")
        props["data-size"] = size

        invalid = props.pop("invalid", False)
        if invalid:
            props["aria-invalid"] = "true"

        # 1. Pop out our custom fine-tuning class overrides
        track_class_name = props.pop("track_class_name", "")
        thumb_class_name = props.pop("thumb_class_name", "")

        on_change = props.pop("on_change", None)
        default_checked = props.pop("default_checked", False)
        disabled = props.pop("disabled", False)
        name = props.pop("name", None)

        input_props = {}
        if default_checked:
            input_props["default_checked"] = True
        if disabled:
            input_props["disabled"] = True
        if name:
            input_props["name"] = name

        if on_change:
            input_props["on_change"] = on_change

        cls.set_class_name(ClassNames.ROOT, props)

        return rx.el.label(
            rx.el.input(type="checkbox", class_name=ClassNames.INPUT, **input_props),
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


native_switch = SwitchNamespace()
