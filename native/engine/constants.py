from dataclasses import dataclass
from pathlib import Path

import reflex as rx


@dataclass
class DocDataStruct:
    """The data structure for the generated doc page"""

    url: str
    description: str
    component: list[rx.Component]
    table_of_content: list[dict]


# --- Docs Path Constants ---
DOCS_BASE_DIR = Path("docs")
DOCS_LIBRARY_ROOT = "native/lib"
COMPONENTS_ROOT = "components"
