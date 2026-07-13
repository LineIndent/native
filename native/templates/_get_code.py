# import reflex as rx
# from components.core.hugeicon import hi
# from components.ui.button import button, button_variants
# from components.ui.dialog import dialog
# from components.ui.separator import separator
# from native.templates._copy_btn import generate_component_id
# from reflex_components_core.el import div, p

# ADD_SWATCHES_JS = """
# (function() {
#     function injectSwatches() {
#         const block = document.getElementById("get-css-theme");
#         if (!block) return;
#         const code = block.querySelector("code") || block;
#         if (code.dataset.swatchesDone === "true") return;
#         code.innerHTML = code.textContent.replace(/oklch\([^)]+\)/g, (m) =>
#             `<span style="background-color:${m};width:.85em;height:.85em;display:inline-block;margin-right:.4em;border-radius:3px;border:1px solid rgba(255,255,255,.15);vertical-align:middle;flex-shrink:0;"></span>` + m
#         );
#         code.dataset.swatchesDone = "true";
#     }
#     setTimeout(injectSwatches, 40);
#     setTimeout(injectSwatches, 120);
#     setTimeout(injectSwatches, 300);
# })();
# """

# RXCONFIG = """import reflex as rx
# from reflex.plugins.shared_tailwind import TailwindConfig

# config = rx.Config(
#     ...,
#     plugins=[
#         rx.plugins.TailwindV4Plugin(
#             config=TailwindConfig(plugins=["@tailwindcss/typography"])
#         ),
#     ],
# )

# """

# def get_code():
#     test_tabs = [
#         {
#             "id": "globals",
#             "label": "globals.css",
#             "content": div(
#                 rx.el.pre(
#                 rx.el.code(id="get-css-theme", class_name="w-full")
#             ),
#             class_name="text-sm w-full h-full"
#         )
#         },
#         {
#             "id": "rxconfig",
#             "label": "rxconfig.py",
#             "content": div(
#                 rx.el.pre(
#                 rx.el.code(RXCONFIG, class_name="language-python w-full"),
#                 ),
#                 rx.el.pre(
#                 rx.el.code("""app = rx.App(stylesheets=[globals.css])""", class_name="language-python w-full"),
#                 ),
#                 class_name="w-full h-full"
#             )
#         },
#         {
#             "id": "rx.app",
#             "label": "rx.App",
#             "content": div(
#                 rx.el.pre(
#                 rx.el.code("""app = rx.App(stylesheets=[globals.css])""", class_name="language-python w-full"),
#                 ),
#                 class_name="w-full h-full"
#             )
#         },
#     ]

#     # 2. Setup the unique DOM ID and initial state just like before
#     demo_id = generate_component_id()
#     initial_view = "globals"

#     # 3. Build the Tab Buttons mapping dynamically
#     tab_buttons = []
#     for tab in test_tabs:
#         t_id = tab["id"]
#         label = tab["label"]
#         tab_buttons.append(
#             button(
#                 label,
#                 variant="outline",
#                 class_name=(
#                     f"font-normal flex-1 h-7 border-transparent bg-transparent "
#                     f"group-data-[view={t_id}]:bg-background group-data-[view={t_id}]:border-border"
#                 ),
#                 on_click=rx.call_script(
#                     f'document.getElementById("dialog-tabs-{demo_id}").dataset.view = "{t_id}";'
#                 ),
#             )
#         )

#     # 4. Build the Content Views mapping dynamically
#     tab_contents = []
#     for tab in test_tabs:
#         t_id = tab["id"]
#         content = tab["content"]
#         tab_contents.append(
#             div(
#                 content,
#                 class_name=(
#                     f"size-full overflow-x-auto p-2 hidden "
#                     f"group-data-[view={t_id}]:flex"
#                 ),
#             )
#         )

#     # 5. Assemble your Dialog
#     return dialog.root(
#         dialog.trigger(
#             button(
#                 "Get Code",
#                 class_name="w-full",
#                 id="copy-theme-button",
#                 type="button",
#                 on_click=lambda _: rx.call_script(ADD_SWATCHES_JS),
#             ),
#         ),
#         dialog.popup(
#             dialog.header(
#                 dialog.title("Compile Preset"),
#                 dialog.description(
#                     "Add the following CSS and theme tokens to your Reflex application to get started."
#                 ),
#                 div(
#                     # *tab_buttons,
#                     rx.el.div(
#                             rx.el.div(
#                                 rx.el.div(
#                                     *tab_buttons,
#                                     class_name="flex w-full gap-3 p-1.5",
#                                 ),
#                                 class_name="scrollbar-none overflow-x-auto w-full",
#                             ),
#                             class_name="mx-auto w-full overflow-hidden",
#                         ),
#                     class_name="flex items-center gap-1 w-full"
#                 ),
#                 div(
#                     rx.el.p(
#                         "Theme Tokens",
#                         class_name="text-foreground text-sm font-normal",
#                     ),
#                     rx.el.p(
#                         "Copy the CSS variables for this preset into your assets folder.",
#                         class_name="text-muted-foreground text-sm font-light pb-2",
#                     ),
#                     class_name="hidden group-data-[view=globals]:flex flex-col py-1"
#                 ),
#                 div(
#                     rx.el.p(
#                         "Tailwind Plugins",
#                         class_name="text-foreground text-sm font-normal",
#                     ),
#                     rx.el.p(
#                         "Copy the following plugins into your rxconfig.py file",
#                         class_name="text-muted-foreground text-sm font-light pb-2",
#                     ),
#                     class_name="hidden group-data-[view=rxconfig]:flex flex-col py-1"
#                 ),
#                 div(
#                     rx.el.p(
#                         "App Stylesheet",
#                         class_name="text-foreground text-sm font-normal",
#                     ),
#                     rx.el.p(
#                         "Import the globals.css into your app. Adjust path as needed.",
#                         class_name="text-muted-foreground text-sm font-light pb-2",
#                     ),
#                     class_name="hidden group-data-[view=rx.app]:flex flex-col py-1"
#                 ),
#             ),
#             div(
#                 *tab_contents,
#                 class_name="scrollbar-none h-[50vh] max-h-[50vh] overflow-y-auto",
#             ),
#             dialog.footer(
#                 rx.el.div(
#                     dialog.close(
#                         button("Cancel", type="button", variant="outline", class_name="flex-1"),
#                         class_name="flex-1",
#                     ),
#                     dialog.close(
#                         button(
#                             "Copy",
#                             type="button",
#                             class_name="flex-1",
#                             id="apply-preset-button",
#                         ),
#                         class_name="flex-1",
#                     ),
#                     class_name="w-full flex flex-row items-center justify-center gap-x-4",
#                 ),
#             ),
#             dialog.close(
#                 button(
#                     hi("Cancel01Icon", class_name="size-4"),
#                     variant="ghost",
#                     size="icon-sm",
#                     class_name=dialog.class_names.CLOSE_ICON,
#                 )
#             ),
#             id=f"dialog-tabs-{demo_id}",
#             data_view=initial_view,
#             class_name="group !max-w-md !p-4 !overflow-hidden"
#         ),
#     )


import reflex as rx
from components.core.hugeicon import hi
from components.ui.button import button
from components.ui.dialog import dialog
from native.templates._copy_btn import generate_component_id
from reflex_components_core.el import div

ADD_SWATCHES_JS = """
(function() {
    function injectSwatches() {
        const block = document.getElementById("get-css-theme");
        if (!block) return;
        const code = block.querySelector("code") || block;
        if (code.dataset.swatchesDone === "true") return;
        code.innerHTML = code.textContent.replace(/oklch\([^)]+\)/g, (m) =>
            `<span style="background-color:${m};width:.85em;height:.85em;display:inline-block;margin-right:.4em;border-radius:3px;border:1px solid rgba(255,255,255,.15);vertical-align:middle;flex-shrink:0;"></span>` + m
        );
        code.dataset.swatchesDone = "true";
    }
    setTimeout(injectSwatches, 40);
    setTimeout(injectSwatches, 120);
    setTimeout(injectSwatches, 300);
})();
"""

# Optimized Copy Script: Expects the explicit container ID and the button context
COPY_EXPLICIT_ID_JS = """
(function(btn, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const codeBlocks = container.querySelectorAll('code');
    const fullText = Array.from(codeBlocks).map(c => c.textContent).join('\\n\\n');

    navigator.clipboard.writeText(fullText).then(() => {
        const oldText = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => { btn.textContent = oldText; }, 1000);
    });
})(this, '{}');
"""

RXCONFIG = """import reflex as rx
from reflex.plugins.shared_tailwind import TailwindConfig

config = rx.Config(
    ...,
    plugins=[
        rx.plugins.TailwindV4Plugin(
            config=TailwindConfig(plugins=["@tailwindcss/typography"])
        ),
    ],
)
"""

def get_code():
    demo_id = generate_component_id()
    initial_view = "globals"

    # 1. Structured Tab Data with explicit target container IDs
    test_tabs = [
        {
            "id": "globals",
            "label": "globals.css",
            "container_id": f"code-container-globals-{demo_id}",
            "content": div(
                rx.el.pre(
                    rx.el.code(id="get-css-theme", class_name="w-full")
                ),
                id=f"code-container-globals-{demo_id}",
                class_name="text-sm w-full h-full"
            )
        },
        {
            "id": "rxconfig",
            "label": "rxconfig.py",
            "container_id": f"code-container-rxconfig-{demo_id}",
            "content": div(
                rx.el.pre(
                    rx.el.code(RXCONFIG, class_name="language-python w-full"),
                ),
                rx.el.pre(
                    rx.el.code("""app = rx.App(stylesheets=[globals.css])""", class_name="language-python w-full"),
                ),
                id=f"code-container-rxconfig-{demo_id}",
                class_name="w-full h-full"
            )
        },
        {
            "id": "rx.app",
            "label": "rx.App",
            "container_id": f"code-container-rxapp-{demo_id}",
            "content": div(
                rx.el.pre(
                    rx.el.code("""app = rx.App(stylesheets=[globals.css])""", class_name="language-python w-full"),
                ),
                id=f"code-container-rxapp-{demo_id}",
                class_name="w-full h-full"
            )
        },
    ]

    # 2. Build the Tab Buttons mapping dynamically
    tab_buttons = []
    for tab in test_tabs:
        t_id = tab["id"]
        label = tab["label"]
        tab_buttons.append(
            button(
                label,
                variant="outline",
                class_name=(
                    f"font-normal flex-1 h-7 border-transparent bg-transparent "
                    f"group-data-[view={t_id}]:bg-background group-data-[view={t_id}]:border-border"
                ),
                on_click=rx.call_script(
                    f'document.getElementById("dialog-tabs-{demo_id}").dataset.view = "{t_id}";'
                ),
            )
        )

    # 3. Build the Content Views mapping dynamically
    tab_contents = []
    for tab in test_tabs:
        t_id = tab["id"]
        content = tab["content"]
        tab_contents.append(
            div(
                content,
                class_name=(
                    f"size-full overflow-x-auto p-2 hidden "
                    f"group-data-[view={t_id}]:flex flex-col gap-y-2"
                ),
            )
        )

    # 4. Master Copy Action Router
    # Instead of reading the DOM layout, this looks up the active state and passes the target ID straight to the script
    js_switch_cases = "".join([
        f"case '{tab['id']}': targetId = '{tab['container_id']}'; break;" for tab in test_tabs
    ])

    ROUTED_COPY_JS = f"""
        (function(btn) {{
            const dialog = document.getElementById("dialog-tabs-{demo_id}");
            if (!dialog) return;
            const activeView = dialog.dataset.view;
            let targetId = '';

            switch(activeView) {{
                {js_switch_cases}
            }}

            const container = document.getElementById(targetId);
            if (!container) return;

            const codeBlocks = container.querySelectorAll('code');
            const fullText = Array.from(codeBlocks).map(c => c.textContent).join('\\n\\n');

            navigator.clipboard.writeText(fullText).then(() => {{
                const oldText = btn.textContent;
                btn.textContent = "Copied!";

                setTimeout(() => {{
                    btn.textContent = oldText;

                    // Programmatically trigger the dialog close handler
                    // by finding the nearest radix close button or dispatching an escape key event
                    const closeBtn = dialog.querySelector('[class*="radix-dialog-close"], button:has(svg)');
                    if (closeBtn) {{
                        closeBtn.click();
                    }} else {{
                        // Fallback: Dispatch an Escape key event to close the Radix Dialog
                        dialog.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Escape', bubbles: true }}));
                    }}
                }}, 1000);
            }});
        }})(this);
        """

    return dialog.root(
        dialog.trigger(
            button(
                "Get Code",
                class_name="w-full",
                id="copy-theme-button",
                type="button",
                on_click=lambda _: rx.call_script(ADD_SWATCHES_JS),
            ),
        ),
        dialog.popup(
            dialog.header(
                dialog.title("Compile Preset"),
                dialog.description(
                    "Add the following CSS and theme tokens to your Reflex application to get started."
                ),
                div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                *tab_buttons,
                                class_name="flex w-full gap-3 p-1.5",
                            ),
                            class_name="scrollbar-none overflow-x-auto w-full",
                        ),
                        class_name="mx-auto w-full overflow-hidden",
                    ),
                    class_name="flex items-center gap-1 w-full"
                ),
                div(
                    rx.el.p(
                        "Theme Tokens",
                        class_name="text-foreground text-sm font-normal",
                    ),
                    rx.el.p(
                        "Copy the CSS variables for this preset into your assets folder.",
                        class_name="text-muted-foreground text-sm font-light pb-2",
                    ),
                    class_name="hidden group-data-[view=globals]:flex flex-col py-1"
                ),
                div(
                    rx.el.p(
                        "Tailwind Plugins",
                        class_name="text-foreground text-sm font-normal",
                    ),
                    rx.el.p(
                        "Copy the following plugins into your rxconfig.py file",
                        class_name="text-muted-foreground text-sm font-light pb-2",
                    ),
                    class_name="hidden group-data-[view=rxconfig]:flex flex-col py-1"
                ),
                div(
                    rx.el.p(
                        "App Stylesheet",
                        class_name="text-foreground text-sm font-normal",
                    ),
                    rx.el.p(
                        "Import the globals.css into your app. Adjust path as needed.",
                        class_name="text-muted-foreground text-sm font-light pb-2",
                    ),
                    class_name="hidden group-data-[view=rx.app]:flex flex-col py-1"
                ),
            ),
            div(
                *tab_contents,
                class_name="scrollbar-none !h-[50vh] max-h-[50vh] overflow-y-auto",
            ),
            dialog.footer(
                rx.el.div(
                    dialog.close(
                        button("Cancel", type="button", variant="outline", class_name="flex-1"),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        button(
                            "Copy",
                            type="button",
                            class_name="w-full",
                            id="apply-preset-button",
                            on_click=rx.call_script(ROUTED_COPY_JS)
                        ),
                        class_name="w-full flex-1",
                    ),
                    class_name="w-full flex flex-row items-center justify-center gap-x-4",
                ),
            ),
            dialog.close(
                button(
                    hi("Cancel01Icon", class_name="size-4"),
                    variant="ghost",
                    size="icon-sm",
                    class_name=dialog.class_names.CLOSE_ICON,
                )
            ),
            id=f"dialog-tabs-{demo_id}",
            data_view=initial_view,
            class_name="group !max-w-md !p-4 !overflow-hidden"
        ),
    )
