from reflex_components_core.el import Div, Header, a, div, header

from components.ui.button import button
from native.templates.github import github
from native.templates.theme import theme_toggle_button

NAV_LIST = [
    {"name": "Home", "path": "/"},
    {"name": "Docs", "path": "/docs"},
    {"name": "Components", "path": "/components"},
    # {"name": "Blocks", "path": "/blocks"},
    # {"name": "Charts", "path": "/charts"},
    # {"name": "Create", "path": "/create"},
]


def _separator() -> Div:
    return div(class_name="h-3 w-px bg-muted-foreground/40")


def navbar() -> Header:
    return header(
        div(
            div(
                *[
                    a(button(nav["name"], variant="ghost"), href=nav["path"])
                    for nav in NAV_LIST
                ],
            ),
            div(
                theme_toggle_button(),
                _separator(),
                github(),
                _separator(),
                button("New Project"),
                class_name="flex flex-row gap-x-2 items-center",
            ),
            class_name="w-full !max-w-[63rem] mx-auto flex flex-row items-center justify-between px-2 md:px-0",
            # class_name="w-full max-w-[96rem] mx-auto flex flex-row items-center justify-between px-2 md:px-7",
        ),
        class_name="sticky top-0 z-50 w-full h-13 bg-background flex items-center",
    )
