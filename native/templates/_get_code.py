import reflex as rx
from components.ui.button import button




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

PLUGIN_STRING="""import reflex as rx
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

APP_CONFIG="""app = rx.App(stylesheets=[globals.css])"""



def get_code_section(title: str, description: str, component: rx.Component, has_copy: bool = False):

    if has_copy:
        copy_id = "css-theme-copy"

        copy_btn = button(
            rx.el.span("Copy", id=f"{copy_id}-text"),
            variant="outline",
            class_name="w-full mt-2",
            id="copy-css-preset",
            type="button",
        )

    else:
        copy_btn = rx.el.div(class_name="hidden")

    return rx.el.div(
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-foreground text-sm font-medium",
            ),
            rx.el.p(
                description,
                class_name="text-muted-foreground text-sm font-light pb-2",
            ),
            rx.el.div(
                component,
                class_name="max-h-[45vh] overflow-y-scroll scrollbar-none p-4 bg-muted/60 rounded-xl"
            ),
            copy_btn,
            class_name="w-full flex flex-col gap-y-1",
        ),
        class_name="flex flex-col gap-y-2"
    )


def get_code():
    return rx.el.div(
        get_code_section(
            title="1. Theme Tokens",
            description="Copy the following CSS variables for this preset into your assets/globals.css file.",
            component=rx.el.pre(
                 rx.el.code(id="get-css-theme", class_name="language-python w-full"),
             ),
             has_copy=True,
        ),
        get_code_section(
            title="2. Tailwind Plugins",
            description="Copy the following plugins into your rxconfig.py file",
            component=rx.el.pre(
                 rx.el.code(PLUGIN_STRING, class_name="language-python w-full")
             ),
        ),
        get_code_section(
            title="3. App Config",
            description="Import the globals.css into your app. Adjust path as needed.",
            component=rx.el.pre(
                 rx.el.code(APP_CONFIG, class_name="language-python w-full")
             ),
        ),
        class_name="w-full h-full p-4 overflow-y-scroll overscroll-y-none flex flex-col gap-y-6 scrollbar-none"
    )
