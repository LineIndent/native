import reflex as rx

from components.avatar import avatar


def avatar_sizes() -> rx.Component:
    return rx.el.div(
        avatar.root(
            avatar.image(
                src="https://avatars.githubusercontent.com/u/84860195?v=4",
                alt="@LineIndent",
            ),
            avatar.fallback("LI"),
            size="sm",
        ),
        avatar.root(
            avatar.image(
                src="https://avatars.githubusercontent.com/u/84860195?v=4",
                alt="@LineIndent",
            ),
            avatar.fallback("LI"),
        ),
        avatar.root(
            avatar.image(
                src="https://avatars.githubusercontent.com/u/84860195?v=4",
                alt="@LineIndent",
            ),
            avatar.fallback("LI"),
            size="lg",
        ),
        class_name="flex flex-wrap items-center gap-2",
    )
