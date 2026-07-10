from reflex.app import App

from native.hooks.head_components import APP_HEAD_COMPONENTS
from native.hooks.stylesheets import APP_STYLESHEETS
from native.export import export

app = App(
    enable_state=False,
    head_components=APP_HEAD_COMPONENTS,
    stylesheets=APP_STYLESHEETS,
)

export(app=app)
