from components.ui.select import select

COMPOSITION = select(
    select.option(),
    select.optgroup(
        select.option(),
        select.option(),
    ),
    select.optgroup(
        select.option(),
        select.option(),
    ),
)
