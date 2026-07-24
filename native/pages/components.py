from pathlib import Path

from reflex.event import call_script
from reflex_base.vars.base import Var
from reflex_components_core.el import a, div, h3, h4, p, span

from components.core.hugeicon import hi
from components.ui.button import button
from components.ui.input_group import input_group
from native.templates.sublayout import sub_layout_decorator

COMPONENTS_PATH = Path("components/ui")
COMPONENT_EXAMPLES = Path("native/lib/components")


DOCS_CHARTS_PATH = Path("docs/charts")
CHART_EXAMPLES = Path("native/lib/charts")

UTILITY_EXAMPLES = Path("native/lib/utilities")

UTILITIES = [
    ("Shimmer", "shimmer"),
    ("Scroll Fade", "scroll_fade"),
    ("Markdown", "markdown"),
]


def link_card(name: str, href: str, count: int):
    return a(
        div(
            div(
                h4(
                    name,
                    class_name="truncate text-sm font-semibold tracking-tight",
                ),
                class_name="flex min-w-0 items-center gap-1.5",
            ),
            span(
                f"{count} example{'s' if count != 1 else ''}",
                class_name="shrink-0 text-xs text-muted-foreground",
            ),
            class_name="flex items-center justify-between gap-2",
        ),
        href=href,
        custom_attrs={"data-name": name.lower()},
        class_name="group flex flex-col gap-3 border border-border bg-background p-4 hover:bg-muted/30 focus-visible:border-ring focus-visible:ring-1 focus-visible:ring-ring/50 focus-visible:outline-none rounded-lg",
    )


def get_links(source_dir: Path, examples_dir: Path, url_prefix: str):
    entries = []

    for file in source_dir.glob("*.py"):
        stem = file.stem
        name = stem.replace("_", " ").title()
        slug = stem.replace("_", "-")

        example_count = len(list(examples_dir.glob(f"{stem}_*.py")))

        entries.append((name, slug, example_count))

    entries.sort(key=lambda x: x[0].lower())

    return [
        link_card(name, f"{url_prefix}/{slug}", count) for name, slug, count in entries
    ]


def get_utility_links():
    return [
        link_card(
            name,
            f"/docs/utilities/{slug.replace('_', '-')}",
            len(list(UTILITY_EXAMPLES.glob(f"{slug}_*.py"))),
        )
        for name, slug in UTILITIES
    ]


def get_chart_links():
    entries = []

    if CHART_EXAMPLES.exists():
        for chart_dir in CHART_EXAMPLES.iterdir():
            if chart_dir.is_dir():
                stem = chart_dir.name  # e.g., "area"

                # Append "-chart" explicitly to the slug, but keep the display name clean
                name = f"{stem.replace('_', ' ').title()} Chart"  # e.g., "Area Chart"
                slug = f"{stem.replace('_', '-')}-chart"  # e.g., "area-chart"

                # Count files inside the subfolder (native/lib/charts/area/*.py)
                example_count = len(list(chart_dir.glob("*.py")))

                entries.append((name, slug, example_count))

    entries.sort(key=lambda x: x[0].lower())

    return [
        link_card(name, f"/docs/charts/{slug}", count) for name, slug, count in entries
    ]


def section(title: str, description: str, links):
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
            *links,
            class_name="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4",
        ),
        class_name="flex flex-col gap-4",
        custom_attrs={"data-section": "true"},
    )


def no_results():
    return div(
        div(
            div("No components found", class_name="font-sans text-sm font-medium"),
            class_name="flex max-w-sm flex-col items-center gap-2",
        ),
        div(
            div(
                span("Nothing matches "),
                span(id="no-results-term", class_name="font-medium text-foreground"),
                span(". Try a different term."),
                class_name="text-xs/relaxed text-muted-foreground [&>a]:underline [&>a]:underline-offset-4 [&>a:hover]:text-primary flex flex-wrap items-center justify-center gap-1",
            ),
            class_name="text-xs/relaxed text-muted-foreground [&>a]:underline [&>a]:underline-offset-4 [&>a:hover]:text-primary flex flex-wrap items-center justify-center gap-1",
        ),
        div(
            button(
                "Show all components",
                variant="outline",
                on_click=call_script(
                    """
                    (function() {
                      const input = document.querySelector('[data-slot="input-group-control"]');
                      if (input) {
                        const nativeSetter = Object.getOwnPropertyDescriptor(
                          window.HTMLInputElement.prototype, 'value'
                        ).set;
                        nativeSetter.call(input, '');
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                      }

                      const container = document.getElementById('search-container');
                      if (!container) return;

                      container.querySelectorAll('[data-name]').forEach((card) => {
                        card.classList.remove('!hidden');
                      });

                      container.querySelectorAll('[data-section]').forEach((sectionEl) => {
                        sectionEl.classList.remove('!hidden');
                      });

                      const noResults = document.getElementById('no-results');
                      if (noResults) noResults.classList.add('!hidden');

                      const termEl = document.getElementById('no-results-term');
                      if (termEl) termEl.textContent = '';
                    })()
                    """
                ),
            ),
            class_name="flex w-full max-w-sm min-w-0 flex-col items-center gap-2.5 text-xs text-balance",
        ),
        id="no-results",
        class_name="!hidden flex w-full min-w-0 flex-1 flex-col items-center justify-center gap-4 rounded-none p-6 text-center text-balance border border-dashed border-border py-40",
    )


component_links = get_links(
    COMPONENTS_PATH,
    COMPONENT_EXAMPLES,
    "/docs/components",
)

utility_links = get_utility_links()
chart_links = get_chart_links()


def filter_script(value: Var) -> Var:
    return Var(
        f"""
(function(term) {{
  term = (term || "").toLowerCase();
  const container = document.getElementById('search-container');
  if (!container) return;

  let anyMatch = false;

  container.querySelectorAll('[data-section]').forEach((sectionEl) => {{
    let sectionMatch = false;

    sectionEl.querySelectorAll('[data-name]').forEach((card) => {{
      const matches = term === '' || card.dataset.name.includes(term);
      card.classList.toggle('!hidden', !matches);
      if (matches) sectionMatch = true;
    }});

    sectionEl.classList.toggle('!hidden', !sectionMatch);
    if (sectionMatch) anyMatch = true;
  }});

  const noResults = document.getElementById('no-results');
  if (noResults) noResults.classList.toggle('!hidden', anyMatch);

  const termEl = document.getElementById('no-results-term');
  if (termEl) termEl.textContent = '"' + term + '"';
}})({value})
"""
    )


@sub_layout_decorator(
    badge_name="Components",
    title="Components for Every App",
    description="A collection of ready-to-use UI components for building modern applications. From simple controls to complex interface patterns, copy and paste into your apps.",
    search=input_group.root(
        input_group.input(
            placeholder="Search categories...",
            on_change=lambda value: call_script(filter_script(value)),
        ),
        input_group.addon(
            hi(
                "SearchIcon",
                class_name="text-muted-foreground size-4",
            ),
            align="inline-start",
        ),
    ),
)
def components_page():
    return div(
        section(
            "UI Components",
            "Building blocks for your web apps.",
            component_links,
        ),
        section(
            "Charts",
            "A collection of ready-to-use chart components built with Recharts.",
            chart_links,
        ),
        section(
            "Utilities",
            "Pure CSS utilities to add to your web apps.",
            utility_links,
        ),
        no_results(),
        id="search-container",
        class_name="flex flex-col gap-8",
    )
