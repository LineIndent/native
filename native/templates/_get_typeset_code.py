import json
from pathlib import Path

import reflex as rx
from reflex.event import EventSpec

from components.ui.button import button

# Adjust this path if your project structure differs — reading the actual
# typeset.css asset at import time (rather than duplicating its content as
# a hardcoded string here) means the "Copy typeset.css" button always
# reflects the real file, with nothing to drift out of sync.
_TYPESET_CSS_PATH = Path(__file__).resolve().parents[2] / "assets" / "typeset.css"

try:
    TYPESET_CSS_CONTENT = _TYPESET_CSS_PATH.read_text()
except FileNotFoundError:
    TYPESET_CSS_CONTENT = (
        "/* typeset.css not found at the expected path — update "
        "_TYPESET_CSS_PATH in typeset_get_code.py to match your project. */"
    )

TYPESET_IMPORT_SNIPPET = '@import "tailwindcss";\n@import "./typeset.css";'


def get_code_section(
    title: str,
    description: str,
    component: rx.Component,
    has_copy: bool = False,
    copy_id: str | None = None,
    on_copy_click: EventSpec | None = None,
):
    """
    copy_id: unique id for the copy button. The original version of this
    helper hardcoded "copy-css-preset" for every has_copy=True call, which
    only worked because exactly one section used it — with three copy-able
    sections here, that would collide (three buttons sharing one id, only
    the first ever reachable via getElementById). Callers must pass a
    unique id per section now.
    on_copy_click: for STATIC content (e.g. the typeset.css file), wire the
    copy action directly here. For DYNAMIC content, leave this None — the
    external typeset-preview.js already listens for clicks on copy_id
    itself via its own document-level delegation, so the button doesn't
    need its own handler in that case.
    """

    if has_copy:
        copy_btn = button(
            "Copy",
            variant="outline",
            class_name="w-full mt-2",
            id=copy_id,
            type="button",
            **({"on_click": on_copy_click} if on_copy_click is not None else {}),
        )
    else:
        copy_btn = rx.el.div(class_name="hidden")

    return rx.el.div(
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-foreground text-sm font-medium",
            ),
            rx.el.p(
                description,
                class_name="text-muted-foreground text-sm font-light pb-2",
            ),
            rx.el.div(
                component,
                class_name="max-h-[45vh] overflow-y-scroll scrollbar-none p-4 bg-muted/60 rounded-xl",
            ),
            copy_btn,
            class_name="w-full flex flex-col gap-y-1",
        ),
        class_name="flex flex-col gap-y-2",
    )


def typeset_get_code():
    return rx.el.div(
        get_code_section(
            title="1. Create typeset.css",
            description="Copy the stylesheet into a typeset.css file next to your main CSS file, then import it:",
            component=rx.el.pre(
                rx.el.code(TYPESET_IMPORT_SNIPPET, class_name="language-css w-full"),
            ),
            has_copy=True,
            copy_id="copy-typeset-css",
            # Static content — copied directly on click rather than routed
            # through typeset-preview.js's dynamic-content delegation.
            on_copy_click=rx.call_script(
                "navigator.clipboard.writeText("
                + json.dumps(TYPESET_CSS_CONTENT)
                + ");"
            ),
        ),
        get_code_section(
            title="2. Add the fonts",
            description="Load the fonts with next/font in your root layout:",
            component=rx.el.pre(
                rx.el.code(id="get-typeset-fonts", class_name="language-jsx w-full"),
            ),
            has_copy=True,
            copy_id="copy-typeset-fonts",
            # Dynamic — typeset-preview.js populates this element's text AND
            # listens for clicks on copy-typeset-fonts itself. No on_click
            # needed here.
        ),
        get_code_section(
            title="3. Create your custom typeset",
            description="Copy the custom typeset class below into your global stylesheet, then wrap your content in it:",
            component=rx.el.pre(
                rx.el.code(id="get-typeset-tokens", class_name="language-css w-full"),
            ),
            has_copy=True,
            copy_id="copy-typeset-tokens",
        ),
        class_name="w-full h-full p-4 overflow-y-scroll overscroll-y-none flex flex-col gap-y-6 scrollbar-none",
    )
