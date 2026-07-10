from reflex.event import call_script
from reflex_components_core.el import div, section

from native.templates.footer import _footer
from native.templates.navbar import navbar


def docpage(main_content, toc_content):
    return div(
        div(
            navbar(),
            div(
                section(
                    div(main_content, class_name="mx-auto flex w-full flex-col gap-8"),
                    _footer(),
                    class_name="flex min-h-screen flex-col gap-16",
                ),
                class_name="mx-auto min-h-screen max-w-5xl px-4 pt-10",
            ),
        ),
        on_mount=[call_script(
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
        call_script(
            """
            requestAnimationFrame(() => {
                Prism.highlightAll();
            });
            """
        ),
        ]
    )
