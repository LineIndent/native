import reflex as rx

from components.ui.accordion import accordion
from native.templates._copy_btn import create_copy_button, generate_component_id

CODE_BLOCK_STYLE = {
    # "color": "var(--foreground)",
    "white-space": "pre",
    # "fontSize": "14px",
    "padding": "1rem 0.75rem",
    "display": "block",
}


def _parse_file_path(file_path: str) -> tuple[str, str]:
    """Helper to split file paths into directories and file names consistently."""
    parts = file_path.rsplit("/", 1)
    dir_part = parts[0] + "/" if len(parts) > 1 else ""
    file_part = parts[1] if len(parts) > 1 else parts[0]
    return dir_part, file_part


def file_codeblock(file_path: str, source: str) -> rx.Component:
    toggle_height_id = generate_component_id()
    dir_part, file_part = _parse_file_path(file_path)

    return rx.el.div(
        rx.el.div(
            create_copy_button(content=source),
            class_name="absolute right-0 translate-y-4/5 bg-secondary dark:bg-card z-20",
        ),
        rx.el.div(
            rx.el.code(
                dir_part + file_part, style=CODE_BLOCK_STYLE, class_name="!text-[15px]"
            ),
            id=f"code-panel-{toggle_height_id}",
            class_name="scrollbar-none flex-1 min-h-0 flex flex-col h-full relative overflow-x-auto",
        ),
        class_name="outline outline-input flex-1 min-h-0 flex flex-col bg-secondary dark:bg-card relative",
    )


def file_codeblock_full(file_path: str, source: str) -> rx.Component:
    toggle_height_id = generate_component_id()
    dir_part, file_part = _parse_file_path(file_path)

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    dir_part,
                    rx.el.span(rx.el.strong(file_part)),
                    class_name="text-muted-foreground text-sm font-normal",
                ),
                class_name="flex px-[0.75rem] py-2",
            ),
            rx.el.div(
                rx.el.button(
                    "Expand",
                    class_name="!text-xs text-muted-foreground hover:text-foreground",
                    id=f"trigger-{toggle_height_id}",
                    on_click=rx.call_script(
                        f"""
                        const panel = document.getElementById('code-panel-{toggle_height_id}');
                        const btn = document.getElementById('trigger-{toggle_height_id}');

                        if (panel.style.maxHeight === 'none') {{
                            panel.style.maxHeight = '40vh';
                            panel.style.overflow = 'hidden';
                            panel.style.maskImage = 'linear-gradient(to bottom, black 65%, transparent 100%)';
                            panel.style.webkitMaskImage = 'linear-gradient(to bottom, black 65%, transparent 100%)';
                            btn.innerText = 'Expand';
                        }} else {{
                            panel.style.maxHeight = 'none';
                            panel.style.overflow = 'auto';
                            panel.style.maskImage = 'none';
                            panel.style.webkitMaskImage = 'none';
                            btn.innerText = 'Collapse';
                        }}
                        """
                    ),
                ),
                create_copy_button(content=source),
                class_name="flex flex-row gap-x-2 items-center",
            ),
            class_name="w-full border-b border-input flex flex-row items-center justify-between",
        ),
        rx.el.div(
            rx.el.code(source, style=CODE_BLOCK_STYLE, class_name="!text-[15px]"),
            id=f"code-panel-{toggle_height_id}",
            style={
                "max-height": "40vh",
                "overflow": "hidden",
                "transition": "max-height 0.3s ease-in-out",
                "mask-image": "linear-gradient(to bottom, black 65%, transparent 100%)",
                "-webkit-mask-image": "linear-gradient(to bottom, black 65%, transparent 100%)",
            },
            class_name="language-python scrollbar-none flex-1 min-h-0 flex flex-col h-full",
        ),
        class_name="rounded-lg outline outline-input flex-1 min-h-0 flex flex-col bg-secondary dark:bg-card",
    )


def installation(cli_command: str, files: list[tuple[str, str]]):
    """Native accordion wrapper for CLI and Manual installation instructions."""
    return accordion.root(
        accordion.item(
            accordion.trigger("Command"),
            accordion.panel(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            "uv",
                            create_copy_button(content=cli_command),
                            class_name="text-muted-foreground w-full border-b border-input/50 flex items-center justify-between pl-[0.75rem] py-2 bg-secondary dark:bg-card/70",
                        ),
                        rx.el.div(
                            rx.el.code(
                                rx.el.span(
                                    rx.el.strong("uv"),
                                    " run buridan ",
                                    rx.el.strong("add "),
                                    f"{cli_command}",
                                ),
                                style=CODE_BLOCK_STYLE,
                                class_name="language-python !text-sm",
                            ),
                            class_name="overflow-x-auto overflow-y-auto scrollbar-none flex-1 min-h-0",
                        ),
                        class_name="w-full flex-1 min-h-0 flex flex-col h-full",
                    ),
                    class_name="outline outline-input flex-1 min-h-0 flex flex-col bg-secondary dark:bg-card",
                ),
                class_name="p-2 mb-4",
            ),
            open=True,
            name="installation",
            class_name="flex-1 border-b-0",
        ),
        accordion.item(
            accordion.trigger("Manual"),
            accordion.panel(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "1. Copy and paste the following dependencies into your project.",
                            class_name="text-sm font-medium",
                        ),
                        rx.el.div(
                            *[file_codeblock(file[0], file[1]) for file in files[:-1]],
                            class_name="w-full flex flex-col gap-y-4",
                        ),
                        class_name="w-full flex flex-col gap-y-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "2. Copy and paste the following component code into your project.",
                            class_name="text-sm font-medium",
                        ),
                        file_codeblock_full(files[-1][0], files[-1][1]),
                        class_name="w-full flex flex-col gap-y-4",
                    ),
                    class_name="flex flex-col gap-y-6",
                )
                if len(files) > 1
                else file_codeblock_full(files[-1][0], files[-1][1]),
                class_name="p-2",
            ),
            name="installation",
            class_name="flex-1 border-b-0",
        ),
        class_name="my-8",
    )
