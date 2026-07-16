from dataclasses import dataclass

from reflex.event import call_script
from reflex_components_core.el import Div, Header, a, div, header

import native.registry.routes as routes
from components.core.hugeicon import hi
from components.ui.button import button, button_variants
from components.ui.menu import menu
from native.templates.github import github
from native.templates.theme import theme_toggle_button

NAV_LIST = [
    {"title": "Home", "url": ""},
    {"title": "Docs", "url": "docs"},
    {"title": "Components", "url": "components"},
    {"title": "Create", "url": "create"},
    {"title": "Typeset", "url": "typeset"},
]


@dataclass
class SidebarSection:
    title: str
    routes: list[dict]


MENU_SECTIONS = [
    SidebarSection(title="Pages", routes=NAV_LIST),
    SidebarSection(title="Getting Started", routes=routes.GET_STARTED_URLS),
    SidebarSection(title="Utilities", routes=routes.UTILITIES),
    SidebarSection(title="Resources", routes=routes.RESOURCES_URLS),
    SidebarSection(title="Charts", routes=routes.CHARTS_URLS),
    SidebarSection(title="Components", routes=routes.BASE_UI_COMPONENTS),
]


def _separator() -> Div:
    return div(class_name="h-3 w-px bg-muted-foreground/40")


def _mobile_navigation():
    menu_elements = []

    for s_idx, section in enumerate(MENU_SECTIONS):
        if section.title:
            menu_elements.append(menu.group_label(section.title))

        for r_idx, route in enumerate(section.routes):
            target_url = f"/{route['url']}"

            menu_elements.append(
                menu.item(
                    route["title"],
                    id=f"mob-nav-{s_idx}-{r_idx}",
                    on_click=call_script(f"window.location.href = '{target_url}';"),
                )
            )

        if s_idx < len(MENU_SECTIONS) - 1:
            menu_elements.append(menu.separator())

    return menu.root(
        menu.trigger(
            hi("Menu09Icon", class_name="size-4 shrink-0 mr-2"),
            "Navigation",
            class_name=button_variants("outline"),
        ),
        menu.content(
            *menu_elements,
            side="bottom",
            align="start",
            class_name="max-h-[50vh] overflow-y-auto w-48",
        ),
    )


def navbar(class_name: str = "") -> Header:
    return header(
        div(
            div(
                *[
                    a(button(nav["title"], variant="ghost"), href=f"/{nav['url']}")
                    for nav in NAV_LIST
                ],
                class_name="hidden md:flex",
            ),
            div(_mobile_navigation(), class_name="flex md:hidden"),
            div(
                theme_toggle_button(),
                _separator(),
                github(),
                _separator(),
                a(button("New Project"), href="/create"),
                class_name="flex flex-row gap-x-2 items-center",
            ),
            class_name="w-full mx-auto flex flex-row items-center justify-between px-4 md:px-8 "
            + class_name,
        ),
        class_name="sticky top-0 z-50 w-full h-13 bg-background flex items-center",
    )
