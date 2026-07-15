import functools
from typing import Callable

from reflex_components_core.el import Main, Section, div, h1, main, p, section

from native.templates.footer import _footer
from native.templates.navbar import navbar


def layout_decorator(
    title: str, description: str, ctas: list | None = None, logos: list | None = None
) -> Callable[[Callable[..., Section]], Callable[..., Main]]:

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            page_content = func(*args, **kwargs)
            return main(
                section(
                    # navbar(),
                    navbar(class_name="max-w-full !pl-4 !pr-6"),
                    div(
                        div(
                            h1(
                                title,
                                class_name="mx-auto max-w-4xl py-4 text-center text-4xl font-bold tracking-tighter text-balance sm:text-5xl md:py-6",
                            ),
                            p(
                                description,
                                class_name="text-md mx-auto max-w-2xl text-center text-pretty text-muted-foreground",
                            ),
                            div(
                                *(ctas if ctas else []),
                                class_name="flex w-full items-center justify-center gap-2 pt-8 **:data-[slot=button]:shadow-none",
                            ),
                            div(
                                *(logos if logos else []),
                                class_name="mx-auto mt-10 flex justify-center",
                            ),
                            class_name="mx-auto flex flex-1 flex-col",
                        ),
                        class_name="w-full px-4",
                    ),
                    page_content,
                    _footer(),
                    class_name="flex min-h-screen flex-col gap-8",
                ),
                class_name="mx-auto min-h-screen max-w-[96rem]",
            )

        return wrapper

    return decorator
