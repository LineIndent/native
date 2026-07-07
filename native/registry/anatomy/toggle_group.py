from components.ui.toggle_group import toggle_group

COMPOSITION = toggle_group(
    toggle_group.item("Option 1", value="1"),
    toggle_group.item("Option 2", value="2"),
)
