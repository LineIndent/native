import functools

from reflex_components_core.el import div


def masonry_card(func=None, *, label="General"):
    if func is None:
        return functools.partial(masonry_card, label=label)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inner_component = func(*args, **kwargs)

        return div(
            inner_component,
            class_name=" ".join(
                [
                    "break-inside-avoid",
                    "w-full",
                    "[&>*]:shadow-lg",
                    "[&>*]:border-t-[0.85px] [&>*]:border-input/80",
                ]
            ),
        )

    return wrapper
