from components.ui.timeline import timeline

COMPOSITION = timeline.root(
    timeline.item(
        timeline.indicator(),
        timeline.separator(),
        timeline.header(
            timeline.date(),
            timeline.title(),
        ),
        timeline.content(),
        step=1,
        active_step=1,
    ),
)
