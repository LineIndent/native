import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn


class ClassNames:
    ROOT = "w-full flex flex-col gap-3 disabled:opacity-50 disabled:cursor-not-allowed text-sm"

    ITEM_ROOT = (
        "group relative inline-flex size-4 shrink-0 cursor-pointer items-center "
        "justify-center rounded-full border border-input "
        "has-[:disabled]:cursor-not-allowed has-[:disabled]:opacity-50 "
        "has-[:focus-visible]:border-ring has-[:focus-visible]:ring-3 has-[:focus-visible]:ring-ring/50 "
        "has-[[aria-invalid=true]]:border-destructive has-[[aria-invalid=true]]:ring-3 "
        "has-[[aria-invalid=true]]:ring-destructive/20 "
        "dark:bg-input/30 "
        "has-[:checked]:border-primary "
        "peer-has-[[data-slot=field-content]]:mt-0.5 [&:has(~[data-slot=field-content])]:mt-0.5"
    )

    ITEM_INPUT = "peer sr-only"

    ITEM_INDICATOR = "hidden peer-checked:flex items-center justify-center"

    ITEM_INDICATOR_DOT = "size-2 rounded-full bg-primary"

    _KNOWN_INPUT_PROPS = (
        "checked",
        "default_checked",
        "disabled",
        "required",
        "id",
    )


class RadioGroupRoot(CoreComponent):
    @classmethod
    def create(cls, *children, disabled: bool = False, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "radio-group"
        props["role"] = "radiogroup"
        if disabled:
            props["disabled"] = True
        cls.set_class_name(cn(ClassNames.ROOT, custom_classes), props)
        return rx.el.fieldset(*children, **props)


class RadioGroupItem(CoreComponent):
    @classmethod
    def create(cls, *children, name: str, value: str, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")

        input_props = {"name": name, "value": value}
        for key in list(props.keys()):
            if (
                key in ClassNames._KNOWN_INPUT_PROPS
                or key.startswith("on_")
                or key.startswith("data-")
                or key.startswith("aria-")
            ):
                input_props[key] = props.pop(key)

        input_props["type"] = "radio"
        input_props["data-slot"] = "radio-group-item-input"
        input_props["class_name"] = ClassNames.ITEM_INPUT

        props["data-slot"] = "radio-group-item"

        if not children:
            children = (RadioGroupIndicator.create(),)

        cls.set_class_name(cn(ClassNames.ITEM_ROOT, custom_classes), props)
        return rx.el.label(rx.el.input(**input_props), *children, **props)


class RadioGroupIndicator(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        if len(children) == 0:
            children = (rx.el.span(class_name=ClassNames.ITEM_INDICATOR_DOT),)
        props["data-slot"] = "radio-group-item-indicator"
        cls.set_class_name(ClassNames.ITEM_INDICATOR, props)
        return rx.el.span(*children, **props)


class RadioGroup(ComponentNamespace):
    root = staticmethod(RadioGroupRoot.create)
    item = staticmethod(RadioGroupItem.create)
    indicator = staticmethod(RadioGroupIndicator.create)
    class_names = ClassNames


radio_group = RadioGroup()
