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
        on_mount=call_script(
            """
            const command = localStorage.getItem("buridan-command");

            if (!command) {
                localStorage.setItem(
                    "buridan-command",
                    "buridan add"
                );
            }

            const activeCommand =
                localStorage.getItem("buridan-command");

            document
              .querySelectorAll(".command-prefix")
              .forEach(el => el.innerText = activeCommand);

            document
              .querySelectorAll(".command-check")
              .forEach(el => el.innerText = "");

            if (activeCommand === "buridan add") {
                document
                  .querySelector("#command-option-cli .command-check")
                  .innerText = "✓";
            }

            if (activeCommand === "uv run buridan add") {
                document
                  .querySelector("#command-option-uv .command-check")
                  .innerText = "✓";
            }

            if (activeCommand === "python -m buridan add") {
                document
                  .querySelector("#command-option-module .command-check")
                  .innerText = "✓";
            }
            """
        ),
    )
