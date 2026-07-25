import importlib
from pathlib import Path

import reflex as rx
from reflex.experimental import ClientStateVar
from reflex_components_core.el import div, h3, p

from components.core.hugeicon import hi
from components.ui.button import button
from native.templates._demo import demo
from native.templates.sublayout import sub_layout_decorator

BLOCKS_PATH = Path("native/lib/blocks")

BLOCKS_MODULE = ".".join(BLOCKS_PATH.parts)


active_block_filter = ClientStateVar.create("active_block_filter", "all")


def block_files(prefix: str) -> list[Path]:
    return sorted(BLOCKS_PATH.glob(f"{prefix}_*.py"))


def load_blocks(prefix: str) -> list[tuple[str, object, str]]:
    blocks = []
    for file in block_files(prefix):
        module = importlib.import_module(f"{BLOCKS_MODULE}.{file.stem}")
        component_fn = getattr(module, file.stem)
        source = file.read_text()
        blocks.append((file.stem, component_fn, source))
    return blocks


def section(prefix: str, title: str, description: str, blocks):
    is_visible = (active_block_filter.value == "all") | (
        active_block_filter.value == prefix
    )

    return div(
        div(
            h3(title, class_name="text-lg font-bold tracking-tight"),
            p(
                description,
                class_name="text-sm text-muted-foreground",
            ),
            class_name="flex flex-col gap-1",
        ),
        div(
            *blocks,
            class_name="flex flex-col gap-10",
        ),
        class_name=rx.cond(is_visible, "flex flex-col gap-4", "hidden"),
        custom_attrs={"data-section": "true", "data-block-type": prefix},
    )


BLOCK_GROUPS = [
    (
        "area_chart",
        "Area Charts",
        "Filled line charts for showing trends over time.",
    ),
    (
        "bar_chart",
        "Bar Charts",
        "Categorical comparisons across groups.",
    ),
    (
        "kpi_card",
        "KPI Cards",
        "Compact metric summaries for dashboards.",
    ),
]


def build_section(prefix: str, title: str, description: str):
    blocks = [
        div(demo(component=component_fn(), source=source))
        for name, component_fn, source in load_blocks(prefix)
    ]

    return section(prefix, title, description, blocks)


def filter_button(label: str, value: str):
    is_active = active_block_filter.value == value
    return button(
        label,
        variant="outline",
        size="sm",
        class_name=rx.cond(is_active, "!bg-muted", ""),
        on_click=active_block_filter.set_value(value),
    )


def filter_blocks():
    return div(
        div(
            hi("FilterMailIcon", class_name="size-4 shrink-0"),
            h3("Filter Blocks", class_name="text-lg font-bold"),
            class_name="flex flex-row gap-2 items-center",
        ),
        div(
            filter_button("All", "all"),
            *[
                filter_button(title, prefix)
                for prefix, title, _description in BLOCK_GROUPS
            ],
            class_name="flex flex-row flex-wrap gap-2 mt-3",
        ),
        class_name="flex flex-col w-full",
    )


@sub_layout_decorator(
    badge_name="Blocks",
    title="Building Blocks for Dashboards",
    description="Clean, modern building blocks for Reflex dashboards. Copy and paste into your apps. Open Source. Extensible.",
    search=div(),
)
def blocks_page():
    return div(
        filter_blocks(),
        *[
            build_section(prefix, title, description)
            for prefix, title, description in BLOCK_GROUPS
        ],
        class_name="flex flex-col gap-8",
    )
