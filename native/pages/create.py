import json

import reflex as rx

from components.ui.select import select
from native.registry.colors import COLOR_THEMES
from native.registry.themes import BASE_THEMES
from native.registry.radii import RADII_OPTIONS
from native.registry.styles import STYLE_REGISTRY
from native.registry.fonts import FONT_REGISTRY
from native.templates.navbar import navbar

from native.lib.examples.card_01 import card_01
from native.lib.examples.card_02 import card_02
from native.lib.examples.card_03 import card_03
from native.lib.examples.card_04 import card_04
from native.lib.examples.card_05 import card_05
from native.lib.examples.card_06 import card_06
from native.lib.examples.card_07 import card_07
from native.lib.examples.card_08 import card_08
from native.lib.examples.card_09 import card_09
from native.lib.examples.card_10 import card_10
from native.lib.examples.card_11 import card_11
from native.lib.examples.card_12 import card_12
from native.lib.examples.card_13 import card_13


def _theme_select(
    id_: str, label: str, options: list[dict], default_id: str, *, describe: bool = False
) -> rx.Component:
    def _option_label(opt: dict) -> str:
        if describe and opt.get("description"):
            return f"{opt['label']}"
            # return f"{opt['label']} — {opt['description']}"
        return opt["label"]


    return rx.el.div(rx.el.div(
        rx.el.div(rx.el.span(
            label, html_for=id_, class_name="text-sm font-medium text-muted-foreground"
        ),

        # rx.el.div(
        #     class_name="size-4 bg-primary shrink-0"
        # ),
            class_name="flex flex-row items-center justify-between"
        ),
        select(
            *[select.option(_option_label(opt), value=opt["id"]) for opt in options],
            id=id_,
            default_value=default_id,
            # wrapper_class_name="w-full [&_[data-slot=native-select-icon]]:hidden",
            wrapper_class_name="w-full",
            class_name="w-full"
        ),
        class_name="flex flex-col gap-2 px-1 pt-2",
    ),
    class_name="px-3 pb-3"
    )


def _create_page() -> rx.Component:
    return rx.el.div(
        rx.el.aside(
            rx.el.h2(
                "Theme Builder",
                class_name="text-lg font-semibold text-foreground mb-2",
            ),
            _theme_select(
                "style-select", "Style", STYLE_REGISTRY, STYLE_REGISTRY[0]["id"],
                describe=True,
            ),
            _theme_select(
                "radius-select", "Radius", RADII_OPTIONS, RADII_OPTIONS[0]["id"]
            ),
            _theme_select(
                "base-theme-select", "Base theme", BASE_THEMES, BASE_THEMES[0]["id"]
            ),
            _theme_select(
                "color-theme-select", "Color theme", COLOR_THEMES, COLOR_THEMES[0]["id"]
            ),
            _theme_select(
                "font-select", "Font", FONT_REGISTRY, FONT_REGISTRY[0]["id"]
            ),
            rx.el.button(
                "Copy theme CSS",
                id="copy-theme-button",
                type="button",
                class_name="mt-2 px-3 py-2 rounded-lg bg-primary text-primary-foreground text-sm w-full",
            ),
            class_name="flex flex-col gap-4 w-64 shrink-0 border-r border-border p-6 overflow-y-auto",
        ),
        rx.el.main(
            rx.el.div(
                card_01(),
                card_02(),
                card_03(),
                card_04(),
                card_05(),
                card_06(),
                card_07(),
                card_08(),
                card_09(),
                card_10(),
                card_11(),
                card_12(),
                card_13(),
                class_name=" ".join(
                    [
                        "flex flex-row gap-10 flex-wrap overflow-scroll w-full"
                    ]
                ),
            ),
            class_name=(
                "preview-theme w-full overflow-hidden flex flex-col gap-(--card-gap) bg-accent dark:bg-background text-foreground "
                "border-(length:--border-width) border-border rounded-xl "
                "p-(--card-padding) flex-1 m-6 font-(family-name:--font-family)"
            ),
        ),
        on_mount=rx.call_script(
            f"""
window.__THEME_REGISTRIES__ = {{
    base: {json.dumps(BASE_THEMES)},
    color: {json.dumps(COLOR_THEMES)},
    radius: {json.dumps(RADII_OPTIONS)},
    style: {json.dumps(STYLE_REGISTRY)},
    font: {json.dumps(FONT_REGISTRY)},
}};
if (window.preview) window.preview.applyAll();
"""
        ),
        class_name="w-full h-screen flex",
    )


def _sidebar_desktop():
    return rx.el.aside(
        _theme_select(
            "style-select", "Style", STYLE_REGISTRY, STYLE_REGISTRY[0]["id"],
            describe=True,
        ),
        rx.el.div(
            _theme_select(
                "base-theme-select", "Base theme", BASE_THEMES, BASE_THEMES[0]["id"]
            ),
            _theme_select(
                "color-theme-select", "Color theme", COLOR_THEMES, COLOR_THEMES[0]["id"]
            ),
        ),
        _theme_select(
            "radius-select", "Radius", RADII_OPTIONS, RADII_OPTIONS[0]["id"]
        ),
        _theme_select(
            "font-select", "Font", FONT_REGISTRY, FONT_REGISTRY[0]["id"]
        ),
        class_name="pt-3 hidden lg:flex w-full max-w-[12rem] shrink-0 !overflow-hidden flex-col border border-input/90 divide-y divide-input h-full text-sm text-card-foreground dark bg-card/90 isolate rounded-2xl",

    )

def sidebar():
    return rx.el.div(
        _sidebar_desktop(),
        class_name="w-full flex-initial h-auto min-h-0 min-w-0 max-w-full lg:flex-1 lg:h-full lg:w-[12rem] lg:max-w-[12rem] lg:shrink-0",

    ),


def preview_space():
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        card_01(),
                        card_02(),
                        card_03(),
                        card_04(),
                        card_05(),
                        card_06(),
                        card_07(),
                        card_08(),
                        card_09(),
                        card_10(),
                        card_11(),
                        card_12(),
                        card_13(),
                        class_name=" ".join(
                            [
                                "preview-theme",
                                "mx-auto",
                                "columns-1",
                                "sm:columns-3",
                                "md:columns-3",
                                "lg:columns-4",
                                "gap-10",
                                "space-y-10",
                            ]
                        ),
                    ),
                    class_name="sm:min-w-[1600px] w-full",
                ),
                class_name="w-full h-full border-1 border-input/90 rounded-2xl p-4 md:p-10 bg-accent dark:bg-transparent overflow-auto scrollbar-none",
            ),
            class_name="w-full h-full",
        ),
        class_name="w-full flex-[2] min-h-0 order-first lg:order-none lg:flex-1 lg:min-w-0 lg:h-full",

    )

def create_page():
    return rx.el.div(
        rx.el.div(
            navbar(),
            rx.el.main(
                sidebar(),
                preview_space(),
                class_name="flex flex-col gap-x-6 lg:flex-row w-full h-full min-h-0 overflow-hidden p-4 lg:px-6 lg:pb-6 lg:pt-2 gap-y-6 scrollbar-none",
            ),
            class_name="relative flex h-screen flex-col bg-background overflow-hidden"
        ),
        class_name="relative flex h-screen flex-col bg-background overflow-hidden",
        on_mount=rx.call_script(
        f"""
            window.__THEME_REGISTRIES__ = {{
                base: {json.dumps(BASE_THEMES)},
                color: {json.dumps(COLOR_THEMES)},
                radius: {json.dumps(RADII_OPTIONS)},
                style: {json.dumps(STYLE_REGISTRY)},
                font: {json.dumps(FONT_REGISTRY)},
            }};
            if (window.preview) window.preview.applyAll();
        """
        ),
    ),
