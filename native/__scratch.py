import reflex as rx
from reflex.experimental import ClientStateVar
from reflex_components_core.el import svg

from components.avatar import avatar
from components.checkbox import checkbox
from components.code import code
from components.core import cn
from components.dialog import dialog
from components.hugeicon import hi
from components.menu import menu
from components.separator import separator
from components.slider import slider
from native.hooks.head_components import APP_HEAD_COMPONENTS
from native.hooks.stylesheets import APP_STYLESHEETS

_test = ClientStateVar.create("test", 40)


def native_menu_demo():
    MENU_ID = "profile-menu"

    return rx.el.div(
        menu.root(
            menu.trigger(
                # "Open Menu",
                rx.el.span("Open Actions Menu"),
                class_name=(
                    "inline-flex items-center justify-center px-4 py-2 "
                    "bg-primary text-primary-foreground rounded-lg font-medium "
                    "cursor-pointer list-none select-none transition-colors "
                    "hover:bg-primary/90 focus-within:ring-2 focus-within:ring-ring "
                    "[&::-webkit-details-marker]:hidden"
                ),
            ),
            menu.content(
                # Example 1: Standard navigation/event + Auto Close
                menu.item(
                    rx.el.a(
                        "Go to Dashboard",
                        href="/dashbaord",
                    ),
                    # "Go to Dashboard",
                    # menu_id=MENU_ID,
                    # on_click=rx.redirect("/dashboard"),
                ),
                # Example 2: Multiple backend events chained together + Auto Close
                menu.item(
                    "Refresh & Toast",
                    menu_id=MENU_ID,
                    on_click=[rx.toast("Data updated successfully!")],
                ),
                # Example 3: Just close visually without triggering anything else
                menu.item("Nevermind", menu_id=MENU_ID),
                class_name="w-[300px]",
            ),
            id=MENU_ID,
        ),
        class_name="",
    )


def my_page():
    sample_code = """def hello_world():
    print("Hello from Reflex!")
    return True"""

    return rx.el.div(
        rx.el.h3(
            "Check out this source code:", class_name="text-lg font-semibold mb-2"
        ),
        # Invoke your sleek new component!
        code(sample_code, class_name="w-full max-w-lg"),
        class_name="",
    )


def avatar_example():
    return avatar.root(
        avatar.image(
            src="https://images.unsplash.com/photo-1543610892-0b1f7e6d8ac1?w=128&h=128&dpr=2&q=80",
            alt="Jane Doe",
            fallback_id="avatar-1-fallback",
        ),
        avatar.fallback("JD", fallback_id="avatar-1-fallback"),
        avatar.badge(
            class_name="bg-green-600 dark:bg-green-800",
        ),
        size="lg",
    )


def dialog_example():
    return dialog.popup(
        dialog.header(
            dialog.title("Settings"),
            dialog.description("Manage your preferences."),
        ),
        dialog.close("X", dialog_id="settings-dialog", variant="icon"),
        dialog.footer(
            dialog.close(
                "Cancel",
                dialog_id="settings-dialog",
            ),
        ),
        dialog_id="settings-dialog",
        dismissible=True,
    )


def separator_vertical() -> rx.Component:
    return rx.el.div(
        rx.el.div("Blog"),
        separator(orientation="vertical"),
        rx.el.div("Docs"),
        separator(orientation="vertical"),
        rx.el.div("Source"),
        class_name="flex h-5 items-center gap-4 text-sm",
    )


rx.el.div(
    rx.el.button(
        "Toggle Theme",
        on_click=rx.call_script(
            """
                        const html = document.documentElement;
                        let targetTheme = 'dark';
                        if (html.classList.contains('dark')) {
                            html.classList.remove('dark');
                            html.classList.add('light');
                            html.style.colorScheme = 'light';
                            targetTheme = 'light';
                        } else {
                            html.classList.remove('light');
                            html.classList.add('dark');
                            html.style.colorScheme = 'dark';
                            targetTheme = 'dark';
                        }
                        localStorage.setItem('site-theme', targetTheme);
                        localStorage.setItem('theme', targetTheme);
                        localStorage.setItem('last_compiled_theme', targetTheme);
            """
        ),
        class_name=(
            "px-4 py-2 rounded-lg text-sm font-medium transition-colors "
            "bg-muted hover:bg-muted/80 text-foreground border border-border"
        ),
    ),
    my_page(),
    rx.el.div(
        # The 'prose' class tells Tailwind to auto-style all raw HTML tags inside this div
        rx.el.h1("Getting Started with the Components"),
        rx.el.p(
            "Welcome to the official documentation. Everything you see here is rendered using "
            "native HTML tags combined with Tailwind's typography system. No Markdown parsers required!"
        ),
        rx.el.div(
            rx.el.p(
                "⚡ Interactive Live Preview Element",
                class_name="font-mono text-xs opacity-70",
            ),
            rx.el.button(
                "Click Me to Test State",
                class_name="mt-2 px-3 py-1 bg-primary text-primary-foreground rounded-md text-sm shadow",
            ),
            # 'not-prose' completely isolates this component from parent prose styles
            class_name="not-prose my-6 p-4 rounded-xl border border-border bg-card text-card-foreground shadow-sm",
        ),
        rx.el.h2("Installation Steps"),
        rx.el.p(
            "To initialize your development environment, run the following native command:"
        ),
        # Code snippets style themselves automatically
        rx.el.pre(rx.el.code("pip install reflex")),
        rx.el.h2("Key Features"),
        rx.el.ul(
            rx.el.li("Zero Markdown parsing overhead."),
            rx.el.li("Native dark mode integration via variables."),
            rx.el.li("Semantic HTML syntax for cleaner layouts."),
        ),
        # Responsive, framework-aware prose wrapper classes
        class_name="prose dark:prose-invert max-w-none p-6 text-foreground",
    ),
    # slider.root(
    #     slider.input(default_value=40, min=0, max=100, step=1, name="volume"),
    # ),
    # slider.root(
    #     slider.value(f"{_test.value}%"),
    #     slider.input(default_value=40, min=0, max=100, on_change=_test.set_value),
    #     class_name="gap-2",
    # ),
    # native_menu_demo(),
    # avatar_example(),
    # checkbox.root(
    #     checkbox.indicator(
    #         class_name="size-10",
    #     ),
    #     default_checked=True,
    #     name="terms",
    #     class_name="size-10",
    # ),
    # rx.el.label(
    #     checkbox.root(checkbox.indicator()),
    #     rx.el.span("Accept terms", class_name="text-sm"),
    #     class_name="flex items-center gap-2",
    # ),
    # dialog.trigger(rx.el.button("Open dialog"), dialog_id="settings-dialog"),
    # dialog_example(),
    # separator_vertical(),
    class_name="w-full min-h-screen flex flex-col gap-y-6 items-center justify-center",
)
