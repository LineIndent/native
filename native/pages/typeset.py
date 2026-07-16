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


def _typeset_select(
    id_: str, label: str, options: list[dict], default_id: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                label,
                html_for=id_,
                class_name="text-sm font-medium text-muted-foreground",
            ),
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
    )


def _sidebar() -> rx.Component:
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
            class_name="flex-1 min-h-0 overflow-y-auto scrollbar-none divide-y divide-input px-2",
        ),
        rx.el.div(
            button(
                "Shuffle",
                id="typeset-shuffle-button",
                type="button",
                variant="outline",
                class_name="w-full justify-start",
            ),
            button(
                "Get Code",
                id="typeset-copy-button",
                type="button",
                class_name="w-full",
            ),
            class_name="p-4 flex flex-col gap-3 bg-card/20",
        ),
        class_name=(
            "hidden lg:flex w-full max-w-[16rem] shrink-0 !overflow-hidden flex-col "
            "border border-input/90 divide-y divide-input h-full text-sm "
            "text-card-foreground dark bg-card/90 isolate rounded-2xl"
        ),
    )


def _sample_content() -> rx.Component:
    """Placeholder article content — swap for real docs content later. The
    exact tags matter here (h1/h2/p/ul/code), since typeset.css targets
    them specifically."""
    return rx.el.div(
        rx.el.h1("Building a Streaming Chatbot"),
        rx.el.p(
            "The ",
            rx.el.code("useChat"),
            " hook makes it effortless to create a conversational user "
            "interface for your chatbot application. It enables the "
            "streaming of chat messages from your AI provider, manages "
            "the chat state, and updates the UI automatically as new "
            "messages arrive.",
        ),
        rx.el.p(
            "To summarize, the ",
            rx.el.code("useChat"),
            " hook provides the following features:",
        ),
        rx.el.ul(
            rx.el.li(
                rx.el.strong("Message Streaming"),
                ": All the messages from the AI provider are streamed to the chat UI in real-time.",
            ),
            rx.el.li(
                rx.el.strong("Managed States"),
                ": The hook manages the states for input, messages, status, error and more for you.",
            ),
            rx.el.li(
                rx.el.strong("Seamless Integration"),
                ": Easily integrate your chat AI into any design or layout with minimal effort.",
            ),
        ),
        rx.el.h2("Example"),
        rx.el.p(
            "In this guide, you will learn how to use the ",
            rx.el.code("useChat"),
            " hook to create a chatbot application with real-time message streaming.",
        ),
        class_name="typeset typeset-preview mx-auto",
    )


def _preview_space() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            _sample_content(),
            class_name="w-full h-full border-1 border-input/90 rounded-2xl p-4 md:p-10 bg-background overflow-auto scrollbar-none",
        ),
        class_name="w-full flex-1 min-h-0 h-full",
    )


def typeset_page() -> rx.Component:
    return rx.el.div(
        rx.el.main(
            _sidebar(),
            _preview_space(),
            class_name="flex flex-col gap-x-6 lg:flex-row w-full h-full min-h-0 overflow-hidden p-4 lg:px-6 lg:pb-6 lg:pt-4 gap-y-6 scrollbar-none",
        ),
        class_name="relative flex h-screen flex-col bg-background overflow-hidden",
        on_mount=rx.call_script(
            f"""
            window.__TYPESET_REGISTRIES__ = {{
                headingBodyFonts: {json.dumps(HEADING_BODY_FONTS)},
                monoFonts: {json.dumps(MONO_FONTS)},
                measure: {json.dumps(MEASURE_OPTIONS)},
                size: {json.dumps(SIZE_OPTIONS)},
                leading: {json.dumps(LEADING_OPTIONS)},
                flow: {json.dumps(FLOW_OPTIONS)},
            }};
            if (window.typesetPreview) window.typesetPreview.applyAll();
            """
        ),
    )
