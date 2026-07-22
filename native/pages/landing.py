from reflex_components_core.el import Section, a, div, img, section

from components.core.hugeicon import hi
from components.ui.button import button
from native.lib.examples.card_01 import card_01
from native.lib.examples.card_02 import card_02
from native.lib.examples.card_03 import card_03
from native.lib.examples.card_04 import card_04
from native.lib.examples.card_05 import card_05
from native.lib.examples.card_06 import card_06
from native.lib.examples.card_07 import card_07
from native.lib.examples.card_08 import card_08
from native.lib.examples.card_09 import card_09
from native.lib.examples.card_10 import card_10
from native.lib.examples.card_11 import card_11
from native.lib.examples.card_12 import card_12
from native.lib.examples.card_13 import card_13
from native.templates.layout import layout_decorator


@layout_decorator(
    title="Native HTML UI components you can copy, paste, and ship in minutes.",
    description="Production-ready shadcn/ui blocks and components designed for Reflex. Extend, override, and ship without fighting the framework. Open souce, no lock-in.",
    ctas=[
        a(
            button("Build Your Own", hi("ArrowRight02Icon", class_name="size-4")),
            href="/create",
        ),
    ],
)
def landing_page() -> Section:

    landing_desktop = div(
        card_01(),
        card_02(),
        card_03(),
        card_04(),
        card_05(),
        card_06(),
        card_07(),
        card_08(),
        card_09(),
        card_10(),
        card_11(),
        card_12(),
        card_13(),
        class_name=" ".join(
            [
                # -> main layout style
                "mx-auto",
                # "max-w-6xl",
                # "columns-[260px]",
                "max-w-[96rem]",
                "columns-[320px]",
                "px-7",
                "gap-8",
                "space-y-8",
                # -> create masking fade-away at the bottom of the component
                "sm:mask-[linear-gradient(to_bottom,black_65%,transparent_100%)]",
                "sm:mask-size-[100%_100%]",
                "sm:mask-repeat-no-repeat",
            ]
        ),
    )

    landing_mobile = div(
        img(
            src="site/landing_ss_dark.webp",
            class_name="w-[1450px] max-w-none hidden dark:flex",
        ),
        img(
            src="/site/landing_ss_light.webp",
            class_name="w-[1450px] max-w-none flex dark:hidden",
        ),
        class_name="overflow-x-hidden w-full flex justify-center",
    )

    return section(
        div(landing_desktop, class_name="hidden sm:block"),
        div(landing_mobile, class_name="flex sm:hidden"),
        class_name="mx-auto w-full relative",
    )
