import reflex as rx

from components.avatar import avatar


def avatar_with_group_count() -> rx.Component:
    return avatar.group(
        avatar.root(
            avatar.image(
                src="/avatars/10.png",
                alt="@avatar-10",
            ),
            avatar.fallback("AH"),
        ),
        avatar.root(
            avatar.image(
                src="/avatars/01.png",
                alt="@avatar-1",
            ),
            avatar.fallback("RD"),
        ),
        avatar.root(
            avatar.image(
                src="/avatars/02.png",
                alt="@avatar-2",
            ),
            avatar.fallback("LI"),
        ),
        avatar.group_count("+3"),
        class_name="grayscale",
    )
