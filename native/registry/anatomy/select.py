from components.ui.select import select

COMPOSITION = select.root(
    select.trigger(
        select.value(),
        select.icon(),
    ),
    select.portal(
        select.positioner(
            select.popup(
                select.group(
                    select.group_label(),
                    select.item(
                        select.item_text(),
                        select.item_indicator(),
                    ),
                ),
                select.separator(),
            ),
        ),
    ),
)
