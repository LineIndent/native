import reflex as rx

from components.ui.avatar import avatar


def avatar_with_badge() -> rx.Component:
    fallback_id = "avatar-badge-fallback"

    return avatar.root(
        avatar.image(
            src="https://avatars.githubusercontent.com/u/84860195?v=4",
            fallback_id=fallback_id,
            custom_attrs={"alt": "@LineIndent"},
        ),
        avatar.fallback(
            "AH",
            fallback_id=fallback_id,
        ),
        avatar.badge(
            class_name="bg-green-600 dark:bg-green-800",
        ),
    )
