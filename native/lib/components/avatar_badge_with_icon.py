import reflex as rx

from components.avatar import avatar
from components.hugeicon import hi


def avatar_badge_icon() -> rx.Component:
    fallback_id = "avatar-badge-icon-fallback"

    return avatar.root(
        avatar.image(
            src="https://avatars.githubusercontent.com/u/104714959?s=200&v=4",
            fallback_id=fallback_id,
            custom_attrs={"alt": "Reflex Dev"},
        ),
        avatar.fallback(
            "RD",
            fallback_id=fallback_id,
        ),
        avatar.badge(
            hi("PlusSignIcon"),
        ),
    )
