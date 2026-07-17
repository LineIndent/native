from components.ui.attachment import attachment

COMPOSITION = attachment.root(
    attachment.media(),
    attachment.content(
        attachment.title(),
        attachment.description(),
    ),
    attachment.actions(attachment.action()),
)
