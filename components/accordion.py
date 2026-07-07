import reflex as rx
from reflex.components.component import ComponentNamespace

from .core import CoreComponent, cn
from .hugeicon import hi


class ClassNames:
    ROOT = "flex w-full flex-col"

    ITEM = "not-last:border-b border-input block group/accordion-item"

    TRIGGER = (
        "flex flex-1 items-start justify-between "
        "rounded-lg border border-transparent py-2.5 text-left text-sm font-medium "
        "list-none cursor-pointer outline-none hover:underline"
    )

    TRIGGER_ICON = (
        "pointer-events-none shrink-0 ml-auto size-4 text-muted-foreground "
        "transition-transform duration-50 "
        "group-open/accordion-item:rotate-180"
    )

    PANEL = "overflow-hidden text-sm"

    PANEL_DIV = (
        "pt-0 pb-2.5 "
        "[&_a]:underline [&_a]:underline-offset-3 [&_a]:hover:text-foreground "
        "[&_p:not(:last-child)]:mb-4"
    )


class NativeAccordionRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        data_slot = props.pop("data_slot", "accordion")
        props["data-slot"] = data_slot
        cls.set_class_name(ClassNames.ROOT, props)
        return rx.el.div(*children, **props)


class NativeAccordionItem(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        data_slot = props.pop("data_slot", "accordion-item")
        props["data-slot"] = data_slot
        name = props.pop("name", None)
        if name:
            custom_attrs = props.setdefault("custom_attrs", {})
            custom_attrs["name"] = name

        cls.set_class_name(ClassNames.ITEM, props)
        return rx.el.details(*children, **props)


class NativeAccordionTrigger(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        data_slot = props.pop("data_slot", "accordion-trigger")
        props["data-slot"] = data_slot
        cls.set_class_name(ClassNames.TRIGGER, props)

        return rx.el.summary(
            *children,
            hi(
                "ArrowDown01Icon",
                class_name=ClassNames.TRIGGER_ICON,
                data_slot="accordion-trigger-icon",
            ),
            **props,
        )


class NativeAccordionPanel(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        data_slot = props.pop("data_slot", "accordion-panel")
        props["data-slot"] = data_slot
        inner_class = props.pop("class_name", "")
        cls.set_class_name(ClassNames.PANEL, props)

        return rx.el.div(
            rx.el.div(*children, class_name=cn(ClassNames.PANEL_DIV, inner_class)),
            **props,
        )


class NativeAccordion(ComponentNamespace):
    root = staticmethod(NativeAccordionRoot.create)
    item = staticmethod(NativeAccordionItem.create)
    trigger = staticmethod(NativeAccordionTrigger.create)
    panel = staticmethod(NativeAccordionPanel.create)
    class_names = ClassNames


accordion = NativeAccordion()
