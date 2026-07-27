import reflex as rx

from components.core.hugeicon import hi
from components.ui.avatar import avatar
from components.ui.button import button
from native.lib.charts.area.v8 import area_chart_with_gradient

NAV_ITEMS = [
    {"label": "Dashboard", "icon": "DashboardSquare01Icon", "active": True},
    {"label": "Projects", "icon": "Folder01Icon", "active": False},
    {"label": "Analytics", "icon": "ChartBarLineIcon", "active": False},
    {"label": "Team", "icon": "UserGroupIcon", "active": False},
    {"label": "Reports", "icon": "GridViewIcon", "active": False},
]

ACTIVE_PROJECTS = [
    "Design System",
    "API Integration",
    "Mobile App",
    "Analytics Rebuild",
]

BREADCRUMB_ITEMS = [
    {"label": "Acme Inc", "icon": "SquareIcon"},
    {"label": "Marketing Site", "icon": None},
    {"label": "Preview", "icon": None},
]

STATS = [
    {"label": "Monthly Revenue", "value": "$48,240", "delta": "+12.5%"},
    {"label": "Active Users", "value": "8,941", "delta": "+4.3%"},
    {"label": "Conversion Rate", "value": "3.24%", "delta": "-0.8%"},
]

ACTIVITY = [
    {
        "name": "Priya Nair",
        "avatar": "https://i.pravatar.cc/150?img=45",
        "action": "deployed",
        "target": "web-app v2.4.0",
        "time": "9:42 AM",
    },
    {
        "name": "Jonas Weber",
        "avatar": "https://i.pravatar.cc/150?img=33",
        "action": "merged",
        "target": "PR 482 Checkout Refactor",
        "time": "9:06 AM",
    },
    {
        "name": "Lena Fischer",
        "avatar": "https://i.pravatar.cc/150?img=47",
        "action": "closed",
        "target": "8 tasks in Sprint 7",
        "time": "8:31 AM",
    },
    {
        "name": "Diego Alvarez",
        "avatar": "https://i.pravatar.cc/150?img=11",
        "action": "invited",
        "target": "Sofia Rossi to the team",
        "time": "Yesterday",
    },
]


def sidebar_header():
    return rx.el.div(
        rx.el.div(
            hi("DashboardSquare01Icon", class_name="size-5 shrink-0"),
            rx.el.span("Acme", class_name="font-semibold text-base"),
            class_name="flex items-center gap-2",
        ),
        rx.el.div(
            hi("SparklesIcon", class_name="size-3 shrink-0"),
            rx.el.span("Pro", class_name="text-xs font-medium"),
            class_name="flex items-center gap-1 bg-foreground text-background rounded-full px-2.5 py-1",
        ),
        class_name="flex items-center justify-between px-4 h-14 shrink-0",
    )


def new_report_button():
    return button(
        hi("PlusSignIcon", class_name="size-4"),
        rx.el.span("New Report", class_name="text-sm font-medium"),
        class_name="w-full",
    )


def _section_label(text: str) -> rx.Component:
    return rx.el.p(
        text,
        class_name="px-4 pt-4 pb-1 text-xs font-medium text-muted-foreground",
    )


def _sidebar_item(label: str, icon: str, active: bool = False) -> rx.Component:
    return rx.el.div(
        hi(icon, class_name="size-4 shrink-0"),
        rx.el.span(label, class_name="text-sm font-medium"),
        class_name=(
            "flex items-center gap-2.5 mx-2 px-3 py-2 rounded-lg cursor-pointer "
            + (
                "bg-accent text-accent-foreground"
                if active
                else "text-muted-foreground hover:bg-accent/60 hover:text-accent-foreground"
            )
        ),
    )


def sidebar_platform_items():
    return rx.el.div(
        _section_label("Platform"),
        *[_sidebar_item(i["label"], i["icon"], i["active"]) for i in NAV_ITEMS],
        class_name="flex flex-col",
    )


def _project_item(label: str) -> rx.Component:
    return rx.el.div(
        hi("Loading03Icon", class_name="size-4 shrink-0 text-muted-foreground"),
        rx.el.span(label, class_name="text-sm"),
        class_name="flex items-center gap-2.5 mx-2 px-3 py-2 rounded-lg text-muted-foreground hover:bg-accent/60 cursor-pointer",
    )


def sidebar_active_projects():
    return rx.el.div(
        _section_label("Active Projects"),
        *[_project_item(p) for p in ACTIVE_PROJECTS],
        class_name="flex flex-col",
    )


def sidebar_usage_card():
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                hi("SparklesIcon", class_name="size-3.5"),
                rx.el.span("Monthly Usage", class_name="text-sm font-medium"),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.span("Resets May 1", class_name="text-xs text-background/60"),
            class_name="flex items-center justify-between",
        ),
        rx.el.p(
            "You have used 82% of your plan this cycle. Upgrade for unlimited requests.",
            class_name="text-xs text-background/70 mt-2 leading-relaxed",
        ),
        rx.el.div(
            rx.el.div(class_name="h-1.5 rounded-full bg-background w-[82%]"),
            class_name="h-1.5 w-full rounded-full bg-background/20 mt-3",
        ),
        rx.el.div(
            rx.el.span("82% Used", class_name="text-xs font-medium"),
            rx.el.span("18% Left", class_name="text-xs text-background/60"),
            class_name="flex items-center justify-between mt-1.5",
        ),
        rx.el.button(
            hi("Notification03Icon", class_name="size-3.5"),
            rx.el.span("Upgrade Plan", class_name="text-sm font-medium"),
            class_name="flex items-center justify-center gap-2 h-9 w-full rounded-lg bg-background text-foreground mt-3",
        ),
        class_name="mx-3 mt-4 p-4 rounded-xl bg-foreground text-background",
    )


def sidebar_footer():
    return rx.el.div(
        avatar.root(
            avatar.image(
                src="https://i.pravatar.cc/150?img=47",
                class_name="shrink-0 grayscale",
            ),
            avatar.fallback("MC"),
            class_name="size-8",
        ),
        rx.el.div(
            rx.el.p(
                "Maya Chen", class_name="text-sm font-medium leading-tight truncate"
            ),
            rx.el.p(
                "maya@acme.com",
                class_name="text-xs text-muted-foreground leading-tight truncate",
            ),
            class_name="min-w-0 flex-1",
        ),
        hi("UnfoldMoreIcon", class_name="size-4 shrink-0 text-muted-foreground"),
        class_name="flex items-center gap-2.5 px-4 py-3 border-t border-input/90 shrink-0",
    )


def sidebar():
    return rx.el.aside(
        sidebar_header(),
        rx.el.div(new_report_button(), class_name="p-2 w-full"),
        rx.el.div(
            sidebar_platform_items(),
            sidebar_active_projects(),
            class_name="flex-1 overflow-y-auto py-3",
        ),
        sidebar_usage_card(),
        sidebar_footer(),
        class_name="w-full max-w-64 h-full bg-accent dark:bg-card border-y border-l border-input/90 hidden md:flex md:flex-col",
    )


def _breadcrumb_item(label: str, icon: str | None, is_last: bool) -> rx.Component:
    return rx.el.div(
        hi(icon, class_name="size-3.5 shrink-0") if icon else rx.el.div(),
        rx.el.span(
            label,
            class_name=(
                "text-sm " + ("font-semibold" if is_last else "text-muted-foreground")
            ),
        ),
        hi("ArrowDown01Icon", class_name="size-3.5 shrink-0 text-muted-foreground"),
        class_name="flex items-center gap-1.5",
    )


def breadcrumb():
    items = []
    for i, crumb in enumerate(BREADCRUMB_ITEMS):
        items.append(
            _breadcrumb_item(
                crumb["label"], crumb["icon"], i == len(BREADCRUMB_ITEMS) - 1
            )
        )
        if i < len(BREADCRUMB_ITEMS) - 1:
            items.append(rx.el.span("/", class_name="text-muted-foreground/50"))
    return rx.el.div(*items, class_name="flex items-center gap-2.5")


def topbar_search():
    return rx.el.div(
        hi("Search01Icon", class_name="size-4 shrink-0 text-muted-foreground"),
        rx.el.span("Search...", class_name="text-sm text-muted-foreground flex-1"),
        rx.el.kbd(
            "⌘K",
            class_name="text-[10px] font-medium text-muted-foreground bg-muted rounded px-1.5 py-0.5",
        ),
        class_name="hidden lg:flex items-center gap-2 h-9 w-64 rounded-lg border border-input/90 px-3 bg-background",
    )


def topbar_status_pill():
    return rx.el.div(
        rx.el.span(class_name="size-1.5 rounded-full bg-orange-500"),
        rx.el.span("Degraded", class_name="text-xs font-medium"),
        class_name="hidden sm:flex items-center gap-1.5 h-9 rounded-lg border border-input/90 px-3",
    )


def topbar():
    return rx.el.div(
        rx.el.div(
            hi(
                "SidebarLeftIcon",
                class_name="size-4 shrink-0 text-muted-foreground hidden md:block",
            ),
            class_name="flex items-center gap-4 min-w-0",
        ),
        rx.el.div(
            topbar_search(),
            topbar_status_pill(),
            rx.el.button(
                hi("Notification03Icon", class_name="size-4.5"),
                rx.el.span(
                    class_name="absolute top-1.5 right-1.5 size-1.5 rounded-full bg-foreground"
                ),
                class_name="relative size-9 flex items-center justify-center rounded-lg hover:bg-accent shrink-0",
            ),
            avatar.root(
                avatar.image(
                    src="https://i.pravatar.cc/150?img=47",
                    class_name="shrink-0 grayscale",
                ),
                avatar.fallback("MC"),
                class_name="size-8 shrink-0 cursor-pointer",
            ),
            class_name="flex items-center gap-3 shrink-0",
        ),
        class_name="flex items-center justify-between gap-4 h-14 shrink-0 px-4 sm:px-6 border-b border-input/90 bg-background",
    )


def _stat_card(label: str, value: str, delta: str) -> rx.Component:
    is_negative = delta.startswith("-")
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm text-muted-foreground"),
            rx.el.div(
                hi(
                    "ArrowDownRight01Icon" if is_negative else "ArrowUpRight01Icon",
                    class_name="size-3.5",
                ),
                rx.el.span(delta, class_name="text-sm font-medium"),
                class_name=(
                    "flex items-center gap-1 "
                    + ("text-muted-foreground" if is_negative else "text-emerald-600")
                ),
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.p(value, class_name="text-3xl font-bold tracking-tight mt-3"),
        rx.el.p("Vs. Last Month", class_name="text-xs text-muted-foreground mt-2"),
        class_name="flex-1 border border-input/90 rounded-2xl p-5",
    )


def main_stats_section():
    return rx.el.div(
        *[_stat_card(s["label"], s["value"], s["delta"]) for s in STATS],
        class_name="grid gap-4 sm:grid-cols-2 md:grid-cols-3",
    )


def main_chart_section():
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p("Revenue", class_name="font-semibold"),
                rx.el.p("Last 8 Months", class_name="text-sm text-muted-foreground"),
            ),
            rx.el.span(
                "+18.2% YTD",
                class_name="text-xs font-medium bg-muted rounded-lg px-2.5 py-1.5 h-fit",
            ),
            class_name="flex items-start justify-between mb-4",
        ),
        area_chart_with_gradient(),
        class_name="lg:col-span-2 border border-input/90 rounded-2xl p-5",
    )


def _activity_row(item: dict) -> rx.Component:
    return rx.el.div(
        avatar.root(
            avatar.image(src=item["avatar"], class_name="shrink-0 grayscale"),
            avatar.fallback(item["name"][:2].upper()),
            class_name="size-9",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(item["name"], class_name="font-semibold text-foreground"),
                " ",
                rx.el.span(item["action"], class_name="text-muted-foreground"),
                " ",
                rx.el.span(item["target"], class_name="font-semibold text-foreground"),
                class_name="text-sm leading-snug",
            ),
            rx.el.p(item["time"], class_name="text-xs text-muted-foreground mt-1"),
            class_name="min-w-0 flex-1",
        ),
        class_name="flex items-start gap-3 py-3 border-b border-input/60 last:border-0",
    )


def main_activity_section():
    return rx.el.div(
        rx.el.div(
            rx.el.p("Recent Activity", class_name="font-semibold"),
            rx.el.span(
                "View All",
                class_name="text-sm text-muted-foreground cursor-pointer hover:text-foreground",
            ),
            class_name="flex items-center justify-between mb-1",
        ),
        rx.el.div(
            *[_activity_row(item) for item in ACTIVITY],
            class_name="flex flex-col",
        ),
        class_name="border border-input/90 rounded-2xl p-5",
    )


def main_performance_section():
    return rx.el.div(
        main_chart_section(),
        main_activity_section(),
        class_name="grid gap-4 lg:grid-cols-3",
    )


def main_active_projects_header():
    return rx.el.div(
        rx.el.p("Active Projects", class_name="font-semibold"),
        rx.el.span(
            "View All",
            class_name="text-sm text-muted-foreground cursor-pointer hover:text-foreground",
        ),
        class_name="flex items-center justify-between p-5 border border-input/90 rounded-2xl",
    )


def main_header_row():
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Welcome Back, Maya", class_name="text-3xl font-bold tracking-tight"
            ),
            rx.el.p(
                "Here is what is happening across your workspace today.",
                class_name="text-sm text-muted-foreground mt-1",
            ),
        ),
        rx.el.button(
            hi("ArrowUpRight01Icon", class_name="size-4"),
            rx.el.span("Export Report", class_name="text-sm font-medium"),
            class_name="flex items-center gap-2 h-9 rounded-lg border border-input/90 px-3 shrink-0",
        ),
        class_name="flex flex-wrap items-end justify-between gap-3",
    )


def main():
    return rx.el.main(
        topbar(),
        rx.el.div(
            main_header_row(),
            main_stats_section(),
            main_performance_section(),
            main_active_projects_header(),
            class_name="flex flex-col gap-4 p-4 sm:p-6",
        ),
        class_name="w-full flex-1 h-full border border-input/90 overflow-y-auto flex flex-col",
    )


def dashboard_03():
    return rx.el.div(
        sidebar(),
        main(),
        class_name="w-full h-screen flex",
    )
