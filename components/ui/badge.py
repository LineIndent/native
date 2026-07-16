from reflex.vars.base import Var
from reflex_components_core.el import Span

from ..core.core import CoreComponent, cn


class ClassNames:
    BASE = (
        "group/badge inline-flex h-5 w-fit shrink-0 items-center justify-center gap-1 overflow-hidden "
        "rounded-4xl border border-transparent px-2 py-0.5 text-xs font-medium whitespace-nowrap "
        "focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 "
        "has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 aria-invalid:border-destructive "
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 [&>svg]:pointer-events-none [&>svg]:size-3!"
    )

    DEFAULT = "bg-primary text-primary-foreground [a]:hover:bg-primary/80"
    SECONDARY = "bg-secondary text-secondary-foreground [a]:hover:bg-secondary/80"
    DESTRUCTIVE = (
        "bg-destructive/10 text-destructive focus-visible:ring-destructive/20 "
        "dark:bg-destructive/20 dark:focus-visible:ring-destructive/40 [a]:hover:bg-destructive/20"
    )
    OUTLINE = "border-border text-foreground [a]:hover:bg-muted [a]:hover:text-muted-foreground"
    GHOST = "hover:bg-muted hover:text-muted-foreground dark:hover:bg-muted/50"
    LINK = "text-primary underline-offset-4 hover:underline"


BADGE_VARIANTS = {
    "default": ClassNames.DEFAULT,
    "secondary": ClassNames.SECONDARY,
    "destructive": ClassNames.DESTRUCTIVE,
    "outline": ClassNames.OUTLINE,
    "ghost": ClassNames.GHOST,
    "link": ClassNames.LINK,
}


def badge_variants(variant: str = "default") -> Var:
    return cn(
        ClassNames.BASE,
        BADGE_VARIANTS.get(variant, BADGE_VARIANTS["default"]),
    )


class BadgeComponent(Span, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Span:
        custom_classes = props.pop("class_name", "")
        variant = props.pop("variant", "default")
        props["data-slot"] = "badge"
        props["data-variant"] = variant

        return super().create(
            *children,
            class_name=cn(badge_variants(variant), custom_classes),
            **props,
        )


class Badge(CoreComponent):
    __call__ = staticmethod(BadgeComponent.create)
    class_names = ClassNames


badge = BadgeComponent.create
