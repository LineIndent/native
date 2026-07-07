from components.ui.card import card

COMPOSITION = card.root(
    card.header(
        card.title(),
        card.description(),
        card.action(),
    ),
    card.content(),
    card.footer(),
)
