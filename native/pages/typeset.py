import json

import reflex as rx

from components.ui.button import button
from components.ui.select import select
from native.registry.typeset_options import (
    DEFAULT_BODY_FONT_ID,
    DEFAULT_FLOW_ID,
    DEFAULT_HEADING_FONT_ID,
    DEFAULT_LEADING_ID,
    DEFAULT_MEASURE_ID,
    DEFAULT_MONO_FONT_ID,
    DEFAULT_SIZE_ID,
    FLOW_OPTIONS,
    HEADING_BODY_FONTS,
    LEADING_OPTIONS,
    MEASURE_OPTIONS,
    MONO_FONTS,
    SIZE_OPTIONS,
)
from native.templates._get_typeset_code import typeset_get_code
from native.templates.navbar import navbar


def _typeset_select(
    id_: str, label: str, options: list[dict], default_id: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    label,
                    html_for=id_,
                    class_name="text-sm font-medium text-muted-foreground",
                ),
                rx.el.div(),
                class_name="flex flex-row items-center justify-between",
            ),
            select(
                *[select.option(opt["label"], value=opt["id"]) for opt in options],
                id=id_,
                default_value=default_id,
                wrapper_class_name="w-full [&_[data-slot=native-select-icon]]:hidden",
                class_name="w-full h-9",
            ),
            class_name="flex flex-col gap-2 px-1 pt-2",
        ),
        class_name="min-w-[10rem] shrink-0 lg:min-w-0 lg:px-3 lg:pb-3",
    )


def _get_code_mobile(): ...


def _sidebar_desktop():
    return rx.el.aside(
        rx.el.div(
            _typeset_select(
                "measure-select", "Measure", MEASURE_OPTIONS, DEFAULT_MEASURE_ID
            ),
            _typeset_select(
                "heading-select", "Heading", HEADING_BODY_FONTS, DEFAULT_HEADING_FONT_ID
            ),
            _typeset_select(
                "body-select", "Body", HEADING_BODY_FONTS, DEFAULT_BODY_FONT_ID
            ),
            _typeset_select("mono-select", "Mono", MONO_FONTS, DEFAULT_MONO_FONT_ID),
            _typeset_select("size-select", "Size", SIZE_OPTIONS, DEFAULT_SIZE_ID),
            _typeset_select(
                "leading-select", "Leading", LEADING_OPTIONS, DEFAULT_LEADING_ID
            ),
            _typeset_select("flow-select", "Flow", FLOW_OPTIONS, DEFAULT_FLOW_ID),
            class_name=(
                "px-2 py-1 lg:p-0 flex gap-1 overflow-x-auto scrollbar-none "
                "lg:flex-1 lg:flex-col lg:gap-0 lg:overflow-y-auto lg:overflow-x-hidden "
                "lg:divide-y lg:divide-input"
            ),
        ),
        rx.el.div(
            button(
                "Shuffle",
                id="typeset-shuffle-button",
                type="button",
                variant="outline",
                class_name="flex-1",
            ),
            # button(
            #     "Get Code",
            #     on_click=rx.call_script(
            #         """
            #         const el = document.getElementById("typeset-toggle-wrapper");
            #         el.dataset.show = el.dataset.show === "true" ? "false" : "true";
            #         """
            #     ),
            #     class_name="flex-1 lg:hidden",
            # ),
            button(
                rx.el.span(
                    "Get Code",
                    class_name="group-data-[show=true]:hidden",
                ),
                rx.el.span(
                    "Preview",
                    class_name="hidden group-data-[show=true]:inline",
                ),
                on_click=rx.call_script(
                    """
                    const el = document.getElementById("typeset-toggle-wrapper");
                    el.dataset.show = el.dataset.show === "true" ? "false" : "true";
                    """
                ),
                id="typeset-code-button",
                type="button",
                class_name="flex-1 lg:hidden",
            ),
            class_name="p-3 lg:p-4 bg-card/20 flex gap-3",
        ),
        class_name=(
            "flex flex-col gap-3 "
            "border border-input/90 dark text-card-foreground rounded-2xl bg-card/90 "
            "lg:w-[12rem] lg:max-w-[12rem] lg:h-full lg:gap-0 lg:divide-y lg:divide-input"
        ),
    )


# def sidebar():
#     return rx.el.div(
#         _sidebar_desktop(),
#         class_name=(
#             "w-full flex-initial h-auto min-h-0 min-w-0 max-w-full lg:flex-1 "
#             "lg:h-full lg:w-[12rem] lg:max-w-[12rem] lg:shrink-0"
#         ),
#     )


def sidebar():
    return rx.el.div(
        _sidebar_desktop(),
        class_name=(
            "w-full flex-initial h-auto min-h-0 min-w-0 max-w-full lg:flex-1 "
            "lg:h-full lg:w-[12rem] lg:max-w-[12rem] lg:shrink-0 "
            "order-last lg:order-none"
        ),
    )


def _read_and_render_md(filename: str) -> str:
    """Helper to read and compile local Markdown files into HTML."""
    import markdown

    _MD_EXTENSIONS = ["fenced_code", "tables", "toc"]
    try:
        with open(f"native/lib/typeset/{filename}") as file:
            content = file.read()
        return markdown.markdown(content, extensions=_MD_EXTENSIONS)
    except FileNotFoundError:
        return f"<p>Error: {filename} not found.</p>"


def _sample_content() -> rx.Component:
    html_one = _read_and_render_md("set_one.md")
    html_two = _read_and_render_md("set_two.md")
    html_three = _read_and_render_md("set_three.md")
    html_four = _read_and_render_md("set_four.md")

    sources = [html_one, html_two, html_three, html_four]

    return rx.el.div(
        rx.el.div(
            *[
                rx.el.div(
                    rx.html(html_content),
                    class_name=f"hidden group-data-[active='{i}']:block w-full",
                )
                for i, html_content in enumerate(sources, start=1)
            ],
            id="typeset-preview",
            class_name="typeset typeset-docs typeset-preview w-full max-w-xl mx-auto px-6 pt-8 pb-24",
        ),
        rx.el.div(
            rx.el.div(
                *[
                    button(
                        str(i),
                        id=f"nav-btn-{i}",
                        type="button",
                        variant="ghost",
                        on_click=rx.call_script(
                            f'document.getElementById("typeset-preview-wrapper").dataset.active = "{i}";'
                        ),
                        class_name=(
                            "inline-flex shrink-0 items-center justify-center whitespace-nowrap outline-none "
                            "focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 "
                            "disabled:pointer-events-none disabled:opacity-50 aria-invalid:border-destructive "
                            "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 "
                            "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 "
                            "hover:bg-accent dark:hover:bg-accent/50 gap-1.5 has-[>svg]:px-2.5 h-7 min-w-7 "
                            "cursor-pointer rounded-lg px-2 text-xs font-medium text-muted-foreground "
                            "transition-colors hover:text-foreground "
                            f"group-data-[active={i}]:bg-accent group-data-[active={i}]:text-accent-foreground"
                        ),
                    )
                    for i in [1, 2, 3, 4]
                ],
                class_name="dark flex items-center gap-1 rounded-xl bg-card/90 p-1 shadow-xl backdrop-blur-xl",
            ),
            class_name="sticky bottom-3 z-20 flex items-center justify-center gap-1.5",
        ),
        id="typeset-preview-wrapper",
        data_active="1",
        class_name="group relative w-full flex flex-col min-h-0",
    )


# def preview_space():
#     return rx.el.div(
#         rx.el.div(
#             _sample_content(),
#             class_name="w-full h-full flex justify-center border-1 border-input/90 rounded-2xl bg-background overflow-auto scrollbar-none",
#         ),
#         class_name="w-full flex-[2] min-h-0 order-first lg:order-none lg:flex-1 lg:min-w-0 lg:h-full",
#     )


def preview_space():
    return rx.el.div(
        rx.el.div(
            _sample_content(),
            class_name="w-full h-full flex justify-center border-1 border-input/90 rounded-2xl bg-background overflow-auto scrollbar-none",
        ),
        class_name="w-full flex-[2] min-h-0 order-first lg:order-none lg:flex-1 lg:min-w-0 lg:h-full max-lg:group-data-[show=true]:hidden",
    )


# def source_space():
#     return rx.el.div(
#         rx.el.div(
#             typeset_get_code(),
#             class_name="flex-[15] min-h-0 w-full border border-input/90 rounded-2xl",
#         ),
#         # rx.el.div(
#         #     rx.el.p(
#         #         rx.el.span(
#         #             "Read the ",
#         #             rx.el.a(
#         #                 "typeset",
#         #                 href="/docs/resources/typeset",
#         #                 class_name="font-semibold underline",
#         #             ),
#         #             " documentation.",
#         #         ),
#         #         class_name="w-full text-[13px] font-light",
#         #     ),
#         #     class_name="flex-[1] flex w-full px-4 flex-row items-end justify-center",
#         # ),
#         id="source-space",
#         class_name=(
#             "hidden xl:flex lg:flex-col lg:gap-y-4 "
#             "lg:w-full lg:flex-initial lg:h-auto lg:min-h-0 lg:min-w-0 lg:max-w-full lg:flex-1 "
#             "lg:h-full lg:w-sm lg:max-w-sm lg:shrink-0"
#         ),
#     )


def source_space():
    return rx.el.div(
        rx.el.div(
            typeset_get_code(),
            class_name="flex-[15] min-h-0 w-full border border-input/90 rounded-2xl",
        ),
        id="source-space",
        class_name=(
            "hidden max-lg:group-data-[show=true]:flex max-lg:group-data-[show=true]:flex-1 "
            "max-lg:group-data-[show=true]:min-h-0 xl:flex lg:flex-col lg:gap-y-4 "
            "lg:w-full lg:flex-initial lg:h-auto lg:min-h-0 lg:min-w-0 lg:max-w-full lg:flex-1 "
            "lg:h-full lg:w-sm lg:max-w-sm lg:shrink-0"
        ),
    )


def typeset_page():
    return rx.el.div(
        rx.el.div(
            navbar(class_name="max-w-full !pl-4 !pr-6"),
            rx.el.main(
                sidebar(),
                preview_space(),
                source_space(),
                id="typeset-toggle-wrapper",
                data_show="false",
                class_name="group flex flex-col gap-x-6 lg:flex-row w-full h-full min-h-0 overflow-hidden p-4 lg:px-6 lg:pb-6 lg:pt-2 gap-y-6 scrollbar-none",
            ),
            class_name="relative flex h-screen flex-col bg-background overflow-hidden",
        ),
        class_name="relative w-full max-w-[96rem] flex h-screen flex-col bg-background overflow-hidden justify-center",
        on_mount=[
            rx.call_script(
                f"""
                window.__TYPESET_REGISTRIES__ = {{
                    headingBodyFonts: {json.dumps(HEADING_BODY_FONTS)},
                    monoFonts: {json.dumps(MONO_FONTS)},
                    measure: {json.dumps(MEASURE_OPTIONS)},
                    size: {json.dumps(SIZE_OPTIONS)},
                    leading: {json.dumps(LEADING_OPTIONS)},
                    flow: {json.dumps(FLOW_OPTIONS)},
                }};
                if (window.typesetPreview) {{
                    window.typesetPreview.applyAll();
                    window.typesetPreview.renderCodeBlocks();
                }}
                """
            ),
            rx.call_script(
                """
                requestAnimationFrame(() => {
                    if (window.Prism) Prism.highlightAll();
                });
                """
            ),
        ],
    )
