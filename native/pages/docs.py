from pathlib import Path

from reflex.event import call_script
from reflex_base.vars.base import Var
from reflex_components_core.el import a, div, h3, h4, p, span

from components.core.hugeicon import hi
from components.ui.button import button
from components.ui.input_group import input_group
from native.templates.sublayout import sub_layout_decorator

DOCS_GETTING_STARTED_PATH = Path("docs/getting_started")
DOCS_RESOURCES_PATH = Path("docs/resources")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parses frontmatter metadata (like order and description) from Markdown content."""
    metadata = {}
    if not content.startswith("---"):
        return metadata, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return metadata, content

    frontmatter = parts[1]
    rest_of_content = parts[2]

    for line in frontmatter.strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]

            if key == "order" and value.isdigit():
                value = int(value)

            metadata[key] = value

    return metadata, rest_of_content.lstrip()


def link_card(name: str, href: str, description: str = ""):
    return a(
        div(
            # Title Stack
            div(
                h4(
                    name,
                    class_name="truncate text-sm font-semibold tracking-tight text-foreground group-hover:text-primary transition-colors",
                ),
                class_name="flex min-w-0 items-center gap-1.5",
            ),
            # Description Block (only renders if description exists)
            div(
                p(
                    description,
                    class_name="text-xs text-muted-foreground line-clamp-2 leading-relaxed",
                ),
                class_name="mt-1",
            ) if description else div(),
            class_name="flex flex-col gap-1",
        ),
        href=href,
        custom_attrs={"data-name": name.lower()},
        class_name="group flex flex-col gap-3 border border-border bg-background p-4 hover:bg-muted/30 focus-visible:border-ring focus-visible:ring-1 focus-visible:ring-ring/50 focus-visible:outline-none transition-all rounded-md",
    )


def get_links(source_dir: Path, url_prefix: str):
    entries = []

    for file in source_dir.glob("*.md"):
        stem = file.stem
        name = stem.replace("_", " ").replace("-", " ").title()
        slug = stem.replace("_", "-")

        # Read file content and extract frontmatter
        try:
            content = file.read_text(encoding="utf-8")
            metadata, _ = parse_frontmatter(content)
        except Exception:
            metadata = {}

        # Extract order (default to 999 if missing so unordered pages go to the end)
        order = metadata.get("order", 999)

        # Pull custom title from frontmatter if available, otherwise fallback to filename title
        display_name = metadata.get("title", name)

        # Grab description
        description = metadata.get("description", "")

        entries.append((order, display_name, slug, description))

    # Sort primarily by the 'order' integer, secondarily by name alphabetically
    entries.sort(key=lambda x: (x[0], x[1].lower()))

    return [
        link_card(name, f"{url_prefix}/{slug}", description)
        for _, name, slug, description in entries
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
            class_name="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3",
        ),
        class_name="flex flex-col gap-4",
        custom_attrs={"data-section": "true"},
    )


def no_results():
    return div(
        div(
            div("No documentation pages found", class_name="font-sans text-sm font-medium"),
            class_name="flex max-w-sm flex-col items-center gap-2",
        ),
        div(
            div(
                span("Nothing matches "),
                span(id="no-results-term", class_name="font-medium text-foreground"),
                span(". Try a different term."),
                class_name="text-xs/relaxed text-muted-foreground flex flex-wrap items-center justify-center gap-1",
            ),
        ),
        div(
            button(
                "Clear search",
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


getting_started_links = get_links(
    DOCS_GETTING_STARTED_PATH,
    "/docs/getting-started",
)

resources_links = get_links(
    DOCS_RESOURCES_PATH,
    "/docs/resources",
)


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
    badge_name="Docs",
    title="Documentation Overview",
    description="Explore our comprehensive guides, core concepts, and developer resources to help you build and scale your applications.",
    search=input_group.root(
        input_group.input(
            placeholder="Search documentation...",
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
def docs_page():
    return div(
        section(
            "Getting Started",
            "Essential guides, installation steps, and core concepts to get you up and running.",
            getting_started_links,
        ),
        section(
            "Resources",
            "Reference materials, configuration guides, and additional tools for your development workflow.",
            resources_links,
        ),
        no_results(),
        id="search-container",
        class_name="flex flex-col gap-8",
    )
