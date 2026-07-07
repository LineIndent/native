from components.ui.message import message

COMPOSITION = message.group(
    message.root(
        message.avatar(),
        message.content(
            message.header(),
            message.footer(),
        ),
    ),
)
