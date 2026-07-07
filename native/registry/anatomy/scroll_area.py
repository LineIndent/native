from components.ui.scroll_area import scroll_area

COMPOSITION = scroll_area.root(
    scroll_area.viewport(
        scroll_area.content(),
    ),
    scroll_area.scrollbar(
        scroll_area.thumb(),
    ),
    scroll_area.corner(),
)
