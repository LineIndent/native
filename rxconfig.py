import reflex as rx
from reflex.plugins.shared_tailwind import TailwindConfig

config = rx.Config(
    app_name="native",
    show_built_with_reflex=False,
    telemetry_enabled=False,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(
            config=TailwindConfig(plugins=["@tailwindcss/typography"])
        ),
    ],
)
