import reflex as rx

from native.registry.anatomy import ANATOMY
from native.templates._install import file_codeblock, file_codeblock_full


def usage(raw_arg, files):
    # intro = raw_arg.strip("[]").strip()

    # if "," not in intro:
    #     raise ValueError(f"Invalid INTRO format: {raw_arg!r}")

    # title, description = intro.split(",", 1)
    # slug = title.strip().lower().replace(" ", "-")
    # copy_id = f"copy-command-{slug}"
    # command_id = f"command-{slug}"

    anatomy = ANATOMY.get(raw_arg)

    return rx.el.div(
        # rx.el.div(
        #     class_name="w-full flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between",
        # ),
        rx.el.div(
            rx.el.h1(
                "Component Guide",
                class_name="text-2xl leading-tight font-bold tracking-tighter",
            ),
            rx.el.p(
                rx.el.span("Use the following to build the "),
                rx.el.strong(raw_arg.capitalize()),
                rx.el.span(" component."),
                class_name="text-sm text-muted-foreground",
            ),
            rx.el.h2(
                "Usage",
                class_name="text-xl leading-tight font-bold tracking-tighter",
            ),
            rx.el.p(
                "The default component path.",
                class_name="text-sm text-muted-foreground",
            ),
            rx.el.div(
                rx.el.code(
                    rx.el.span(
                        "from",
                        class_name="font-medium text-foreground",
                    ),
                    rx.el.span(
                        f" components.ui.{raw_arg}",
                        class_name="font-medium text-muted-foreground",
                    ),
                    rx.el.span(
                        " import",
                        class_name="font-medium text-foreground",
                    ),
                    rx.el.span(
                        f" {raw_arg}",
                        class_name="font-medium text-muted-foreground",
                    ),
                    class_name=(
                        "flex h-8 min-w-0 flex-1 items-center gap-2 "
                        "overflow-x-auto border border-border bg-muted/40 "
                        "px-3 font-mono text-sm whitespace-nowrap"
                    ),
                ),
                class_name="w-full",
            ),
            rx.el.h2(
                "Anatomy",
                class_name="text-xl leading-tight font-bold tracking-tighter",
            ),
            rx.el.p(
                f"Use the following composition to build the {raw_arg.capitalize()} component.",
                class_name="text-sm text-muted-foreground",
            ),
            rx.el.div(
                rx.el.code(
                    anatomy,
                    class_name="block whitespace-pre px-3 py-2 font-mono",
                ),
                class_name=(
                    "w-full overflow-x-auto border border-border bg-muted/40 "
                    "flex-1 min-h-0 flex flex-col text-sm"
                ),
            ),
            rx.el.h2(
                "Source Code & Dependencies",
                class_name="text-xl leading-tight font-bold tracking-tighter",
            ),
            rx.el.p(
                "For manual installation, copy each of the source codes below in their respective locations.",
                class_name="text-sm text-muted-foreground",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "1. Copy and paste the following dependencies into your project.",
                        class_name="text-sm font-medium",
                    ),
                    rx.el.div(
                        *[file_codeblock(file[0], file[1]) for file in files[:-1]],
                        class_name="w-full flex flex-col gap-y-4",
                    ),
                    class_name="w-full flex flex-col gap-y-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "2. Copy and paste the following component code into your project.",
                        class_name="text-sm font-medium",
                    ),
                    file_codeblock_full(files[-1][0], files[-1][1]),
                    class_name="w-full flex flex-col gap-y-4",
                ),
                class_name="flex flex-col gap-y-6",
            )
            if len(files) > 1
            else file_codeblock_full(files[-1][0], files[-1][1]),
            class_name="flex flex-col items-start gap-4",
        ),
        class_name="w-full flex flex-col gap-6",
    )
