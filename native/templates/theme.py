from reflex_base.event import call_script
from reflex_components_core.el import svg

from components.ui.button import button
import reflex as rx

def theme_toggle_button():
    return button(
        svg(
            svg.path(
                d="M0 0h24v24H0z",
                fill="none",
                stroke="none",
            ),
            svg.path(
                d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0",
            ),
            svg.path(
                d="M12 3l0 18",
            ),
            svg.path(
                d="M12 9l4.65 -4.65",
            ),
            svg.path(
                d="M12 14.3l7.37 -7.37",
            ),
            svg.path(
                d="M12 19.6l8.85 -8.85",
            ),
            xmlns="http://www.w3.org/2000/svg",
            view_box="0 0 24 24",
            fill="none",
            stroke="currentColor",
            stroke_width="2",
            stroke_linecap="round",
            stroke_linejoin="round",
            class_name="size-4 !transition-none",
        ),
        on_click=lambda _: call_script(
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

        if (window.preview) {
            window.preview.applyAll();
            console.log('toggle fired, dark =', document.documentElement.classList.contains('dark'));
        } else {
            console.log('window.preview is undefined at toggle time');
        }
        """
        ),
        variant="ghost",
        size="sm",
    )
