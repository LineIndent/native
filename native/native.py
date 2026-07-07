import reflex as rx
from reflex.app import App

from native.engine.generator import generate_docs_library
from native.hooks.head_components import APP_HEAD_COMPONENTS
from native.hooks.stylesheets import APP_STYLESHEETS
from native.pages.landing import landing_page
from native.templates.docpage import docpage
from native.templates.toc import table_of_content

app = App(
    enable_state=False,
    head_components=APP_HEAD_COMPONENTS,
    stylesheets=APP_STYLESHEETS,
)


app.add_page(
    component=landing_page(),
    route="/",
)

for doc in generate_docs_library():
    main_content = rx.el.div(*doc.component, class_name="w-full")
    toc_content = table_of_content(doc.url, doc.table_of_content)

    app.add_page(
        component=docpage(main_content, toc_content),
        route=f"/{doc.url}",
    )
