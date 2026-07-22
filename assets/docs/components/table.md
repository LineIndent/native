---
title: "Table"
description: "Powerful table and datagrids with built-in features."
order: 0
---


## Table, Powerful Table And Datagrids With Built-In Features.



> Component `table` not found


```python
from typing import Any

from reflex.components.component import Component
from reflex.utils.imports import ImportVar
from reflex.vars import FunctionVar, Var
from reflex.vars.base import VarData

PACKAGE_CN = "clsx-for-tailwind@1.0.0"
CN = Var(
    "cn",
    _var_data=VarData(
        imports={
            PACKAGE_CN: ImportVar(tag="cn"),
        },
    ),
).to(FunctionVar)


class CoreComponent(Component):
    unstyled: Var[bool]

    @classmethod
    def set_class_name(
        cls, default_class_name: str | Var[str], props: dict[str, Any]
    ) -> None:

        if "render_" in props:
            return

        props_class_name = props.get("class_name", "")

        if props.pop("unstyled", False):
            props["class_name"] = props_class_name
            return

        props["class_name"] = cn(default_class_name, props_class_name)

    def _exclude_props(self) -> list[str]:
        return [
            *super()._exclude_props(),
            "unstyled",
        ]


def cn(*classes: Var | str | tuple | list | None) -> Var:
    return CN.call(*classes).to(str)
```

```python
import uuid
from typing import Any, Literal

import reflex as rx
from reflex.components.component import Component, ComponentNamespace
from reflex_components_core.el import (
    Caption,
    Div,
    Table,
    Tbody,
    Td,
    Tfoot,
    Th,
    Thead,
    Tr,
)

from ..core.core import CoreComponent
from .input import ClassNames as InputStyle

LiteralAlign = Literal["left", "center", "right"]


class ClassNames:
    ROOT = "w-full rounded-lg border border-input bg-card"
    SCROLL = "w-full overflow-auto"
    TABLE = "w-full caption-bottom text-sm border-collapse"
    HEADER = "[&_tr]:border-b bg-secondary/50 backdrop-blur-sm sticky top-0"
    BODY = "[&_tr:last-child]:border-0"
    FOOTER = "border-t bg-muted/50 font-medium [&>tr]:last:border-b-0"
    ROW = "border-b transition-colors data-[state=selected]:bg-muted has-[:checked]:bg-muted/60 hover:bg-muted/50"
    HEAD = "h-10 px-4 text-left align-middle font-semibold text-muted-foreground [&:has([role=checkbox])]:pr-0 whitespace-nowrap"
    HEAD_SORT_BTN = (
        "flex items-center gap-1 cursor-pointer select-none hover:text-foreground"
    )
    CELL = "px-4 py-2 align-middle [&:has([role=checkbox])]:pr-0"
    CAPTION = "mt-4 text-sm text-muted-foreground"
    TOOLBAR = "flex items-center justify-between gap-2 p-3 border-b border-input"
    SEARCH_INPUT = "h-9 w-56 rounded-md border border-input bg-background px-3 text-sm outline-hidden focus:ring-1 focus:ring-ring"
    PAGINATION = "flex items-center justify-between gap-2 p-3 border-t border-input text-xs text-muted-foreground"
    PAGE_BUTTON = "h-8 rounded-md border border-input px-3 text-xs disabled:opacity-40 disabled:cursor-not-allowed"


def _chevron_icon(path_d: str | list[str], **props) -> Component:
    paths = [path_d] if isinstance(path_d, str) else path_d
    return rx.el.svg(
        *[rx.el.path(d=p) for p in paths],
        view_box="0 0 24 24",
        width="14",
        height="14",
        fill="none",
        stroke="currentColor",
        stroke_width="2",
        stroke_linecap="round",
        stroke_linejoin="round",
        **props,
    )


def _sort_icons() -> list[Component]:
    return [
        _chevron_icon(
            "m18 15-6-6-6 6",
            **{"data-dt-sort-icon": "asc"},
            style={"display": "none"},
        ),
        _chevron_icon(
            "m6 9 6 6 6-6",
            **{"data-dt-sort-icon": "desc"},
            style={"display": "none"},
        ),
        _chevron_icon(
            ["m7 15 5 5 5-5", "m7 9 5-5 5 5"],
            **{"data-dt-sort-icon": "none"},
            class_name="shrink-0 opacity-40",
        ),
    ]


# --------------------------------------------------------------------------
# Client-side controller. Returned from `add_custom_code`, so Reflex
# de-duplicates it and injects it once per page no matter how many
# <TableRoot> instances exist — same idea as the per-instance scripts
# in dialog.py, just shared instead of inlined per node.
#
# Opt-in hooks (all via data-* attributes, none required):
#   [data-dt-search-for="tableId"]  search input, anywhere on the page —
#                                    see TableSearch / table.search()
#   [data-dt-sort="key"]            sortable header button (paired with a
#                                    `data-sort-value` attr on the matching
#                                    <td>, or falls back to that cell's text)
#   [data-dt-prev] / [data-dt-next] / [data-dt-info] / [data-dt-page-label]
#                                    pagination controls
#   [data-dt-select-all]            header "select all" checkbox <input>
#   [data-dt-select]                per-row checkbox <input> — must have a
#                                    unique `value` (e.g. a row id)
# --------------------------------------------------------------------------
DATA_TABLE_JS = r"""
window.__dataTable = window.__dataTable || {
  registry: {},

  init(tableId, opts) {
    var root = document.getElementById(tableId);
    if (!root || root.__dtInitialized) return;
    root.__dtInitialized = true;

    var state = {
      page: 0,
      pageSize: (opts && opts.pageSize) || 5,
      sortKey: null,
      sortDir: 'asc',
      search: '',
      selected: new Set(),
      visibleRows: [],
    };

    var tbody = root.querySelector('tbody');
    if (!tbody) return;
    var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));

    // Strict check: the ENTIRE string must be a number, not just a numeric
    // prefix. parseFloat("2026-06-30") === 2026, which would make every
    // 2026 date tie under a naive !isNaN(parseFloat(...)) check.
    var isNumeric = function (v) {
      return /^-?\d+(\.\d+)?$/.test(v);
    };
    var compare = function (av, bv) {
      if (isNumeric(av) && isNumeric(bv)) return parseFloat(av) - parseFloat(bv);
      return String(av).localeCompare(String(bv));
    };

    var getSelectCb = function (row) { return row.querySelector('[data-dt-select]'); };
    var getSelectAllCb = function () { return root.querySelector('[data-dt-select-all]'); };

    var syncRowCheckboxes = function (pageRows) {
      pageRows.forEach(function (r) {
        var cb = getSelectCb(r);
        if (cb && cb.value) cb.checked = state.selected.has(cb.value);
      });
    };

    var updateSelectAllState = function () {
      var selectAll = getSelectAllCb();
      if (!selectAll) return;
      var selectableRows = state.visibleRows.filter(function (r) { return !!getSelectCb(r); });
      var selectedCount = selectableRows.filter(function (r) {
        var cb = getSelectCb(r);
        return cb && cb.value && state.selected.has(cb.value);
      }).length;
      if (selectableRows.length === 0 || selectedCount === 0) {
        selectAll.checked = false;
        selectAll.indeterminate = false;
      } else if (selectedCount === selectableRows.length) {
        selectAll.checked = true;
        selectAll.indeterminate = false;
      } else {
        selectAll.checked = false;
        selectAll.indeterminate = true;
      }
    };

    var dispatchSelectionChange = function () {
      root.dispatchEvent(
        new CustomEvent('dt-selection-change', { detail: { selected: Array.from(state.selected) } })
      );
    };

    var updateSortIcons = function () {
      root.querySelectorAll('[data-dt-sort]').forEach(function (btn) {
        var isActive = btn.getAttribute('data-dt-sort') === state.sortKey;
        var target = isActive ? state.sortDir : 'none';
        btn.querySelectorAll('[data-dt-sort-icon]').forEach(function (icon) {
          icon.style.display = icon.getAttribute('data-dt-sort-icon') === target ? '' : 'none';
        });
      });
    };

    var render = function () {
      // visibleRows = every row matching the current search, across ALL
      // pages — this is what "select all" operates on, not just the page.
      var visible = !state.search ? rows.slice() : rows.filter(function (r) {
        return r.innerText.toLowerCase().indexOf(state.search.toLowerCase()) !== -1;
      });
      state.visibleRows = visible;

      if (state.sortKey) {
        var headBtn = root.querySelector('[data-dt-sort="' + state.sortKey + '"]');
        var th = headBtn ? headBtn.closest('th') : null;
        var colIndex = th ? Array.prototype.indexOf.call(th.parentElement.children, th) : -1;
        if (colIndex > -1) {
          visible.sort(function (a, b) {
            var ac = a.children[colIndex], bc = b.children[colIndex];
            var av = (ac && (ac.getAttribute('data-sort-value') || ac.innerText)) || '';
            var bv = (bc && (bc.getAttribute('data-sort-value') || bc.innerText)) || '';
            var cmp = compare(av, bv);
            return state.sortDir === 'asc' ? cmp : -cmp;
          });
        }
      }

      // Pagination only kicks in if pagination controls actually exist
      // in the DOM (i.e. `paginate=True` was passed). Otherwise show all.
      var hasPagination = !!root.querySelector('[data-dt-prev]');
      var pageSize = hasPagination ? state.pageSize : (visible.length || 1);
      var totalPages = Math.max(1, Math.ceil(visible.length / pageSize));
      state.page = Math.min(state.page, totalPages - 1);
      var start = state.page * pageSize;
      var pageRows = visible.slice(start, start + pageSize);

      rows.forEach(function (r) { r.style.display = 'none'; });
      pageRows.forEach(function (r) {
        r.style.display = '';
        tbody.appendChild(r); // re-order into place
      });

      syncRowCheckboxes(pageRows);
      updateSelectAllState();

      var info = root.querySelector('[data-dt-info]');
      if (info) {
        info.textContent = visible.length === 0
          ? '0 results'
          : (start + 1) + '\u2013' + Math.min(start + pageSize, visible.length) + ' of ' + visible.length;
      }
      var pageLabel = root.querySelector('[data-dt-page-label]');
      if (pageLabel) pageLabel.textContent = 'Page ' + (state.page + 1) + ' of ' + totalPages;
      var prevBtn = root.querySelector('[data-dt-prev]');
      var nextBtn = root.querySelector('[data-dt-next]');
      if (prevBtn) prevBtn.disabled = state.page === 0;
      if (nextBtn) nextBtn.disabled = state.page >= totalPages - 1;

      updateSortIcons();
    };

    root.querySelectorAll('[data-dt-sort]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.getAttribute('data-dt-sort');
        if (state.sortKey === key) state.sortDir = state.sortDir === 'asc' ? 'desc' : 'asc';
        else { state.sortKey = key; state.sortDir = 'asc'; }
        render();
      });
    });

    var prevBtn = root.querySelector('[data-dt-prev]');
    var nextBtn = root.querySelector('[data-dt-next]');
    if (prevBtn) prevBtn.addEventListener('click', function () { state.page = Math.max(0, state.page - 1); render(); });
    if (nextBtn) nextBtn.addEventListener('click', function () { state.page += 1; render(); });

    // Delegated listener catches every row checkbox, including ones that
    // scroll into view only after pagination/sort re-renders.
    tbody.addEventListener('change', function (e) {
      var cb = e.target.closest('[data-dt-select]');
      if (!cb || !cb.value) return;
      if (cb.checked) state.selected.add(cb.value); else state.selected.delete(cb.value);
      dispatchSelectionChange();
      render();
    });

    var selectAllCb = getSelectAllCb();
    if (selectAllCb) {
      selectAllCb.addEventListener('change', function () {
        var checked = selectAllCb.checked;
        state.visibleRows.forEach(function (r) {
          var cb = getSelectCb(r);
          if (!cb || !cb.value) return;
          if (checked) state.selected.add(cb.value); else state.selected.delete(cb.value);
        });
        dispatchSelectionChange();
        render();
      });
    }

    // Exposed so any search input — the built-in toolbar one, or one
    // placed anywhere else via <TableSearch for_table="..."> — can drive
    // this table's search state without caring where it's mounted.
    this.registry[tableId] = {
      setSearch: function (value) {
        state.search = value;
        state.page = 0;
        render();
      },
    };

    render();
  },
};

// Single page-wide delegated listener (guarded so it only ever attaches
// once, even though this whole script block is itself de-duplicated).
// Delegation means a <TableSearch> can mount before OR after its table.
if (!window.__dtGlobalSearchListenerAttached) {
  window.__dtGlobalSearchListenerAttached = true;
  document.addEventListener('input', function (e) {
    var input = e.target.closest('[data-dt-search-for]');
    if (!input) return;
    var entry = window.__dataTable.registry[input.getAttribute('data-dt-search-for')];
    if (entry) entry.setSearch(input.value);
  });
}
"""


class TableRoot(Div, CoreComponent):
    @classmethod
    def create(
        cls,
        *children,
        searchable: bool = False,
        paginate: bool = False,
        page_size: int = 5,
        **props,
    ) -> Component:
        table_id = props.get("id") or f"data-table-{uuid.uuid4().hex[:8]}"
        props["id"] = table_id

        cls.set_class_name(ClassNames.ROOT, props)

        toolbar = (
            rx.el.div(
                TableSearch.create(for_table=table_id),
                class_name=ClassNames.TOOLBAR,
            )
            if searchable
            else None
        )

        pagination = (
            rx.el.div(
                rx.el.span("", **{"data-dt-info": "true"}),
                rx.el.div(
                    rx.el.button(
                        "Prev",
                        class_name=ClassNames.PAGE_BUTTON,
                        **{"data-dt-prev": "true"},
                    ),
                    rx.el.span("", class_name="px-2", **{"data-dt-page-label": "true"}),
                    rx.el.button(
                        "Next",
                        class_name=ClassNames.PAGE_BUTTON,
                        **{"data-dt-next": "true"},
                    ),
                    class_name="flex items-center gap-1",
                ),
                class_name=ClassNames.PAGINATION,
            )
            if paginate
            else None
        )

        table_props = {"class_name": ClassNames.TABLE}
        scroll_wrapper = rx.el.div(
            Table.create(*children, **table_props), class_name=ClassNames.SCROLL
        )

        props["on_mount"] = rx.call_script(
            f"window.__dataTable.init({table_id!r}, {{pageSize: {page_size}}})"
        )

        parts = [p for p in (toolbar, scroll_wrapper, pagination) if p is not None]
        return super().create(*parts, **props)

    def add_custom_code(self) -> list[str]:
        return [DATA_TABLE_JS]


class TableSearch(CoreComponent):
    @classmethod
    def create(
        cls, *, for_table: str, placeholder: str = "Search\u2026", **props
    ) -> Component:
        props.setdefault("placeholder", placeholder)
        props["data-dt-search-for"] = for_table
        cls.set_class_name(InputStyle.INPUT, props)
        return rx.el.input(**props)


class TableHeader(Thead, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Component:
        cls.set_class_name(ClassNames.HEADER, props)
        return super().create(*children, **props)


class TableBody(Tbody, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Component:
        cls.set_class_name(ClassNames.BODY, props)
        return super().create(*children, **props)


class TableFooter(Tfoot, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Component:
        cls.set_class_name(ClassNames.FOOTER, props)
        return super().create(*children, **props)


class TableRow(Tr, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Component:
        cls.set_class_name(ClassNames.ROW, props)
        return super().create(*children, **props)


class TableHead(Th, CoreComponent):
    @classmethod
    def create(cls, *children, sort_key: str | None = None, **props) -> Component:
        cls.set_class_name(ClassNames.HEAD, props)
        if sort_key:
            children = (
                rx.el.button(
                    *children,
                    *_sort_icons(),
                    class_name=ClassNames.HEAD_SORT_BTN,
                    **{"data-dt-sort": sort_key},
                ),
            )
        return super().create(*children, **props)


class TableCell(Td, CoreComponent):
    @classmethod
    def create(cls, *children, sort_value: Any = None, **props) -> Component:
        cls.set_class_name(ClassNames.CELL, props)
        if sort_value is not None:
            props["data-sort-value"] = str(sort_value)
        return super().create(*children, **props)


class TableCaption(Caption, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Component:
        cls.set_class_name(ClassNames.CAPTION, props)
        return super().create(*children, **props)


class TableNamespace(ComponentNamespace):
    root = staticmethod(TableRoot.create)
    search = staticmethod(TableSearch.create)
    header = staticmethod(TableHeader.create)
    body = staticmethod(TableBody.create)
    footer = staticmethod(TableFooter.create)
    row = staticmethod(TableRow.create)
    head = staticmethod(TableHead.create)
    cell = staticmethod(TableCell.create)
    caption = staticmethod(TableCaption.create)


table = TableNamespace()
```

# Examples

## Basic Table

```python
def table_block() -> rx.Component:
    subtotal = sum(item["qty"] * item["unit_price"] for item in LINE_ITEMS)
    tax = subtotal * TAX_RATE
    total = subtotal + tax

    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Acme Studio",
                            class_name="text-base font-semibold text-foreground",
                        ),
                        rx.el.span(
                            "hello@acmestudio.io",
                            class_name="text-xs text-muted-foreground whitespace-nowrap",
                        ),
                        class_name="flex flex-col gap-0.5",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "INV-2026-047",
                            class_name="font-mono text-xs font-medium text-foreground",
                        ),
                        rx.el.span(
                            "Issued Jun 17, 2026, due Jul 17, 2026",
                            class_name="text-xs text-muted-foreground whitespace-nowrap",
                        ),
                        class_name="flex flex-col items-end gap-0.5",
                    ),
                    class_name="flex items-start justify-between gap-4",
                ),
                class_name="flex flex-col gap-1 pb-5",
            ),
            # Container ensuring the table handles horizontal responsive overflows correctly
            rx.el.div(
                table.root(
                    table.caption(
                        "Billed to ",
                        rx.el.span(
                            "Northgate Holdings Ltd.",
                            class_name="font-medium text-foreground",
                        ),
                        " Net 30 payment terms apply.",
                        class_name="mt-0 px-3 py-2.5 text-left whitespace-nowrap",
                    ),
                    table.header(
                        table.row(
                            table.head(
                                "Description", class_name="pl-3 whitespace-nowrap"
                            ),
                            table.head(
                                "Category",
                                class_name="hidden sm:table-cell whitespace-nowrap",
                            ),
                            table.head(
                                "Qty", class_name="text-right whitespace-nowrap"
                            ),
                            table.head(
                                "Unit",
                                class_name="hidden text-right md:table-cell whitespace-nowrap",
                            ),
                            table.head(
                                "Unit Price", class_name="text-right whitespace-nowrap"
                            ),
                            table.head(
                                "Amount", class_name="pr-3 text-right whitespace-nowrap"
                            ),
                        )
                    ),
                    table.body(
                        *[
                            table.row(
                                table.cell(
                                    item["description"],
                                    class_name="pl-3 font-medium py-2 whitespace-nowrap",
                                ),
                                table.cell(
                                    item["category"],
                                    class_name="hidden text-muted-foreground sm:table-cell py-2 whitespace-nowrap",
                                ),
                                table.cell(
                                    str(item["qty"]),
                                    class_name="text-right text-muted-foreground tabular-nums py-2 whitespace-nowrap",
                                ),
                                table.cell(
                                    item["unit"],
                                    class_name="hidden text-right text-muted-foreground md:table-cell py-2 whitespace-nowrap",
                                ),
                                table.cell(
                                    fmt(item["unit_price"]),
                                    class_name="text-right text-muted-foreground tabular-nums py-2 whitespace-nowrap",
                                ),
                                table.cell(
                                    fmt(item["qty"] * item["unit_price"]),
                                    class_name="pr-3 text-right font-medium tabular-nums py-2 whitespace-nowrap",
                                ),
                            )
                            for item in LINE_ITEMS
                        ]
                    ),
                    table.footer(
                        table.row(
                            *summary_label("Subtotal", "text-muted-foreground"),
                            table.cell(
                                fmt(subtotal),
                                class_name="pr-3 text-right tabular-nums py-2 whitespace-nowrap",
                            ),
                            class_name="border-0",
                        ),
                        table.row(
                            *summary_label("Tax (8%)", "text-muted-foreground"),
                            table.cell(
                                fmt(tax),
                                class_name="pr-3 text-right tabular-nums py-2 whitespace-nowrap",
                            ),
                            class_name="border-0",
                        ),
                        table.row(
                            *summary_label(
                                "Total Due", "font-semibold text-foreground"
                            ),
                            table.cell(
                                fmt(total),
                                class_name="pr-3 text-right font-semibold text-foreground tabular-nums py-2 whitespace-nowrap",
                            ),
                        ),
                    ),
                ),
                class_name="mt-6 bg-card w-full overflow-x-auto",
            ),
            class_name="w-full max-w-2xl",
        ),
        class_name="flex w-full items-center justify-center bg-background px-6 py-12 text-foreground",
    )
```

## Table Invoice

```python
def table_demo_two() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Acme Inc.",
                        class_name="text-[10px] font-semibold tracking-widest text-muted-foreground uppercase",
                    ),
                    rx.el.h1(
                        "Invoices",
                        class_name="text-xl font-semibold tracking-tight text-foreground",
                    ),
                    rx.el.p(
                        "Recent billing activity across all client projects.",
                        class_name="text-sm text-muted-foreground",
                    ),
                    class_name="flex flex-col gap-1",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Outstanding",
                            class_name="text-[10px] tracking-widest text-muted-foreground uppercase",
                        ),
                        rx.el.span(
                            OUTSTANDING_FORMATTED,
                            class_name="text-lg font-semibold text-foreground tabular-nums",
                        ),
                        class_name="flex flex-col items-end gap-0.5",
                    ),
                    class_name="flex items-end gap-4",
                ),
                class_name="flex items-end justify-between gap-4",
            ),
            rx.el.hr(class_name="my-5"),
            table.search(for_table="invoices-table", class_name="w-56"),
            rx.el.hr(class_name="my-3 border-none"),
            table.root(
                table.header(
                    table.row(
                        table.head(
                            checkbox.root(
                                checkbox.indicator(),
                                **{"data-dt-select-all": "true"},
                            ),
                            class_name="w-10 pl-4",
                        ),
                        table.head("Invoice"),
                        table.head("Client", sort_key="client"),
                        table.head("Project", class_name="hidden sm:table-cell"),
                        table.head("Method", class_name="hidden md:table-cell"),
                        table.head(
                            "Due", sort_key="due", class_name="hidden md:table-cell"
                        ),
                        table.head("Status"),
                        table.head(
                            "Amount", sort_key="amount", class_name="text-right"
                        ),
                        table.head(
                            rx.el.span("Actions", class_name="sr-only"),
                            class_name="w-10 pr-4",
                        ),
                        class_name="whitespace-nowrap",
                    )
                ),
                table.body(*[render_row(inv) for inv in INVOICES]),
                id="invoices-table",
                paginate=True,
                page_size=7,
            ),
            rx.el.p(
                "Figures shown in USD. Last updated Jun 17, 2026.",
                class_name="mt-3 text-[11px] text-muted-foreground",
            ),
            class_name="w-full max-w-3xl",
        ),
        class_name="flex min-h-svh w-full items-start justify-center bg-background px-6 py-12 text-foreground",
    )
```

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
