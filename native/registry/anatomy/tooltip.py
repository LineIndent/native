from components.ui.tooltip import tooltip

COMPOSITION = tooltip.root(
    tooltip.trigger(),
    tooltip.portal(
        tooltip.positioner(
            tooltip.popup(
                tooltip.arrow(),
                "Tooltip content",
            ),
        ),
    ),
)
