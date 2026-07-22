import reflex as rx

from components.ui.avatar import avatar
from components.ui.badge import badge
from components.ui.checkbox import checkbox
from components.ui.table import table

INVOICES = [
    {
        "id": "INV-0041",
        "client": "Miriam Okafor",
        "initials": "MO",
        "avatar": "https://i.pravatar.cc/80?img=1",
        "project": "Brand Refresh",
        "amount": 4200.00,
        "method": "Wire Transfer",
        "due": "Jun 30, 2026",
        "due_date": "2026-06-30",
        "status": "Pending",
    },
    {
        "id": "INV-0040",
        "client": "Theo Hartmann",
        "initials": "TH",
        "avatar": "https://i.pravatar.cc/80?img=12",
        "project": "API Integration",
        "amount": 1850.00,
        "method": "Credit Card",
        "due": "Jun 15, 2026",
        "due_date": "2026-06-15",
        "status": "Paid",
    },
    {
        "id": "INV-0039",
        "client": "Suki Nakamura",
        "initials": "SN",
        "avatar": "https://i.pravatar.cc/80?img=5",
        "project": "Dashboard UI",
        "amount": 6500.00,
        "method": "ACH",
        "due": "Jun 01, 2026",
        "due_date": "2026-06-01",
        "status": "Overdue",
    },
    {
        "id": "INV-0038",
        "client": "Elias Ferreira",
        "initials": "EF",
        "avatar": "https://i.pravatar.cc/80?img=3",
        "project": "Mobile App MVP",
        "amount": 9000.00,
        "method": "Wire Transfer",
        "due": "May 28, 2026",
        "due_date": "2026-05-28",
        "status": "Paid",
    },
    {
        "id": "INV-0037",
        "client": "Priya Menon",
        "initials": "PM",
        "avatar": "https://i.pravatar.cc/80?img=9",
        "project": "SEO Audit",
        "amount": 780.00,
        "method": "Credit Card",
        "due": "May 10, 2026",
        "due_date": "2026-05-10",
        "status": "Refunded",
    },
    {
        "id": "INV-0036",
        "client": "Dmitri Volkov",
        "initials": "DV",
        "avatar": "https://i.pravatar.cc/80?img=11",
        "project": "Data Pipeline",
        "amount": 3350.00,
        "method": "ACH",
        "due": "Apr 25, 2026",
        "due_date": "2026-04-25",
        "status": "Paid",
    },
    {
        "id": "INV-0035",
        "client": "Amara Diallo",
        "initials": "AD",
        "avatar": "https://i.pravatar.cc/80?img=16",
        "project": "Design System",
        "amount": 5400.00,
        "method": "Wire Transfer",
        "due": "Jun 22, 2026",
        "due_date": "2026-06-22",
        "status": "Pending",
    },
    {
        "id": "INV-0034",
        "client": "Noah Bergström",
        "initials": "NB",
        "avatar": "https://i.pravatar.cc/80?img=14",
        "project": "Marketing Site",
        "amount": 2100.00,
        "method": "Credit Card",
        "due": "Apr 18, 2026",
        "due_date": "2026-04-18",
        "status": "Paid",
    },
    {
        "id": "INV-0033",
        "client": "Lucia Romano",
        "initials": "LR",
        "avatar": "https://i.pravatar.cc/80?img=20",
        "project": "Onboarding Flow",
        "amount": 3950.00,
        "method": "ACH",
        "due": "May 31, 2026",
        "due_date": "2026-05-31",
        "status": "Overdue",
    },
    {
        "id": "INV-0032",
        "client": "Kwame Mensah",
        "initials": "KM",
        "avatar": "https://i.pravatar.cc/80?img=15",
        "project": "Analytics Setup",
        "amount": 1280.00,
        "method": "Credit Card",
        "due": "Apr 09, 2026",
        "due_date": "2026-04-09",
        "status": "Paid",
    },
]

OUTSTANDING_TOTAL = sum(
    inv["amount"] for inv in INVOICES if inv["status"] in ["Pending", "Overdue"]
)
OUTSTANDING_FORMATTED = f"${OUTSTANDING_TOTAL:,.2f}"

STATUS_CONFIG = {
    "Paid": {"variant": "default", "dot": "bg-primary-foreground"},
    "Pending": {"variant": "secondary", "dot": "bg-muted-foreground"},
    "Overdue": {"variant": "destructive", "dot": "bg-destructive"},
    "Refunded": {"variant": "outline", "dot": "bg-muted-foreground"},
}


def render_status_badge(status: str) -> rx.Component:
    config = STATUS_CONFIG.get(
        status, {"variant": "default", "dot": "bg-muted-foreground"}
    )

    return badge(
        rx.el.span(
            class_name=f"inline-block size-1.5 shrink-0 rounded-lg {config['dot']}"
        ),
        status,
        variant=config["variant"],
        class_name="gap-1.5 text-[11px] font-medium",
    )


def render_row(inv: dict) -> rx.Component:
    formatted_amount = f"{inv['amount']:,.2f}"

    return table.row(
        table.cell(
            checkbox.root(
                checkbox.indicator(),
                value=inv["id"],
                **{"data-dt-select": "true"},
            ),
            class_name="pl-4 py-2",
        ),
        table.cell(
            rx.el.span(
                inv["id"],
                class_name="font-mono text-xs text-muted-foreground py-2",
            )
        ),
        table.cell(
            rx.el.div(
                avatar.root(
                    avatar.image(
                        src=inv["avatar"],
                        class_name="shrink-0 border border-border grayscale",
                    ),
                ),
                rx.el.span(
                    inv["client"],
                    class_name="truncate text-sm font-medium text-foreground",
                ),
                class_name="flex min-w-0 items-center gap-2.5",
            ),
            sort_value=inv["client"],
            class_name="py-2",
        ),
        table.cell(
            rx.el.span(
                inv["project"],
                class_name="block max-w-[140px] truncate text-sm text-muted-foreground",
            ),
            class_name="hidden sm:table-cell py-2",
        ),
        table.cell(
            rx.el.span(inv["method"], class_name="text-sm text-muted-foreground"),
            class_name="hidden md:table-cell py-2",
        ),
        table.cell(
            rx.el.span(
                inv["due"],
                class_name="text-sm text-muted-foreground tabular-nums",
            ),
            sort_value=inv["due_date"],
            class_name="hidden md:table-cell py-2",
        ),
        table.cell(render_status_badge(inv["status"])),
        table.cell(
            rx.el.span(
                f"${formatted_amount}",
                class_name="block text-right text-sm font-semibold text-foreground tabular-nums",
            ),
            sort_value=inv["amount"],
            class_name="py-2",
        ),
        class_name="whitespace-nowrap !py-2",
    )


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
