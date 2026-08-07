from components.ui.radio_group import radio_group

COMPOSITION = radio_group.root(
    radio_group.item(name="plan", value="free"),
    radio_group.item(name="plan", value="pro"),
)
