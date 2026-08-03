import reflex as rx
from reflex.components.component import Component, ComponentNamespace
from reflex_components_core.el import Div

from ..core.core import CoreComponent


class ClassNames:
    ROOT = "flex flex-col justify-center text-secondary-12"
    TRIGGER = (
        "flex items-center gap-2 cursor-pointer select-none list-none rounded-md "
        "marker:content-none [&::-webkit-details-marker]:hidden "
        "[details[open]>&]:bg-muted/50"
    )
    PANEL = "text-sm"


class CollapsibleRoot(CoreComponent):
    @classmethod
    def create(cls, *children, default_open: bool = False, **props) -> Component:
        props["data-slot"] = "collapsible"
        if default_open:
            props.setdefault("open", True)
        cls.set_class_name(ClassNames.ROOT, props)
        return rx.el.details(*children, **props)


class CollapsibleTrigger(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Component:
        props["data-slot"] = "collapsible-trigger"
        cls.set_class_name(ClassNames.TRIGGER, props)
        return rx.el.summary(*children, **props)


class CollapsiblePanel(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        props["data-slot"] = "collapsible-panel"
        cls.set_class_name(ClassNames.PANEL, props)
        return super().create(*children, **props)


class Collapsible(ComponentNamespace):
    root = staticmethod(CollapsibleRoot.create)
    trigger = staticmethod(CollapsibleTrigger.create)
    panel = staticmethod(CollapsiblePanel.create)
    class_names = ClassNames


collapsible = Collapsible()
