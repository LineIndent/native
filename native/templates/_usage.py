import reflex as rx

from native.registry.anatomy import ANATOMY

from native.templates._copy_btn import generate_component_id
from reflex_components_core.el import div, p, h1, span, strong
from components.ui.button import button

def _usage_demo(component_name: str):
    demo_id = generate_component_id()
    anatomy = ANATOMY.get(component_name)

    return div(
        div(
            div(
                div(
                    button(
                        "Basic Usage",
                        variant="outline",
                        class_name=(
                            "font-normal w-fit h-7 usage-btn bg-background "
                            "group-data-[view=anatomy]:bg-transparent "
                            "group-data-[view=anatomy]:border-transparent"
                        ),

                        on_click=rx.call_script(
                            f"""
                            document.getElementById("demo-{demo_id}").dataset.view = "usage";
                            """
                        ),
                    ),
                    button(
                        "Anatomy",
                        variant="outline",
                        class_name=(
                            "h-7 w-fit font-normal anatomy-btn border-transparent bg-transparent "
                            "group-data-[view=anatomy]:border-border "
                            "group-data-[view=anatomy]:bg-background"
                        ),
                        on_click=rx.call_script(
                            f"""
                            document.getElementById("demo-{demo_id}").dataset.view = "anatomy";
                            """
                        ),
                    ),
                    class_name="flex items-center gap-1"
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-stretch p-0.5 pb-0.5",
        ),
        div(
            div(
                rx.el.pre(
                    rx.el.code(
                        f"from components.ui.{component_name} import {component_name}",
                        class_name="language-python text-sm",
                        on_mount=rx.call_script("Prism.highlightAll()"),
                    ),
                ),
                class_name=(
                    "size-full overflow-x-auto p-2 flex "
                    "group-data-[view=anatomy]:hidden"
                ),
            ),
            div(
                rx.el.pre(
                    rx.el.code(
                        anatomy,
                        class_name="language-python text-sm",
                        on_mount=rx.call_script("Prism.highlightAll()"),
                    ),
                ),
                class_name=(
                    "size-full overflow-x-auto p-2 hidden "
                    "group-data-[view=anatomy]:flex"
                ),
            ),
            class_name=(
                "relative m-0.5 mt-0 flex min-h-0 flex-1 flex-col "
                "overflow-hidden border bg-background "
                "dark:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.05)]"
            ),
        ),
        id=f"demo-{demo_id}",
        data_view="usage",
        class_name="w-full group relative flex min-w-0 flex-col border bg-muted/50 min-h-10",
    )


def usage(raw_arg):
    return div(
        div(
            h1(
                "Component Guide",
                class_name="text-2xl leading-tight font-bold tracking-tighter",
            ),
            p(
                span("Use the following to build the "),
                strong(raw_arg.capitalize()),
                span(" component."),
                class_name="text-sm text-muted-foreground",
            ),
            _usage_demo(raw_arg),
            class_name="w-full flex flex-col items-start gap-4",
        ),
        class_name="w-full flex flex-col gap-6 mb-10",
    )
