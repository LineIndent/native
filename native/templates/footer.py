from reflex_components_core.el import Footer, a, footer, p, span


def _footer() -> Footer:
    return footer(
        p(
            span(
                "Built by ",
                a(
                    "Line Indent",
                    href="https://github.com/LineIndent",
                    class_name="font-semibold underline",
                ),
                " at ",
                a(
                    "Reflex",
                    href="https://reflex.dev",
                    class_name="font-semibold underline",
                ),
                ".",
            ),
            span(
                " The source code is available on ",
                a(
                    "GitHub",
                    href="https://github.com/LineIndent/native",
                    class_name="font-semibold underline",
                ),
                ".",
                class_name="block sm:inline",
            ),
            class_name="w-full text-[13px] font-light",
        ),
        class_name="w-full flex items-center justify-center py-8 text-muted-foreground !text-sm !text-center",
    )
