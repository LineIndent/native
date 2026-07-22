from reflex.components.component import Component
from reflex.utils.imports import ImportVar
from reflex.vars.base import Var, VarData

from ..core.core import CoreComponent

REACT_LIBRARY = "@hugeicons/react@1.1.9"
CORE_ICONS_LIBRARY = "@hugeicons/core-free-icons@4.2.3"


class HugeIcon(CoreComponent):
    library = REACT_LIBRARY

    tag = "HugeiconsIcon"

    icon: Var[str]

    alt_icon: Var[str | None]

    show_alt: Var[bool]

    size: Var[int | str] = Var.create(16)

    color: Var[str]

    primary_color: Var[str]

    secondary_color: Var[str]

    stroke_width: Var[float] = Var.create(1.5)

    absolute_stroke_width: Var[bool]

    disable_secondary_opacity: Var[bool]

    @classmethod
    def create(cls, *children, **props) -> Component:

        if children and isinstance(children[0], str) and "icon" not in props:
            props["icon"] = children[0]
            children = children[1:]

        for prop in ("icon", "alt_icon"):
            value = props.get(prop)

            if isinstance(value, str):
                props[prop] = Var(
                    value,
                    _var_data=VarData(
                        imports={CORE_ICONS_LIBRARY: [ImportVar(tag=value)]}
                    ),
                )

        stroke_width = props.get("stroke_width", 1.5)

        cls.set_class_name(
            f"[&_path]:stroke-[{stroke_width}]",
            props,
        )

        return super().create(*children, **props)


hi = icon = HugeIcon.create
