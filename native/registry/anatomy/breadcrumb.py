from components.ui.breadcrumb import breadcrumb

COMPOSITION = breadcrumb.root(
    breadcrumb.list(
        breadcrumb.item(
            breadcrumb.link(),
        ),
        breadcrumb.separator(),
        breadcrumb.item(
            breadcrumb.page(),
        ),
    ),
)
