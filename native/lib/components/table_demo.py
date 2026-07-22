from typing import Any

import reflex as rx

from components.ui.table import table

LINE_ITEMS: list[dict[str, Any]] = [
    {
        "description": "Brand identity design",
        "category": "Design",
        "qty": 1,
        "unit": "project",
        "unit_price": 3200.0,
    },
    {
        "description": "UI component library",
        "category": "Development",
        "qty": 1,
        "unit": "project",
        "unit_price": 5800.0,
    },
    {
        "description": "Content strategy workshop",
        "category": "Consulting",
        "qty": 3,
        "unit": "session",
        "unit_price": 450.0,
    },
    {
        "description": "Copywriting: landing pages",
        "category": "Content",
        "qty": 5,
        "unit": "page",
        "unit_price": 280.0,
    },
    {
        "description": "QA & usability testing",
        "category": "Development",
        "qty": 8,
        "unit": "hour",
        "unit_price": 95.0,
    },
    {
        "description": "Project management",
        "category": "Consulting",
        "qty": 12,
        "unit": "hour",
        "unit_price": 75.0,
    },
]

TAX_RATE = 0.08


def fmt(val: float) -> str:
    return f"${val:,.2f}"


def summary_label(text: str, extra_classes: str = "") -> list:
    base_class = f"py-2 pl-3 whitespace-nowrap {extra_classes}"
    return [
        table.cell(text, col_span=3, class_name=f"{base_class} sm:hidden"),
        table.cell(
            text, col_span=4, class_name=f"hidden {base_class} sm:table-cell md:hidden"
        ),
        table.cell(text, col_span=5, class_name=f"hidden {base_class} md:table-cell"),
    ]


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
