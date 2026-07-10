import reflex as rx
from components.ui.menu import menu
from components.ui.button import button_variants
from components.core.hugeicon import hi

def menu_icons() -> rx.Component:
    return menu.root(
        menu.trigger("Options", class_name=button_variants(variant="outline")),
        menu.content(
            menu.item(hi("UserIcon"), "Profile"),
            menu.item(hi("CreditCardIcon"), "Billing"),
            menu.item(hi("Setting07Icon"), "Settings"),
        )
    )
