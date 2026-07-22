---
title: "Table"
description: "Powerful table and datagrids with built-in features."
order: 0
---

--INTRO([Table, Powerful table and datagrids with built-in features.])--

--USAGE(table)--

--SOURCE(table)--

# Examples

## Basic Table

--DEMO(table_block)--

## Table Invoice

--DEMO(table_demo_two)--

# API Reference

## table.root

The main container component. Renders the table shell — optional search toolbar, the scrollable `<table>`, and an optional pagination footer — and initializes the client-side controller that handles sorting, search, pagination, and row selection entirely in JS (no server round-trip).

If you plan to place a `table.search()` somewhere outside the table, give `id` an explicit, stable value so it can be targeted reliably.

```python
table.root(
    table.header(...),
    table.body(...),
    id="invoices-table",
    searchable=True,
    paginate=True,
    page_size=10,
)
```

| Prop         | Type   | Default          |
| ------------ | ------ | ---------------- |
| `searchable` | `bool` | `False`          |
| `paginate`   | `bool` | `False`          |
| `page_size`  | `int`  | `5`              |
| `id`         | `str`  | _Auto-generated_ |
| `class_name` | `str`  | `""`             |

## table.search

A standalone search input that can be placed anywhere on the page — inside the table, in a page header, in a sidebar — and still filters a specific table. It's linked purely by `for_table` matching that table's `id`, using an event listener on the document rather than DOM position, so mount order doesn't matter. Multiple `table.search()` instances can target the same table.

```python
table.search(
    for_table="invoices-table",
    placeholder="Search invoices…",
)
```

| Prop          | Type  | Default     |
| ------------- | ----- | ----------- |
| `for_table`   | `str` | _Required_  |
| `placeholder` | `str` | `"Search…"` |
| `class_name`  | `str` | `""`        |

## table.header

Wraps the header row(s) in a sticky, styled `<thead>`.

```python
table.header(
    table.row(
        table.head("Name"),
        table.head("Amount", sort_key="amount"),
    )
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## table.body

Wraps the data rows in `<tbody>`. This is the element the client-side controller reads and reorders — sorting, search, and pagination all operate on the `<tr>` children found here.

```python
table.body(
    table.row(
        table.cell("Brand identity design"),
        table.cell("$3,200.00", sort_value=3200.0),
    )
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## table.footer

An optional `<tfoot>` for summary or total rows, rendered below the body and excluded from sorting/search/pagination.

```python
table.footer(
    table.row(
        table.cell("Total", col_span=2),
        table.cell("$12,450.00"),
    )
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## table.row

A single `<tr>`. Used inside `table.header`, `table.body`, or `table.footer`.

```python
table.row(
    table.cell("Invoice"),
    table.cell("Client"),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## table.head

A `<th>` header cell. Passing `sort_key` turns it into a clickable sortable column, wiring up the click handler and the chevron sort-direction indicators automatically. Omit it for a plain, non-sortable header.

```python
table.head("Client")                          # plain
table.head("Amount", sort_key="amount", class_name="text-right")  # sortable
```

| Prop         | Type          | Default |
| ------------ | ------------- | ------- |
| `sort_key`   | `str \| None` | `None`  |
| `class_name` | `str`         | `""`    |

## table.cell

A `<td>` data cell. By default, sorting compares each cell's rendered text. Pass `sort_value` whenever the displayed text isn't directly sortable — formatted currency, dates, or any derived/computed value — and it'll be compared instead.

```python
table.cell(
    "$3,200.00",
    sort_value=3200.0,
    class_name="text-right",
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `sort_value` | `Any` | `None`  |
| `class_name` | `str` | `""`    |

## table.caption

An optional `<caption>`, rendered below the table for a lightweight description or footnote. Not involved in sorting/search/pagination.

```python
table.caption(
    "Billed to ",
    rx.el.span("Acme Inc.", class_name="font-medium"),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## Row selection (opt-in convention)

There's no dedicated `table.select_all()` / `table.select()` component — selection is wired through plain `checkbox.root()` calls plus two data attributes the controller looks for. This keeps the checkbox styling entirely in your control.

```python
# Header — select-all checkbox
table.head(
    checkbox.root(checkbox.indicator(), **{"data-dt-select-all": "true"}),
    class_name="w-10",
)

# Row — must have a unique `value` (e.g. a row id)
table.cell(
    checkbox.root(
        checkbox.indicator(),
        value=invoice["id"],
        **{"data-dt-select": "true"},
    )
)
```

Selection state lives in the browser only. To read it (e.g. for a "Delete selected" button), listen for the `dt-selection-change` custom event dispatched on the table's root element:

```python
rx.el.div(
    ...,
    on_mount=rx.call_script(
        """
        document.getElementById('invoices-table').addEventListener(
            'dt-selection-change',
            (e) => console.log(e.detail.selected)
        )
        """
    ),
)
```

`e.detail.selected` is a list of the `value`s currently checked, kept in sync across sorting, search, and pagination.
