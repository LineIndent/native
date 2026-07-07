import reflex as rx

from components.button import button
from components.card import card
from components.hugeicon import hi
from components.input_group import input_group
from native.templates.masonary import masonry_card

social_fields = [
    {
        "label": "Spotify Artist URL",
        "icon": "SpotifyIcon",
        "placeholder": "spotify.com/artist/3j...2k",
        "value": "spotify.com/artist/3j...2k",
    },
    {
        "label": "Instagram Handle",
        "icon": "InstagramIcon",
        "placeholder": "@julianduryea_music",
        "value": "@julianduryea_music",
    },
    {
        "label": "SoundCloud URL",
        "icon": "SoundcloudIcon",
        "placeholder": "soundcloud.com/username",
        "value": "",
    },
    {
        "label": "Website",
        "icon": "InternetIcon",
        "placeholder": "https://yoursite.com",
        "value": "",
    },
]


@masonry_card(label="General")
def card_01() -> rx.Component:

    return card.root(
        card.header(
            card.title("Social Links"),
            card.description("Connect your platforms"),
        ),
        card.content(
            rx.el.div(
                *[
                    rx.el.div(
                        rx.el.p(
                            field["label"],
                            class_name="text-sm font-semibold text-foreground",
                        ),
                        input_group.root(
                            input_group.input(
                                id=f"inline-start-input-{field['label'].lower().replace(' ', '-')}",
                                placeholder=field["placeholder"],
                                default_value=field["value"],
                            ),
                            input_group.addon(
                                hi(
                                    field["icon"],
                                    class_name="text-muted-foreground size-4",
                                ),
                                align="inline-start",
                            ),
                        ),
                        class_name="w-full flex flex-col gap-y-2",
                    )
                    for field in social_fields
                ],
                class_name="w-full flex flex-col gap-y-3",
            )
        ),
        card.footer(
            button("Discard", variant="secondary", size="sm"),
            button("Save Changes", variant="default", size="sm"),
            class_name="w-full flex flex-row items-center justify-end gap-x-2",
        ),
        class_name="mx-auto w-full max-w-sm",
    )
