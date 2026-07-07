from components.ui.table import table

COMPOSITION = table.root(
    table.header(
        table.row(
            table.head(),
        ),
    ),
    table.body(
        table.row(
            table.cell(),
        ),
    ),
    table.footer(),
    table.caption(),
)
