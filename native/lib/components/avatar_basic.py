import reflex as rx

from components.avatar import avatar


def avatar_basic() -> rx.Component:
    fallback_id = "avatar-basic-fallback"

    return avatar.root(
        avatar.image(
            src="https://github.com/LineIndent.png",
            fallback_id=fallback_id,
            custom_attrs={"alt": "@lineindent"},
        ),
        avatar.fallback(
            "AH",
            fallback_id=fallback_id,
        ),
    )
