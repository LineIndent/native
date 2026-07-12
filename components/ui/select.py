from typing import Literal

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn
from ..core.hugeicon import hi

LiteralNativeSelectSize = Literal["default", "sm"]


class ClassNames:
    WRAPPER = "group/native-select relative w-fit has-[select:disabled]:opacity-50"

    SELECT = (
        "h-8 w-full min-w-0 appearance-none rounded-lg border border-input "
        "bg-transparent py-1 pr-8 pl-2.5 text-sm outline-none "
        "select-none selection:bg-primary selection:text-primary-foreground "
        "placeholder:text-muted-foreground "
        "focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 "
        "disabled:pointer-events-none disabled:cursor-not-allowed "
        "aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 "
        "data-[size=sm]:h-7 data-[size=sm]:rounded-[min(var(--radius-md),10px)] "
        "data-[size=sm]:py-0.5 "
        "dark:bg-input/30 dark:hover:bg-input/50 "
        "dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40"
    )

    ICON = (
        "pointer-events-none absolute top-1/2 right-2.5 size-4 -translate-y-1/2 "
        "text-muted-foreground select-none"
    )

    OPTION = "bg-[Canvas] text-[CanvasText]"

    OPTGROUP = "bg-[Canvas] text-[CanvasText]"


class NativeSelectComponent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        size = props.pop("size", "default")
        wrapper_class_name = props.pop("wrapper_class_name", "")
        data_slot = props.pop("data_slot", "native-select")

        select_class_name = cn(ClassNames.SELECT, props.get("class_name", ""))
        props["class_name"] = select_class_name
        props["data-slot"] = data_slot
        props["data-size"] = size

        select_el = rx.el.select(*children, **props)

        return rx.el.div(
            select_el,
            hi(
                "ArrowDown01Icon",
                class_name=ClassNames.ICON,
                data_slot="native-select-icon",
                aria_hidden="true",
            ),
            data_slot="native-select-wrapper",
            data_size=size,
            class_name=cn(ClassNames.WRAPPER, wrapper_class_name),
        )


class NativeSelectOptionComponent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "native-select-option"
        cls.set_class_name(ClassNames.OPTION, props)
        return rx.el.option(*children, **props)


class NativeSelectOptGroupComponent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "native-select-optgroup"
        cls.set_class_name(ClassNames.OPTGROUP, props)
        return rx.el.optgroup(*children, **props)


class NativeSelect(ComponentNamespace):
    __call__ = staticmethod(NativeSelectComponent.create)
    option = staticmethod(NativeSelectOptionComponent.create)
    optgroup = staticmethod(NativeSelectOptGroupComponent.create)
    class_names = ClassNames


select = NativeSelect()
