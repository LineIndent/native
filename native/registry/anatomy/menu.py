from components.ui.menu import menu

COMPOSITION = menu.root(
    menu.trigger(),
    menu.content(
        menu.group_label(),
        menu.item(menu.shortcut()),
        menu.separator(),
        menu.group_label(),
        menu.close(),
    ),
)
