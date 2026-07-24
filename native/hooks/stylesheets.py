GOOGLE_FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Inter:wght@300;400;700&"
    "family=Geist:wght@300;400;700&"
    "family=Geist+Mono:wght@300;400;700&"
    "family=Roboto:wght@300;400;700&"
    "family=Outfit:wght@300;400;700&"
    "family=Plus+Jakarta+Sans:wght@300;400;700&"
    "family=Public+Sans:wght@300;400;700&"
    "family=Playfair+Display:wght@400;700&"
    "family=Merriweather:wght@300;400;700&"
    "family=Lora:wght@400;700&"
    "family=Instrument+Serif:wght@400&"
    "family=Fira+Code:wght@400;700&"
    "family=JetBrains+Mono:wght@400;700&"
    "family=IBM+Plex+Mono:wght@400;700&"
    "family=Oxanium:wght@200..800&"  # --> my font!
    "display=swap"
)

APP_STYLESHEETS: list[str] = [
    "globals.css",
    "prism.css",
    "themes.css",
    "typeset.css",
    GOOGLE_FONTS_URL,
]
