import json
import reflex as rx

from components.ui.select import select
from components.ui.button import button
from components.ui.dialog import dialog
from components.ui.input import input
from components.core.hugeicon import hi
from native.registry.colors import COLOR_THEMES
from native.registry.themes import BASE_THEMES
from native.registry.radii import RADII_OPTIONS
from native.registry.styles import STYLE_REGISTRY
from native.registry.fonts import FONT_REGISTRY
from native.templates.navbar import navbar
from native.templates._get_code import get_code


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
from native.lib.examples.card_14 import card_14


def _theme_select(
    id_: str,
    label: str,
    options: list[dict],
    default_id: str,
    *,
    describe: bool = False,
    icon: rx.Component | None = None,
    swatch: bool = False,
) -> rx.Component:
    """
    swatch=True: a single live color dot next to the label (id=f"{id_}-swatch"),
      kept in sync by theme-preview.js. Which CSS token it reflects is
      decided per-select in the JS layer, not here — base-theme-select
      shows --accent, color-theme-select shows the effective --primary,
      chart-color-select shows the effective --chart-1.
    icon: a static icon (e.g. hi("PaintBucketIcon")) shown instead of a
      swatch — for selects with no live color to preview (Style, Radius,
      Font). Pass real icon names from your own hugeicon set; I'm not
      guessing at exact names here.
    """

    def _option_label(opt: dict) -> str:
        if describe and opt.get("description"):
            return f"{opt['label']}"
        return opt["label"]

    if icon is not None:
        indicator = icon
    elif swatch:
        indicator = rx.el.div(
            id=f"{id_}-swatch",
            class_name="size-4 rounded-full shrink-0 border border-border/40",
        )
    else:
        indicator = rx.el.div()

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    label, html_for=id_, class_name="text-sm font-medium text-muted-foreground"
                ),
                indicator,
                class_name="flex flex-row items-center justify-between",
            ),
            select(
                *[select.option(_option_label(opt), value=opt["id"]) for opt in options],
                id=id_,
                default_value=default_id,
                wrapper_class_name="w-full [&_[data-slot=native-select-icon]]:hidden",
                class_name="w-full h-9",
            ),
            class_name="flex flex-col gap-2 px-1 pt-2",
        ),
        class_name="px-3 pb-3",
    )


def open_preset() -> rx.Component:
    return dialog.root(
        dialog.trigger(button("Open Preset", variant="outline", class_name="justify-start")),
        dialog.popup(
            dialog.header(
                dialog.title("Open Theme Preset"),
                dialog.description(
                    "Paste a preset ID to load a theme configuration."
                ),
            ),
            rx.el.div(
                input(id="preset-input", placeholder="e.g. IBZJp", class_name="flex-1"),
            ),
            dialog.footer(
                rx.el.div(
                    dialog.close(
                        button("Cancel", type="button", variant="outline", class_name="flex-1"),
                        class_name="flex-1",
                    ),
                    dialog.close(
                        button(
                            "Apply",
                            type="button",
                            class_name="flex-1",
                            id="apply-preset-button",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="w-full flex flex-row items-center justify-center gap-x-4",
                ),
            ),
            class_name="sm:max-w-sm",
        ),
    )


def _sidebar_desktop():
    return rx.el.aside(
        rx.el.div(
            button(
                "Get Code",
                id="copy-theme-button",
                type="button",
                class_name="w-full",
                on_click=rx.call_script(
                    'const el = document.getElementById("toggle-wrapper"); '
                    'el.dataset.show = el.dataset.show === "true" ? "false" : "true";'
                )
            ),
            class_name="p-3 bg-card/20",
        ),
        rx.el.div(
            _theme_select(
                "style-select", "Style", STYLE_REGISTRY, STYLE_REGISTRY[0]["id"],
                describe=True,
                icon=hi("HexagonIcon"),
            ),
            rx.el.div(
                _theme_select(
                    "base-theme-select", "Base theme", BASE_THEMES, BASE_THEMES[0]["id"],
                    swatch=True,
                ),
                _theme_select(
                    "color-theme-select", "Color theme",
                    [{"id": "__match_base__", "label": BASE_THEMES[0]["label"]}] + COLOR_THEMES,
                    "__match_base__",
                    swatch=True,
                ),
                _theme_select(
                    "chart-color-select", "Chart colors",
                    [{"id": "__match_base__", "label": BASE_THEMES[0]["label"]}] + COLOR_THEMES,
                    "__match_base__",
                    swatch=True,
                ),
            ),
            _theme_select(
                "radius-select", "Radius",
                [{"id": "__default__", "label": "Default"}] + RADII_OPTIONS,
                "__default__",
                icon=hi("SquareRoundCornerIcon")
            ),
            _theme_select(
                "font-select", "Font", FONT_REGISTRY, FONT_REGISTRY[0]["id"],
                icon=hi("TextFontIcon")
            ),
            class_name="flex-1 min-h-0 overflow-y-auto scrollbar-none divide-y divide-input",
        ),
        rx.el.div(
            button(
                "Shuffle",
                id="shuffle-button",
                type="button",
                variant="outline",
                class_name="w-full justify-start",
            ),
            button(
                rx.el.span("--preset ", html_for="preset-code-display"),
                rx.el.input(
                    id="preset-code-display",
                    default_value="b0",
                    read_only=True,
                    disabled=True,
                ),
                variant="outline",
                type="button",
                class_name="w-full flex flex-row items-center justify-start",
            ),
            open_preset(),
            class_name="p-4 flex flex-col gap-3 bg-card/20",
        ),
        rx.el.div(
            button(
                "Reset",
                id="reset-preset-button",
                type="button",
                class_name="w-full",
                variant="destructive",
            ),
            class_name="p-3 bg-card/20",
        ),
        class_name=(
            "hidden lg:flex w-full max-w-[12rem] shrink-0 !overflow-hidden flex-col "
            "border border-input/90 divide-y divide-input h-full text-sm "
            "text-card-foreground dark bg-card/90 isolate rounded-2xl"
        ),
    )


def sidebar():
    return rx.el.div(
        _sidebar_desktop(),
        class_name=(
            "w-full flex-initial h-auto min-h-0 min-w-0 max-w-full lg:flex-1 "
            "lg:h-full lg:w-[12rem] lg:max-w-[12rem] lg:shrink-0"
        ),
    )


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
                        card_14(),
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



def source_space():
    return rx.el.div(
        rx.el.div(
            get_code(),
            class_name="flex-[15] min-h-0 w-full border border-input/90 rounded-2xl"
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(
                    "Read the ",
                    rx.el.a(
                        "theming",
                        href="/docs/resources/theming",
                        class_name="font-semibold underline",
                    ),
                    " documentation.",
                ),
                class_name="w-full text-[13px] font-light",
            ),
            class_name="flex-[1] flex w-full px-4 flex-row items-end justify-center"
        ),

        id="source-space",
        class_name=(
            "hidden "
            "group-data-[show=true]:flex flex-col gap-y-4 "
            "w-full flex-initial h-auto min-h-0 min-w-0 max-w-full lg:flex-1 "
            "lg:h-full lg:w-sm lg:max-w-sm lg:shrink-0"
        ),
    )


def create_page():
    return rx.el.div(
        rx.el.div(
            navbar(class_name="max-w-full !pl-4 !pr-6"),
            rx.el.main(
                sidebar(),
                preview_space(),
                source_space(),
                id="toggle-wrapper",
                data_show="false",
                class_name="group flex flex-col gap-x-6 lg:flex-row w-full h-full min-h-0 overflow-hidden p-4 lg:px-6 lg:pb-6 lg:pt-2 gap-y-6 scrollbar-none",
            ),
            class_name="relative flex h-screen flex-col bg-background overflow-hidden",
        ),
        class_name="relative flex h-screen flex-col bg-background overflow-hidden",
        on_mount=[rx.call_script(
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
        rx.call_script(
            """
            requestAnimationFrame(() => {
                Prism.highlightAll();
            });
            """
        ),
        ],
    )
