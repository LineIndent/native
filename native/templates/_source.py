import reflex as rx

from native.templates._copy_btn import create_copy_button
from reflex_components_core.el import div, p, h1, h4, span


def _parse_file_path(file_path: str) -> tuple[str, str]:
    """Helper to split file paths into directories and file names consistently."""
    parts = file_path.rsplit("/", 1)
    dir_part = parts[0] + "/" if len(parts) > 1 else ""
    file_part = parts[1] if len(parts) > 1 else parts[0]
    return dir_part, file_part


def file_codeblock(file_path: str, source: str) -> rx.Component:

    dir_part, file_part = _parse_file_path(file_path)
    button, btn_id = create_copy_button(content=source)

    return div(
        div(
            div(
                h4(
                    dir_part + file_part,
                    class_name="truncate text-sm tracking-tight",
                ),
                class_name="flex min-w-0 items-center gap-1.5",
            ),
            button,
            class_name="flex items-center justify-between gap-2",
        ),
        on_click=rx.call_script(
            f"document.getElementById('{btn_id}').click();"
        ),
        class_name="group flex flex-col gap-3 border border-border bg-background p-4 transition-colors hover:bg-muted/30 focus-visible:border-ring focus-visible:ring-1 focus-visible:ring-ring/50 focus-visible:outline-none rounded-lg",
    )


def source(files):
    return div(
        div(
            h1(
                "Source Code & Dependencies",
                class_name="text-2xl leading-tight font-bold tracking-tighter",
            ),
            p(
                span("For manual installation, copy each of the source codes below in their respective locations."),
                class_name="text-sm text-muted-foreground",
            ),
            div(
                *[file_codeblock(file[0], file[1]) for file in files],
                class_name="w-full grid grid-cols-1 gap-8 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3",
            ),
            class_name="w-full flex flex-col items-start gap-4",
        ),
        class_name="w-full flex flex-col gap-6 mb-10",
    )
