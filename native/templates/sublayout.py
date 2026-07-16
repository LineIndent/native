import functools
from typing import Callable

from reflex_components_core.el import Div, Main, div, h1, main, p, section

from native.templates.footer import _footer
from native.templates.navbar import navbar


def sub_layout_decorator(
    badge_name: str,
    title: str,
    description: str,
    search: Div | list,
) -> Callable[[Callable[..., Div]], Callable[..., Main]]:

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            page_content = func(*args, **kwargs)
            return main(
                section(
                    navbar(),
                    div(
                        section(
                            div(
                                div(
                                    div(
                                        badge_name,
                                        class_name="inline-flex w-fit items-center gap-1.5 bg-primary px-2.5 py-1 text-xs font-medium text-primary-foreground",
                                    ),
                                    h1(
                                        title,
                                        class_name="text-2xl leading-tight font-bold tracking-tighter",
                                    ),
                                    p(
                                        description,
                                        class_name="text-sm text-muted-foreground max-w-2xl",
                                    ),
                                    class_name="flex flex-col items-start gap-3",
                                ),
                                div(
                                    search if search else [],
                                    class_name="relative w-full sm:w-64 sm:shrink-0",
                                ),
                                class_name="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between",
                            ),
                            page_content,
                            class_name="mx-auto flex w-full max-w-5xl flex-col gap-8 px-4 sm:px-2",
                        ),
                        class_name="flex flex-col w-full gap-8",
                    ),
                    _footer(),
                    class_name="flex min-h-screen flex-col gap-16",
                ),
                class_name="mx-auto min-h-screen w-full",
            )

        return wrapper

    return decorator
