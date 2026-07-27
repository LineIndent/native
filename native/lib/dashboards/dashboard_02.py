import reflex as rx

from components.core.hugeicon import hi
from components.ui.avatar import avatar
from components.ui.badge import badge
from native.lib.charts.area.v8 import area_chart_with_gradient

NAV_ITEMS = [
    {"label": "Overview", "icon": "DashboardSquare01Icon", "active": True},
    {"label": "Analytics", "icon": "ChartBarLineIcon", "active": False},
    {"label": "Projects", "icon": "FolderIcon", "active": False},
    {"label": "Team", "icon": "UserGroupIcon", "active": False},
    {"label": "Settings", "icon": "Settings01Icon", "active": False},
]

STATS = [
    {"label": "Total revenue", "value": "$48.2k", "delta": "+12.4%"},
    {"label": "Active users", "value": "2,840", "delta": "+5.1%"},
    {"label": "Conversion", "value": "3.6%", "delta": "-0.8%"},
]

ACTIVITY = [
    {
        "name": "Priya Nair",
        "avatar": "https://i.pravatar.cc/150?img=45",
        "icon": "RocketIcon",
        "action": "deployed",
        "target": "acme-web v2.4",
        "time": "2 min ago",
    },
    {
        "name": "Marco Diaz",
        "avatar": "https://i.pravatar.cc/150?img=33",
        "icon": "GitMergeIcon",
        "action": "merged",
        "target": "PR #482: checkout refactor",
        "time": "1 hour ago",
    },
    {
        "name": "Lena Fischer",
        "avatar": "https://i.pravatar.cc/150?img=47",
        "icon": "CheckmarkCircle01Icon",
        "action": "closed",
        "target": "8 tasks in Sprint 7",
        "time": "3 hours ago",
    },
]


def sidebar_header():
    return rx.el.div(
        hi("DashboardSquare01Icon", class_name="size-5 shrink-0"),
        rx.el.span("Acme", class_name="font-semibold text-base"),
        class_name="flex items-center gap-2 px-4 h-14 shrink-0 border-b border-input/90",
    )


def _sidebar_item(label: str, icon: str, active: bool = False) -> rx.Component:
    return rx.el.div(
        hi(icon, class_name="size-4 shrink-0"),
        rx.el.span(label, class_name="text-sm"),
        class_name=(
            "flex items-center gap-2.5 px-3 py-2 rounded-lg cursor-pointer "
            + (
                "bg-accent text-accent-foreground"
                if active
                else "text-muted-foreground hover:bg-accent/60 hover:text-accent-foreground"
            )
        ),
    )


def sidebar_items():
    return rx.el.div(
        *[_sidebar_item(i["label"], i["icon"], i["active"]) for i in NAV_ITEMS],
        class_name="flex flex-col gap-1 p-2",
    )


def sidebar_footer():
    return rx.el.div(
        avatar.root(
            avatar.image(
                src="https://i.pravatar.cc/150?img=15",
                class_name="shrink-0 border border-input/90 grayscale",
            ),
            avatar.fallback("AC"),
            class_name="size-8",
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


def navbar():
    return rx.el.div(
        rx.el.div(
            hi("Search01Icon", class_name="size-4 shrink-0 text-muted-foreground"),
            rx.el.span(
                "Search projects, people...",
                class_name="text-sm text-muted-foreground",
            ),
            class_name=(
                "flex items-center gap-2 h-9 w-full max-w-sm border border-input/90 "
                "rounded-lg px-3 bg-background cursor-pointer"
            ),
        ),
        rx.el.div(
            rx.el.button(
                hi("Notification03Icon", class_name="size-5"),
                rx.el.span(
                    "2",
                    class_name=(
                        "absolute -top-1 -right-1 flex size-4 items-center justify-center "
                        "rounded-full bg-primary text-[9px] font-bold text-primary-foreground"
                    ),
                ),
                class_name="relative size-9 flex items-center justify-center rounded-lg hover:bg-accent",
            ),
            avatar.root(
                avatar.image(
                    src="https://i.pravatar.cc/150?img=15",
                    class_name="shrink-0 border border-input/90 grayscale",
                ),
                avatar.fallback("AC"),
                class_name="size-8 cursor-pointer",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name=(
            "flex items-center justify-between gap-3 h-14 shrink-0 px-4 sm:px-6 "
            "border-b border-input/90 bg-background"
        ),
    )


def _stat_card(label: str, value: str, delta: str) -> rx.Component:
    is_negative = delta.startswith("-")
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-muted-foreground"),
            badge(
                delta,
                variant="destructive" if is_negative else "secondary",
                class_name="text-[11px]",
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.p(value, class_name="text-3xl font-semibold tracking-tight mt-3"),
        class_name="flex-1 border border-input/90 rounded-2xl p-4",
    )


def main_stats_section():
    return rx.el.div(
        *[_stat_card(s["label"], s["value"], s["delta"]) for s in STATS],
        class_name="grid gap-4 sm:grid-cols-2 md:grid-cols-3",
    )


def main_chart_section():
    return rx.el.div(
        rx.el.div(
            rx.el.p("Performance", class_name="font-medium"),
            badge("+18.2% MoM", variant="secondary", class_name="text-[11px]"),
            class_name="flex items-center justify-between mb-2",
        ),
        area_chart_with_gradient(),
        class_name="md:col-span-2 border border-input/90 rounded-2xl p-4",
    )


def _activity_row(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            avatar.root(
                avatar.image(src=item["avatar"], class_name="shrink-0 grayscale"),
                avatar.fallback(item["name"][:2].upper()),
                class_name="size-8",
            ),
            rx.el.div(
                hi(item["icon"], class_name="size-2.5 text-muted-foreground"),
                class_name=(
                    "absolute -right-1 -bottom-1 flex size-4 items-center justify-center "
                    "rounded-full border border-input/90 bg-background"
                ),
            ),
            class_name="relative shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(item["name"], class_name="font-medium text-foreground"),
                " ",
                rx.el.span(item["action"], class_name="text-muted-foreground"),
                " ",
                rx.el.span(item["target"], class_name="font-medium text-foreground"),
                class_name="text-sm leading-snug",
            ),
            rx.el.p(item["time"], class_name="text-xs text-muted-foreground mt-0.5"),
            class_name="min-w-0 flex-1",
        ),
        class_name="flex items-start gap-3",
    )


def main_activity_section():
    return rx.el.div(
        rx.el.p("Recent Activity", class_name="font-medium mb-4"),
        rx.el.div(
            *[_activity_row(item) for item in ACTIVITY],
            class_name="flex flex-col gap-4",
        ),
        class_name="border border-input/90 rounded-2xl p-4",
    )


def main_performance_section():
    return rx.el.div(
        main_chart_section(),
        main_activity_section(),
        class_name="grid gap-4 md:grid-cols-3",
    )


def main():
    return rx.el.main(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Overview", class_name="text-2xl font-semibold tracking-tight"
                    ),
                    rx.el.p(
                        "Here is what is happening across Acme today.",
                        class_name="text-sm text-muted-foreground",
                    ),
                ),
                badge(
                    rx.el.span(class_name="size-1.5 rounded-full bg-primary"),
                    "Live",
                    variant="secondary",
                    class_name="gap-1.5",
                ),
                class_name="flex flex-wrap items-end justify-between gap-3",
            ),
            main_stats_section(),
            main_performance_section(),
            class_name="flex flex-col gap-4 p-4 sm:p-6",
        ),
        class_name="w-full flex-1 h-full border border-input/90 overflow-y-auto flex flex-col",
    )


def dashboard_02():
    return rx.el.div(
        sidebar(),
        main(),
        class_name="w-full h-screen flex",
    )
