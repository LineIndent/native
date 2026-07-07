import reflex as rx
from reflex.plugins.shared_tailwind import TailwindConfig

config = rx.Config(
    app_name="native",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(
            config=TailwindConfig(plugins=["@tailwindcss/typography"])
        ),
    ],
)
