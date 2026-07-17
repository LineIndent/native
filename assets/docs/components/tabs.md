---
title: "Tabs"
description: "A set of layered sections of content—known as tab panels—that are displayed one at a time."
order: 0
---


## Tabs, A Set Of Layered Sections Of Content—Known As Tab Panels—That Are Displayed One At A Time.


```python
from components.ui.tabs import Tabs
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

        user_on_click = props.pop("on_click", None)
        user_on_mount = props.pop("on_mount", None)

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

        click_handlers = [rx.call_script(js_on_click)]
        if user_on_click is not None:
            if isinstance(user_on_click, list):
                click_handlers.extend(user_on_click)
            else:
                click_handlers.append(user_on_click)
        props["on_click"] = click_handlers

        mount_handlers = [rx.call_script(js_on_mount)]
        if user_on_mount is not None:
            if isinstance(user_on_mount, list):
                mount_handlers.extend(user_on_mount)
            else:
                mount_handlers.append(user_on_mount)
        props["on_mount"] = mount_handlers

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
```

# Examples

# Basic

```python
def tabs_basic() -> rx.Component:
    return tabs.root(
        tabs.list(
            tabs.trigger("Overview", value="overview"),
            tabs.trigger("Analytics", value="analytics"),
            tabs.trigger("Reports", value="reports"),
            tabs.trigger("Settings", value="settings"),
            variant="line",
        ),
        tabs.content(
            card.root(
                card.header(
                    card.title("Overview"),
                    card.description(
                        "View your key metrics and recent project activity. Track progress "
                        "across all your active projects."
                    ),
                ),
                card.content(
                    "You have 12 active projects and 3 pending tasks.",
                    class_name="text-sm text-muted-foreground",
                ),
            ),
            value="overview",
        ),
        tabs.content(
            card.root(
                card.header(
                    card.title("Analytics"),
                    card.description(
                        "Track performance and user engagement metrics. Monitor trends and "
                        "identify growth opportunities."
                    ),
                ),
                card.content(
                    "Page views are up 25% compared to last month.",
                    class_name="text-sm text-muted-foreground",
                ),
            ),
            value="analytics",
        ),
        tabs.content(
            card.root(
                card.header(
                    card.title("Reports"),
                    card.description(
                        "Generate and download your detailed reports. Export data in "
                        "multiple formats for analysis."
                    ),
                ),
                card.content(
                    "You have 5 reports ready and available to export.",
                    class_name="text-sm text-muted-foreground",
                ),
            ),
            value="reports",
        ),
        tabs.content(
            card.root(
                card.header(
                    card.title("Settings"),
                    card.description(
                        "Manage your account preferences and options. Customize your "
                        "experience to fit your needs."
                    ),
                ),
                card.content(
                    "Configure notifications, security, and themes.",
                    class_name="text-sm text-muted-foreground",
                ),
            ),
            value="settings",
        ),
        default_value="overview",
        class_name="w-[400px]",
    )
```

# Line

Use the `variant="line"` prop on `tabs.list` for a line style.

```python
def tabs_line() -> rx.Component:
    return tabs.root(
        tabs.list(
            tabs.trigger("Overview", value="overview"),
            tabs.trigger("Analytics", value="analytics"),
            tabs.trigger("Reports", value="reports"),
            variant="line",
        ),
        default_value="overview",
    )
```

# Vertical

Use `orientation="vertical"` for vertical tabs.

```python
def tabs_vertical():
    return rx.el.div(
        tabs.root(
            tabs.list(
                tabs.trigger("Account", value="account"),
                tabs.trigger("Password", value="password"),
                tabs.trigger("Notifications", value="notifications"),
            ),
            default_value="account",
            orientation="vertical",
        ),
        class_name="flex justify-center text-sm",
    )
```

# Disabled

Use `disabled=True` to disable a tab.

```python
def tabs_disabled():
    return tabs.root(
        tabs.list(
            tabs.trigger("Home", value="home"),
            tabs.trigger(
                "Disabled",
                value="settings",
                disabled=True,
            ),
        ),
        default_value="home",
    )
```

# Icons

```python
def tabs_icons() -> rx.Component:
    return tabs.root(
        tabs.list(
            tabs.trigger(
                hi("BrowserIcon"),
                "Preview",
                value="preview",
            ),
            tabs.trigger(
                hi("CodeIcon"),
                "Code",
                value="code",
            ),
        ),
        default_value="preview",
    )
```

# API Reference

## tabs.root

The main container component that initializes your tab instance, holds the active state configuration on the client, and dictates the layout orientation.

```python
tabs.root(
    tabs.list(
        tabs.trigger("Overview", value="overview"),
        tabs.trigger("Analytics", value="analytics"),
    ),
    tabs.content(
        "Overview panel data",
        value="overview"
    ),
    default_value="overview",
)
```

| Prop            | Type                                | Default        |
| --------------- | ----------------------------------- | -------------- |
| `default_value` | `str`                               | `""`           |
| `orientation`   | `Literal["horizontal", "vertical"]` | `"horizontal"` |
| `class_name`    | `str`                               | `""`           |

## tabs.list

Groups the trigger navigation buttons together and controls the visual theme style.

```python
tabs.list(
    tabs.trigger("Tab 1", value="tab1"),
    tabs.trigger("Tab 2", value="tab2"),
    variant="line",
)
```

| Prop         | Type                         | Default     |
| ------------ | ---------------------------- | ----------- |
| `variant`    | `Literal["default", "line"]` | `"default"` |
| `class_name` | `str`                        | `""`        |

## tabs.trigger

The clickable button elements used to switch active states. They safely merge internal client-side JS actions with optional user-supplied events.

```python
tabs.trigger(
    "Analytics",
    value="analytics",
    on_click=rx.console_log("Switched tabs!")
)
```

| Prop         | Type                                      | Default               |
| ------------ | ----------------------------------------- | --------------------- |
| `value`      | `str`                                     | _Required_            |
| `class_name` | `str`                                     | `""`                  |
| `id`         | `str`                                     | _Auto-generated UUID_ |
| `disabled`   | `bool`                                    | `False`               |
| `on_click`   | `Union[EventHandler, list[EventHandler]]` | `None`                |
| `on_mount`   | `Union[EventHandler, list[EventHandler]]` | `None`                |

## tabs.content

The structural panel containing content mapped to a specific tab trigger value. Toggles layout visibility instantly purely using CSS attribute matching.

```python
tabs.content(
    "Your dashboard analytics modules go here.",
    value="analytics",
)
```

| Prop         | Type  | Default    |
| ------------ | ----- | ---------- |
| `value`      | `str` | _Required_ |
| `class_name` | `str` | `""`       |
