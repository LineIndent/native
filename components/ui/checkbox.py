import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn
from ..core.hugeicon import hi


class ClassNames:
    ROOT = (
        "group relative inline-flex size-4 shrink-0 cursor-pointer items-center "
        "justify-center rounded-[4px] border border-input "
        "has-[:disabled]:cursor-not-allowed has-[:disabled]:opacity-50 "
        "has-[:focus-visible]:border-ring has-[:focus-visible]:ring-3 has-[:focus-visible]:ring-ring/50 "
        "has-[[aria-invalid=true]]:border-destructive has-[[aria-invalid=true]]:ring-3 "
        "has-[[aria-invalid=true]]:ring-destructive/20 "
        "dark:bg-input/30 "
        "has-[:checked]:border-primary has-[:checked]:bg-primary has-[:checked]:text-primary-foreground "
        "dark:has-[:checked]:bg-primary"
    )

    INPUT = "peer sr-only"

    INDICATOR = (
        "hidden peer-checked:grid place-content-center text-current [&>svg]:size-3.5"
    )

    BOX = (
        "pointer-events-none flex size-4 shrink-0 items-center justify-center "
        "rounded-[4px] border border-input "
        "peer-focus-visible:border-ring peer-focus-visible:ring-3 peer-focus-visible:ring-ring/50 "
        "peer-disabled:cursor-not-allowed peer-disabled:opacity-50 "
        "peer-aria-[invalid=true]:border-destructive peer-aria-[invalid=true]:ring-3 "
        "peer-aria-[invalid=true]:ring-destructive/20 "
        "dark:bg-input/30 "
        "peer-checked:border-primary peer-checked:bg-primary peer-checked:text-primary-foreground "
        "dark:peer-checked:bg-primary"
    )


class CheckboxRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")

        input_props = {}
        for key in (
            "checked",
            "default_checked",
            "disabled",
            "required",
            "name",
            "value",
            "on_change",
            "id",
        ):
            if key in props:
                input_props[key] = props.pop(key)

        input_props["type"] = "checkbox"
        input_props["data-slot"] = "checkbox-input"
        input_props["class_name"] = ClassNames.INPUT

        props["data-slot"] = "checkbox"

        if not children:
            children = (CheckboxIndicator.create(),)

        cls.set_class_name(cn(ClassNames.ROOT, custom_classes), props)
        return rx.el.label(rx.el.input(**input_props), *children, **props)


class CheckboxIndicator(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        if len(children) == 0:
            children = (hi("Tick02Icon"),)
        props["data-slot"] = "checkbox-indicator"
        cls.set_class_name(ClassNames.INDICATOR, props)
        return rx.el.span(*children, **props)


class Checkbox(ComponentNamespace):
    root = staticmethod(CheckboxRoot.create)
    indicator = staticmethod(CheckboxIndicator.create)
    class_names = ClassNames


checkbox = Checkbox()
