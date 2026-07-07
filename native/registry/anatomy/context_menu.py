from components.ui.context_menu import context_menu

COMPOSITION = context_menu.root(
    context_menu.trigger(),
    context_menu.portal(
        context_menu.positioner(
            context_menu.popup(
                context_menu.item(),
                context_menu.separator(),
                context_menu.group(
                    context_menu.group_label(),
                    context_menu.item(),
                ),
                context_menu.checkbox_item(
                    context_menu.checkbox_item_indicator(),
                ),
                context_menu.radio_group(
                    context_menu.radio_item(
                        context_menu.radio_item_indicator(),
                    ),
                ),
                context_menu.sub(
                    context_menu.sub_trigger(),
                    context_menu.positioner(
                        context_menu.popup(),
                    ),
                ),
            ),
        ),
    ),
)
