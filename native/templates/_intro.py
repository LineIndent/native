import reflex as rx
from reflex_components_core.el import div, h1, p, span, strong

from components.core.hugeicon import hi
from components.ui.button import button, button_variants
from native.templates._copy_btn import generate_component_id

COPY_ICON_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" color="currentColor" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 15C9 12.1716 9 10.7574 9.87868 9.87868C10.7574 9 12.1716 9 15 9L16 9C18.8284 9 20.2426 9 21.1213 9.87868C22 10.7574 22 12.1716 22 15V16C22 18.8284 22 20.2426 21.1213 21.1213C20.2426 22 18.8284 22 16 22H15C12.1716 22 10.7574 22 9.87868 21.1213C9 20.2426 9 18.8284 9 16L9 15Z"/><path d="M16.9999 9C16.9975 6.04291 16.9528 4.51121 16.092 3.46243C15.9258 3.25989 15.7401 3.07418 15.5376 2.90796C14.4312 2 12.7875 2 9.5 2C6.21252 2 4.56878 2 3.46243 2.90796C3.25989 3.07417 3.07418 3.25989 2.90796 3.46243C2 4.56878 2 6.21252 2 9.5C2 12.7875 2 14.4312 2.90796 15.5376C3.07417 15.7401 3.25989 15.9258 3.46243 16.092C4.51121 16.9528 6.04291 16.9975 9 16.9999"/></svg>'
TICK_ICON_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" color="currentColor" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 14.5C5 14.5 6.5 14.5 8.5 18C8.5 18 14.0588 8.83333 19 7"/></svg>'


def _usage_demo(slug: str):
    demo_id = generate_component_id()
    icon_id = f"icon-{demo_id}"

    commands = {
        "buridan": f"buridan add {slug}",
        "uv": f"uv run buridan add {slug}",
        "pip": f"python -m buridan add {slug}",
    }

    def view_button(view: str, label: str):
        return button(
            label,
            variant="outline",
            class_name=(
                "h-7 w-fit font-normal usage-btn border-transparent bg-transparent "
                f"group-data-[view={view}]:border-border "
                f"group-data-[view={view}]:bg-background"
            ),
            on_click=rx.call_script(
                f"""document.getElementById("demo-{demo_id}").dataset.view = "{view}";"""
            ),
        )

    def command_line(view: str, command_text: str):
        return div(
            rx.el.pre(
                rx.el.code(
                    command_text,
                    id=f"command-{demo_id}-{view}",
                    class_name="language-python text-sm",
                ),
            ),
            class_name=(
                f"size-full overflow-x-auto p-2 hidden group-data-[view={view}]:flex"
            ),
        )

    commands_js = ", ".join(f'"{view}": "{cmd}"' for view, cmd in commands.items())

    return div(
        div(
            div(
                view_button("uv", "uv"),
                view_button("pip", "pip"),
                view_button("buridan", "buridan"),
                class_name="flex items-center gap-1",
            ),
            rx.el.button(
                hi("Copy01Icon", id=icon_id, class_name="size-4"),
                class_name="flex items-center gap-1 px-2",
                on_click=rx.call_script(
                    f"""
                    const commands = {{{commands_js}}};
                    const view = document.getElementById("demo-{demo_id}").dataset.view;
                    const icon = document.getElementById("{icon_id}");

                    navigator.clipboard.writeText(commands[view]);

                    icon.innerHTML = `{TICK_ICON_SVG}`;

                    setTimeout(() => {{
                        icon.innerHTML = `{COPY_ICON_SVG}`;
                    }}, 1500);
                    """
                ),
            ),
            class_name="flex items-stretch justify-between p-0.5 pb-0.5",
        ),
        div(
            *[command_line(view, cmd) for view, cmd in commands.items()],
            class_name=(
                "rounded-md relative m-0.5 mt-0 flex min-h-0 flex-1 flex-col "
                "overflow-hidden border bg-background "
                "dark:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.05)]"
            ),
        ),
        id=f"demo-{demo_id}",
        data_view="uv",
        class_name="w-full group relative flex min-w-0 flex-col border bg-muted/50 min-h-10 rounded-lg",
    )


def intro(raw_arg):
    intro = raw_arg.strip("[]").strip()

    if "," not in intro:
        raise ValueError(f"Invalid INTRO format: {raw_arg!r}")

    title, description = intro.split(",", 1)
    slug = title.strip().lower().replace(" ", "_")

    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                title.strip(),
                class_name="text-2xl leading-tight font-bold tracking-tighter",
            ),
            rx.el.p(
                description.strip(),
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col items-start gap-4 max-w-xl",
        ),
        div(
            h1(
                "Installation",
                class_name="text-2xl leading-tight font-bold tracking-tighter",
            ),
            p(
                span("Command to install the "),
                strong(title.strip()),
                span(" component."),
                class_name="text-sm text-muted-foreground",
            ),
            _usage_demo(slug),
            class_name="w-full flex flex-col items-start gap-4",
        ),
        class_name="flex flex-col gap-6 mb-10",
    )
