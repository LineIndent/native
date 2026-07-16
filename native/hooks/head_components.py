from reflex_base.components.component import Component
from reflex_components_core.el import link, script

_THEME_LOGIC = """
(function() {
    try {
        const html = document.documentElement;
        function applyTheme() {
            let savedTheme = localStorage.getItem('site-theme');
            if (!savedTheme) savedTheme = 'dark'; // Your default fallback
            // Sync all keys to keep Reflex happy
            localStorage.setItem('site-theme', savedTheme);
            localStorage.setItem('theme', savedTheme);
            localStorage.setItem('last_compiled_theme', savedTheme);
            if (savedTheme === 'light') {
                if (!html.classList.contains('light')) html.classList.add('light');
                if (html.classList.contains('dark')) html.classList.remove('dark');
                html.style.colorScheme = 'light';
            } else {
                if (!html.classList.contains('dark')) html.classList.add('dark');
                if (html.classList.contains('light')) html.classList.remove('light');
                html.style.colorScheme = 'dark';
            }
        }
        applyTheme();
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.attributeName === 'class' || mutation.attributeName === 'style') {
                    // Temporarily turn off observer to avoid infinite loops, apply theme, then turn back on
                    observer.disconnect();
                    applyTheme();
                    startObserving();
                }
            });
        });
        function startObserving() {
            observer.observe(html, { attributes: true });
        }
        startObserving();
        window.addEventListener('load', applyTheme);
    } catch (e) {}
})();
"""


APP_HEAD_COMPONENTS: list[Component] = [
    link(rel="preconnect", href="https://fonts.googleapis.com"),
    link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="true"),
    script(src="/prism.js"),
    script(src="/theme-preview.js"),
    script(src="/typeset-preview.js"),
    script(_THEME_LOGIC),
]
