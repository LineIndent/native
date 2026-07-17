import uuid

import reflex as rx
from reflex.components.component import ComponentNamespace
from reflex_components_core.el import Div

from ..core.core import CoreComponent, cn


class ClassNames:
    ROOT = (
        "group/tabs flex gap-2 "
        "data-[orientation=horizontal]:flex-col "
        "data-[orientation=vertical]:flex-row"
    )

    LIST = (
        "group/tabs-list inline-flex w-fit items-center justify-center rounded-lg p-[3px] text-muted-foreground "
        "group-data-[orientation=horizontal]/tabs:h-8 group-data-[orientation=vertical]/tabs:h-fit group-data-[orientation=vertical]/tabs:flex-col "
        "data-[variant=line]:rounded-none data-[variant=default]:bg-muted data-[variant=line]:gap-1 data-[variant=line]:bg-transparent"
    )

    TRIGGER = (
        "relative inline-flex h-[calc(100%-1px)] flex-1 items-center justify-center gap-1.5 rounded-md border border-transparent px-1.5 py-0.5 text-sm font-medium whitespace-nowrap text-foreground/60 transition-all "
        "group-data-[orientation=vertical]/tabs:w-full group-data-[orientation=vertical]/tabs:justify-start hover:text-foreground focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 focus-visible:outline-1 focus-visible:outline-ring disabled:pointer-events-none disabled:opacity-50 "
        "has-data-[icon=inline-end]:pr-1 has-data-[icon=inline-start]:pl-1 aria-disabled:pointer-events-none aria-disabled:opacity-50 dark:text-muted-foreground dark:hover:text-foreground "
        "group-data-[variant=default]/tabs-list:data-[active=true]:shadow-sm group-data-[variant=line]/tabs-list:data-[active=true]:shadow-none [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 "
        "group-data-[variant=line]/tabs-list:bg-transparent group-data-[variant=line]/tabs-list:data-[active=true]:bg-transparent dark:group-data-[variant=line]/tabs-list:data-[active=true]:border-transparent dark:group-data-[variant=line]/tabs-list:data-[active=true]:bg-transparent "
        "data-[active=true]:bg-background data-[active=true]:text-foreground dark:data-[active=true]:border-input dark:data-[active=true]:bg-input/30 dark:data-[active=true]:text-foreground "
        "after:absolute after:bg-foreground after:opacity-0 after:transition-opacity group-data-[orientation=horizontal]/tabs:after:inset-x-0 group-data-[orientation=horizontal]/tabs:after:bottom-[-5px] group-data-[orientation=horizontal]/tabs:after:h-0.5 group-data-[orientation=vertical]/tabs:after:inset-y-0 group-data-[orientation=vertical]/tabs:after:-right-1 group-data-[orientation=vertical]/tabs:after:w-0.5 group-data-[variant=line]/tabs-list:data-[active=true]:after:opacity-100 cursor-pointer"
    )

    CONTENT = "flex-1 text-sm outline-none hidden"


class TabsRoot(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        custom_classes = props.pop("class_name", "")
        orientation = props.pop("orientation", "horizontal")
        default_value = props.pop("default_value", "")

        props["data-slot"] = "tabs"
        props["data-orientation"] = orientation
        props["data-value"] = default_value

        return super().create(
            *children, class_name=cn(ClassNames.ROOT, custom_classes), **props
        )


class TabsList(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        custom_classes = props.pop("class_name", "")
        variant = props.pop("variant", "default")

        props["data-slot"] = "tabs-list"
        props["data-variant"] = variant

        return super().create(
            *children, class_name=cn(ClassNames.LIST, custom_classes), **props
        )


class TabsTrigger(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        value = props.pop("value", "")

        props["data-slot"] = "tabs-trigger"
        props["data-value"] = value
        props["type"] = "button"

        trigger_id = props.get("id") or f"tabs-trigger-{uuid.uuid4().hex[:8]}"
        props["id"] = trigger_id

        js_on_click = f"""
        (function() {{
            var trigger = document.getElementById('{trigger_id}');
            if (!trigger) return;
            var root = trigger.closest('[data-slot="tabs"]');
            if (!root) return;

            root.dataset.value = '{value}';
            root.querySelectorAll('[data-slot="tabs-trigger"]').forEach(function(t) {{
                t.setAttribute('data-active', t.getAttribute('data-value') === '{value}' ? 'true' : 'false');
            }});
        }})()
        """

        js_on_mount = f"""
        (function() {{
            var trigger = document.getElementById('{trigger_id}');
            if (!trigger) return;
            var root = trigger.closest('[data-slot="tabs"]');
            if (!root) return;

            var initialValue = root.dataset.value;
            trigger.setAttribute('data-active', trigger.getAttribute('data-value') === initialValue ? 'true' : 'false');
        }})()
        """

        props["on_click"] = rx.call_script(js_on_click)
        props["on_mount"] = rx.call_script(js_on_mount)

        cls.set_class_name(cn(ClassNames.TRIGGER, custom_classes), props)
        return rx.el.button(*children, **props)


class TabsContent(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        custom_classes = props.pop("class_name", "")
        value = props.pop("value", "")

        props["data-slot"] = "tabs-content"
        props["data-value"] = value

        active_toggle_class = f"group-data-[value='{value}']/tabs:block"

        return super().create(
            *children,
            class_name=cn(ClassNames.CONTENT, active_toggle_class, custom_classes),
            **props,
        )


class Tabs(ComponentNamespace):
    root = staticmethod(TabsRoot.create)
    list = staticmethod(TabsList.create)
    trigger = staticmethod(TabsTrigger.create)
    content = staticmethod(TabsContent.create)
    class_names = ClassNames


tabs = Tabs()
