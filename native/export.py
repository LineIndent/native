from reflex.app import App

from native.engine.generator import generate_docs_library
from native.pages.components import components_page
from native.pages.landing import landing_page
from native.pages.create import create_page
from native.pages.docs import docs_page
from native.templates.docpage import docpage
from native.templates.toc import table_of_content
from native.templates._meta_tags import generate_site_meta_tags


from reflex_components_core.el import div

def export(app: App):

    app.add_page(
        component=create_page(),
        route="/create"
    )

    app.add_page(
        component=landing_page(),
        route="/",
        title="The UI Library for Reflex Developers - buridan/ui",
        meta=generate_site_meta_tags(
            title="Buridan UI",
            url="/",
            description="Composable, themeable components designed for Reflex. Extend, override, and ship without fighting the framework. Open source.",
            social_card="index.webp",
        )
    )

    app.add_page(
        component=components_page(),
        route="/components",
        title="Components - buridan/ui",
        meta=generate_site_meta_tags(
            title="Components",
            url="/components",
            description="A collection of ready-to-use UI components for building modern applications. From simple controls to complex interface patterns, copy and paste into your apps.",
            social_card="components.webp",
        )
    )

    app.add_page(
        component=docs_page(),
        route="/docs",
        title="Documentation - buridan/ui",
        meta=generate_site_meta_tags(
            title="Documentation",
            url="/docs",
            description="Explore our comprehensive guides, core concepts, and developer resources to help you build and scale your applications.",
            social_card="docs.webp",
        )
    )

    # for doc in generate_docs_library():
    #     main_content = div(*doc.component, class_name="w-full")

    #     toc_content = (
    #         table_of_content(doc.url, doc.table_of_content)
    #         if not (doc.url.startswith("docs/components/") or doc.url.startswith("docs/charts/"))
    #         else None
    #     )
    #     title_s = doc.url.split("/")[-1].replace("-", " ").title()
    #     title = f"{title_s} – buridan/ui"
    #     card_path = f"{doc.url.split('/')[-1]}.webp"

    #     app.add_page(
    #         component=docpage(main_content, toc_content),
    #         route=f"/{doc.url}",
    #         title=title,
    #         meta=generate_site_meta_tags(
    #             title=title_s,
    #             url=f"{doc.url}",
    #             description=doc.description,
    #             social_card=card_path,
    #         ),
    #     )
