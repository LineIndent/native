import reflex as rx

from native.templates._copy_btn import create_copy_button, generate_component_id
from reflex_components_core.el import div
from components.ui.button import button
from components.core.hugeicon import hi

def demo(component: rx.Component, source: str):
    demo_id = generate_component_id()
    copy_button, _ = create_copy_button(content=source)

    return div(
        div(
            div(
                div(
                    button(
                        hi("SearchIcon", class_name="size-3.5"),
                        variant="outline",
                        class_name=(
                            "size-7 preview-btn bg-background "
                            "group-data-[view=code]:bg-transparent "
                            "group-data-[view=code]:border-transparent"
                        ),

                        on_click=rx.call_script(
                            f"""
                            document.getElementById("demo-{demo_id}").dataset.view = "preview";
                            """
                        ),
                    ),
                    button(
                        hi("CodeIcon", class_name="size-3.5"),
                        variant="outline",
                        class_name=(
                            "size-7 code-btn border-transparent bg-transparent "
                            "group-data-[view=code]:border-border "
                            "group-data-[view=code]:bg-background"
                        ),
                        on_click=rx.call_script(
                            f"""
                            document.getElementById("demo-{demo_id}").dataset.view = "code";
                            """
                        ),
                    ),
                    class_name="flex items-center gap-1"
                ),
                class_name="flex items-center gap-2",
            ),
            div(
                copy_button,
                class_name="flex items-center gap-1 px-2"),
            class_name="flex items-stretch justify-between p-0.5 pb-0.5",
        ),
        div(
            div(
                component,
                class_name=(
                    "w-full flex-1 flex items-center justify-center px-2 py-4 sm:p-6 "
                    "group-data-[view=code]:hidden"
                ),
            ),
            div(
                rx.el.pre(
                    rx.el.code(
                        source,
                        class_name="language-python text-sm",
                    ),
                ),
                class_name=(
                    "size-full overflow-y-auto p-2 hidden "
                    "group-data-[view=code]:flex"
                ),
            ),
            class_name=(
                "relative m-0.5 mt-0 flex min-h-0 flex-1 flex-col "
                "overflow-hidden border bg-background "
                "dark:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.05)]"
            ),
        ),
        id=f"demo-{demo_id}",
        data_view="preview",
        class_name="group relative flex min-w-0 flex-col border bg-muted/50 min-h-[45vh]",
    )
