from reflex.event import call_script
from reflex_components_core.el import div

from native.templates._dashboard_example import dashboard_example
from native.templates.sublayout import sub_layout_decorator


@sub_layout_decorator(
    badge_name="Dashboards",
    title="Dashboards for Data Apps",
    description="Build responsive dashboards for analytics, monitoring, and data-driven applications using composable UI components.",
    search=div(),
)
def dashboard_page():
    return div(
        dashboard_example(
            "dashboard_01",
            title="Dashboard 01",
            description="A KPI row, bar chart, and data table for a general-purpose analytics dashboard.",
        ),
        dashboard_example(
            "dashboard_02",
            title="Dashboard 02",
            description="Dashboard with search top bar, avatar, and dashboard placeholder cards.",
        ),
        dashboard_example(
            "dashboard_03",
            title="Dashboard 03",
            description="A complex dashboard with intricate sidebar, menu items, call-to-action card, analytics, and a menu top bar.",
        ),
        class_name="flex flex-col gap-16",
        on_mount=call_script(
            """
            requestAnimationFrame(() => {
                Prism.highlightAll();
            });
            """
        ),
    )
