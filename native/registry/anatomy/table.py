from components.ui.table import table

COMPOSITION = table.root(
    table.search(for_table=""),
    table.header(
        table.row(
            table.head(),
        )
    ),
    table.body(
        table.row(
            table.cell(),
        )
    ),
)
