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
