from components.ui.button import button
from components.ui.button_group import button_group

COMPOSITION = button_group.root(
    button(),
    button_group.separator(),
)
