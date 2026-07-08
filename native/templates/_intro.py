# import reflex as rx

# from components.core.hugeicon import hi
# from components.ui.button import button, button_variants
# from components.ui.button_group import button_group
# from components.ui.menu import menu


# def intro(raw_arg):
#     intro = raw_arg.strip("[]").strip()

#     if "," not in intro:
#         raise ValueError(f"Invalid INTRO format: {raw_arg!r}")

#     title, description = intro.split(",", 1)
#     slug = title.strip().lower().replace(" ", "-")

#     return rx.el.div(
#         rx.el.div(
#             rx.el.h1(
#                 title.strip(),
#                 class_name="text-2xl leading-tight font-bold tracking-tighter",
#             ),
#             rx.el.p(
#                 description.strip(),
#                 class_name="text-sm text-muted-foreground",
#             ),
#             rx.el.div(
#                 rx.el.code(
#                     rx.el.span(
#                         "❯",
#                         class_name="shrink-0 select-none text-muted-foreground/50",
#                     ),
#                     rx.el.span(
#                         "buridan add",
#                         class_name="text-muted-foreground",
#                         id=f"component-{slug}",
#                     ),
#                     rx.el.span(
#                         title.strip().lower(),
#                         class_name="font-medium text-foregroundfont-medium text-foreground",
#                     ),
#                     class_name="flex h-8 min-w-0 flex-1 items-center gap-2 overflow-x-auto border border-border bg-muted/40 px-3 font-mono text-xs whitespace-nowrap",
#                 ),
#                 button_group.root(
#                     button("Copy", variant="outline", on_click=rx.toast("click")),
#                     menu.root(
#                         menu.trigger(
#                             hi(
#                                 "ArrowDown01Icon",
#                             ),
#                             class_name=button_variants("outline"),
#                         ),
#                         menu.content(
#                             menu.group_label("Commands"),
#                             menu.separator(),
#                             menu.item(
#                                 "buridan",
#                                 on_click=rx.call_script(
#                                     f"""document.getElementById("component-{slug}").innerText = "buridan add";"""
#                                 ),
#                             ),
#                             menu.item(
#                                 "uv run",
#                                 on_click=rx.call_script(
#                                     f"""document.getElementById("component-{slug}").innerText = "uv run buridan add";"""
#                                 ),
#                             ),
#                             menu.item(
#                                 "python -m",
#                                 on_click=rx.call_script(
#                                     f"""document.getElementById("component-{slug}").innerText = "python -m buridan add";"""
#                                 ),
#                             ),
#                         ),
#                     ),
#                 ),
#                 class_name="flex w-full max-w-2xl items-stretch gap-2",
#             ),
#             class_name="flex flex-col items-start gap-4 max-w-xl",
#         ),
#         rx.el.button("Open Full Preview"),
#         class_name="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between",
#     )


# import reflex as rx

# from components.core.hugeicon import hi
# from components.ui.button import button, button_variants
# from components.ui.button_group import button_group
# from components.ui.menu import menu


# def intro(raw_arg):
#     intro = raw_arg.strip("[]").strip()

#     if "," not in intro:
#         raise ValueError(f"Invalid INTRO format: {raw_arg!r}")

#     title, description = intro.split(",", 1)

#     slug = title.strip().lower().replace(" ", "-")

#     return rx.el.div(
#         rx.el.div(
#             rx.el.h1(
#                 title.strip(),
#                 class_name="text-2xl leading-tight font-bold tracking-tighter",
#             ),
#             rx.el.p(
#                 description.strip(),
#                 class_name="text-sm text-muted-foreground",
#             ),
#             rx.el.div(
#                 rx.el.code(
#                     rx.el.span(
#                         "❯",
#                         class_name="shrink-0 select-none text-muted-foreground/50",
#                     ),
#                     rx.el.span(
#                         "buridan add",
#                         class_name="text-muted-foreground command-prefix",
#                     ),
#                     rx.el.span(
#                         f" {title.strip().lower()}",
#                         class_name="font-medium text-foreground",
#                     ),
#                     class_name=(
#                         "flex h-8 min-w-0 flex-1 items-center gap-2 "
#                         "overflow-x-auto border border-border bg-muted/40 "
#                         "px-3 font-mono text-xs whitespace-nowrap"
#                     ),
#                 ),
#                 button_group.root(
#                     button(
#                         "Copy",
#                         variant="outline",
#                         on_click=rx.toast("click"),
#                     ),
#                     menu.root(
#                         menu.trigger(
#                             hi("ArrowDown01Icon"),
#                             class_name=button_variants("outline"),
#                         ),
#                         menu.content(
#                             menu.group_label("Commands"),
#                             menu.separator(),
#                             menu.item(
#                                 "buridan",
#                                 on_click=rx.call_script(
#                                     """
#                                     localStorage.setItem(
#                                         "buridan-command",
#                                         "buridan add"
#                                     );

#                                     document
#                                       .querySelectorAll(".command-prefix")
#                                       .forEach(
#                                         el => el.innerText = "buridan add"
#                                       );
#                                     """
#                                 ),
#                             ),
#                             menu.item(
#                                 "uv run",
#                                 on_click=rx.call_script(
#                                     """
#                                     localStorage.setItem(
#                                         "buridan-command",
#                                         "uv run buridan add"
#                                     );

#                                     document
#                                       .querySelectorAll(".command-prefix")
#                                       .forEach(
#                                         el => el.innerText = "uv run buridan add"
#                                       );
#                                     """
#                                 ),
#                             ),
#                             menu.item(
#                                 "python -m",
#                                 on_click=rx.call_script(
#                                     """
#                                     localStorage.setItem(
#                                         "buridan-command",
#                                         "python -m buridan add"
#                                     );

#                                     document
#                                       .querySelectorAll(".command-prefix")
#                                       .forEach(
#                                         el => el.innerText = "python -m buridan add"
#                                       );
#                                     """
#                                 ),
#                             ),
#                         ),
#                     ),
#                 ),
#                 class_name="flex w-full max-w-2xl items-stretch gap-2",
#             ),
#             class_name="flex flex-col items-start gap-4 max-w-xl",
#         ),
#         rx.el.button("Open Full Preview"),
#         class_name="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between",
#     )


import reflex as rx

from components.core.hugeicon import hi
from components.ui.button import button, button_variants
from components.ui.button_group import button_group
from components.ui.menu import menu


def command_selector():
    return menu.root(
        menu.trigger(
            hi("ArrowDown01Icon"),
            class_name=button_variants("outline"),
        ),
        menu.content(
            menu.group_label("Commands"),
            menu.separator(),
            menu.item(
                rx.el.span(
                    "",
                    class_name="command-check w-4",
                ),
                rx.el.span("buridan"),
                id="command-option-cli",
                on_click=rx.call_script(
                    """
                    const command = "buridan add";

                    localStorage.setItem(
                        "buridan-command",
                        command
                    );

                    document
                      .querySelectorAll(".command-prefix")
                      .forEach(el => el.innerText = command);

                    document
                      .querySelectorAll(".command-check")
                      .forEach(el => el.innerText = "");

                    document
                      .querySelector("#command-option-cli .command-check")
                      .innerText = "✓";
                    """
                ),
            ),
            menu.item(
                rx.el.span(
                    "",
                    class_name="command-check w-4",
                ),
                rx.el.span("uv run"),
                id="command-option-uv",
                on_click=rx.call_script(
                    """
                    const command = "uv run buridan add";

                    localStorage.setItem(
                        "buridan-command",
                        command
                    );

                    document
                      .querySelectorAll(".command-prefix")
                      .forEach(el => el.innerText = command);

                    document
                      .querySelectorAll(".command-check")
                      .forEach(el => el.innerText = "");

                    document
                      .querySelector("#command-option-uv .command-check")
                      .innerText = "✓";
                    """
                ),
            ),
            menu.item(
                rx.el.span(
                    "",
                    class_name="command-check w-4",
                ),
                rx.el.span("python -m"),
                id="command-option-module",
                on_click=rx.call_script(
                    """
                    const command = "python -m buridan add";

                    localStorage.setItem(
                        "buridan-command",
                        command
                    );

                    document
                      .querySelectorAll(".command-prefix")
                      .forEach(el => el.innerText = command);

                    document
                      .querySelectorAll(".command-check")
                      .forEach(el => el.innerText = "");

                    document
                      .querySelector("#command-option-module .command-check")
                      .innerText = "✓";
                    """
                ),
            ),
        ),
    )


def intro(raw_arg):
    intro = raw_arg.strip("[]").strip()

    if "," not in intro:
        raise ValueError(f"Invalid INTRO format: {raw_arg!r}")

    title, description = intro.split(",", 1)
    slug = title.strip().lower().replace(" ", "-")
    copy_id = f"copy-command-{slug}"
    command_id = f"command-{slug}"

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
            rx.el.div(
                rx.el.code(
                    rx.el.span(
                        "❯",
                        class_name="shrink-0 select-none text-muted-foreground/50",
                    ),
                    rx.el.span(
                        "buridan add",
                        id=command_id,
                        class_name="text-muted-foreground command-prefix",
                    ),
                    rx.el.span(
                        f" {title.strip().lower()}",
                        class_name="font-medium text-foreground",
                    ),
                    class_name=(
                        "flex h-8 min-w-0 flex-1 items-center gap-2 "
                        "overflow-x-auto border border-border bg-muted/40 "
                        "px-3 font-mono text-xs whitespace-nowrap"
                    ),
                ),
                button_group.root(
                    button(
                        rx.el.span(
                            "Copy",
                            id=f"{copy_id}-text",
                        ),
                        variant="outline",
                        class_name="w-[80px]",
                        on_click=rx.call_script(
                            f"""
                            const command =
                              document.getElementById("{command_id}").innerText;

                            const component =
                              "{slug}";

                            navigator.clipboard.writeText(
                              `${{command}} ${{component}}`
                            );

                            const text =
                              document.getElementById("{copy_id}-text");

                            text.innerText = "Copied!";

                            setTimeout(() => {{
                              text.innerText = "Copy";
                            }}, 1000);
                            """
                        ),
                    ),
                    command_selector(),
                ),
                class_name="flex w-full max-w-2xl items-stretch gap-2",
            ),
            class_name="flex flex-col items-start gap-4 max-w-xl",
        ),
        rx.el.button("Open Full Preview"),
        class_name="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between mb-10",
    )
