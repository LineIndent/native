import reflex as rx

from native.templates.footer import _footer
from native.templates.navbar import navbar
from native.templates.sidebar import sidebar


def docpage(main_content, toc_content):

    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                sidebar(),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            main_content,
                            class_name="mx-auto flex w-full max-w-[50rem] min-w-0 flex-1 px-4 py-8 md:px-0 lg:py-10",
                        ),
                        class_name="flex-1 min-w-0",
                    ),
                    toc_content,
                    class_name="flex items-start w-full flex-1 min-w-0 gap-x-10",
                ),
                class_name="flex w-full gap-x-10 xl:max-w-[96rem] 2xl:max-w-[96rem] mx-auto px-2 md:px-8",
            ),
            class_name="w-full",
        ),
        _footer(),
        class_name="bg-background relative flex min-h-screen flex-col",
        on_mount=[
            rx.call_script(
                """
                (() => {
                    try {
                        const DEFAULT_COMMAND = "buridan add";

                        const get = (selector) => document.querySelector(selector);

                        const setText = (selector, text) => {
                            const el = get(selector);
                            if (el) {
                                el.innerText = text;
                            }
                        };

                        let activeCommand = localStorage.getItem("buridan-command");

                        if (!activeCommand) {
                            activeCommand = DEFAULT_COMMAND;
                            localStorage.setItem("buridan-command", activeCommand);
                        }

                        document.querySelectorAll(".command-prefix").forEach(el => {
                            el.innerText = activeCommand;
                        });

                        document.querySelectorAll(".command-check").forEach(el => {
                            el.innerText = "";
                        });

                        switch (activeCommand) {
                            case "buridan add":
                                setText("#command-option-cli .command-check", "✓");
                                break;

                            case "uv run buridan add":
                                setText("#command-option-uv .command-check", "✓");
                                break;

                            case "python -m buridan add":
                                setText("#command-option-module .command-check", "✓");
                                break;
                        }
                    } catch (err) {
                        console.error("Failed to initialize command selector:", err);
                    }
                })();
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


# def _docpage(main_content, toc_content):
#     return div(
#         navbar(),
#         div(
#             div(
#                 div(
#                     section(
#                         div(
#                             main_content,
#                             class_name="mx-auto flex w-full flex-col gap-8",
#                         ),
#                         class_name="flex min-h-screen flex-col gap-16",
#                     ),
#                     class_name="min-w-0 flex-1",
#                 ),
#                 toc_content if toc_content else div(class_name="hidden"),
#                 class_name="mx-auto flex max-w-3xl xl:max-w-5xl gap-20 px-4 sm:px-2.5",
#             ),
#             _footer(),
#             class_name="min-h-screen pt-10",
#         ),
#         on_mount=[
#             call_script(
#                 """
#                 (() => {
#                     try {
#                         const DEFAULT_COMMAND = "buridan add";

#                         const get = (selector) => document.querySelector(selector);

#                         const setText = (selector, text) => {
#                             const el = get(selector);
#                             if (el) {
#                                 el.innerText = text;
#                             }
#                         };

#                         let activeCommand = localStorage.getItem("buridan-command");

#                         if (!activeCommand) {
#                             activeCommand = DEFAULT_COMMAND;
#                             localStorage.setItem("buridan-command", activeCommand);
#                         }

#                         document.querySelectorAll(".command-prefix").forEach(el => {
#                             el.innerText = activeCommand;
#                         });

#                         document.querySelectorAll(".command-check").forEach(el => {
#                             el.innerText = "";
#                         });

#                         switch (activeCommand) {
#                             case "buridan add":
#                                 setText("#command-option-cli .command-check", "✓");
#                                 break;

#                             case "uv run buridan add":
#                                 setText("#command-option-uv .command-check", "✓");
#                                 break;

#                             case "python -m buridan add":
#                                 setText("#command-option-module .command-check", "✓");
#                                 break;
#                         }
#                     } catch (err) {
#                         console.error("Failed to initialize command selector:", err);
#                     }
#                 })();
#                 """
#             ),
#             call_script(
#                 """
#                 requestAnimationFrame(() => {
#                     Prism.highlightAll();
#                 });
#                 """
#             ),
#         ],
#     )
