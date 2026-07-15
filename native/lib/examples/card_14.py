import reflex as rx

from components.ui.button import button
from components.ui.card import card
from native.templates.masonary import masonry_card



@masonry_card(label="General")
def card_14() -> rx.Component:
    return card.root(
        card.header(
            card.title(
                "Fellowship of the Ring.",
            ),
        ),
        card.content(
            rx.el.div(
                rx.el.p(
                    """Five hundred times have the red leaves fallen in Mirkwood in my home since then," said Legolas, "and but a little while does that seem to us.""",
                    class_name="text-sm font-light text-muted-foreground leading-relaxed font-theme",
                ),
                rx.el.p(
                    """I have seen many an oak grow from acorn to ruinous age. I wish that there were leisure now to walk among them: they have voices, and in time I might come to understand their thought.""",
                    class_name="text-sm font-light text-muted-foreground leading-relaxed font-theme",
                ),
                class_name="flex flex-col gap-y-2",
            ),
        ),
        card.footer(
            button(
                "Share Feedback",
                variant="outline",
                class_name="w-full rounded-full",
            ),
        ),
    )
