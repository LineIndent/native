import reflex as rx

from components.core.hugeicon import hi
from components.ui.avatar import avatar
from components.ui.badge import badge
from components.ui.checkbox import checkbox
from components.ui.table import table
from native.lib.blocks.bar_chart_02 import bar_chart_02
from native.lib.blocks.kpi_card_01 import kpi_card_01

NAV_ITEMS = [
    {"label": "Overview", "icon": "DashboardSquare01Icon"},
    {"label": "Analytics", "icon": "ChartBarLineIcon"},
    {"label": "Projects", "icon": "FolderIcon"},
    {"label": "Team", "icon": "UserGroupIcon"},
    {"label": "Settings", "icon": "Settings01Icon"},
]

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

STATUS_CONFIG = {
    "Paid": {"variant": "default", "dot": "bg-primary-foreground"},
    "Pending": {"variant": "secondary", "dot": "bg-muted-foreground"},
    "Overdue": {"variant": "destructive", "dot": "bg-destructive"},
    "Refunded": {"variant": "outline", "dot": "bg-muted-foreground"},
}


def main_kpi_section():
    return kpi_card_01()


def main_chart_section():
    return rx.el.div(
        bar_chart_02(), class_name="w-full border border-input/90 rounded-2xl p-4"
    )


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


def main_table_section():

    return rx.el.div(
        table.search(
            for_table="invoices-table",
            class_name="mb-4 w-full max-w-sm",
        ),
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
                        "Due",
                        sort_key="due",
                        class_name="hidden md:table-cell",
                    ),
                    table.head("Status"),
                    table.head(
                        "Amount",
                        sort_key="amount",
                        class_name="text-right",
                    ),
                )
            ),
            table.body(*[render_row(inv) for inv in INVOICES]),
            id="invoices-table",
            paginate=True,
            page_size=7,
            class_name="w-full",
        ),
        class_name="w-full",
    )


def main():
    return rx.el.main(
        rx.el.h1("Overview", class_name="text-2xl font-semibold"),
        main_kpi_section(),
        main_chart_section(),
        main_table_section(),
        class_name="w-full flex-1 h-full border border-input/90 overflow-y-auto p-6 flex flex-col gap-6",
    )


def sidebar_header():
    return rx.el.div(
        rx.el.span("Acme", class_name="font-semibold text-lg"),
        class_name="flex items-center gap-2 px-4 h-10 shrink-0 border-b border-input/90",
    )


def _sidebar_item(label: str, icon: str) -> rx.Component:
    return rx.el.div(
        hi(icon, class_name="size-4 shrink-0"),
        rx.el.span(label, class_name="text-sm"),
        class_name="flex items-center gap-2.5 px-4 py-2 rounded-lg cursor-pointer",
    )


def sidebar_items():
    return rx.el.div(
        *[_sidebar_item(i["label"], i["icon"]) for i in NAV_ITEMS],
        class_name="flex flex-col gap-1 py-2",
    )


def sidebar_footer():
    return rx.el.div(
        rx.el.div(
            "AC",
            class_name="size-8 rounded-full bg-muted border border-input/90 flex items-center justify-center text-xs font-medium shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                "Avery Cole", class_name="text-sm font-medium leading-tight truncate"
            ),
            rx.el.p(
                "avery@acme.com",
                class_name="text-xs text-muted-foreground leading-tight truncate",
            ),
            class_name="min-w-0",
        ),
        class_name="flex items-center gap-2.5 px-4 py-3 border-t border-input/90 shrink-0",
    )


def sidebar():
    return rx.el.aside(
        sidebar_header(),
        sidebar_items(),
        rx.el.div(class_name="flex-1"),
        sidebar_footer(),
        class_name="w-full max-w-64 h-full bg-accent dark:bg-card border-y border-l border-input/90 hidden md:flex md:flex-col",
    )


def dashboard_01():
    return rx.el.div(
        sidebar(),
        main(),
        class_name="w-full h-screen flex",
    )
