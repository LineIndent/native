import reflex as rx
from reflex_components_core.el import Pre

from .core import CoreComponent


class ClassNames:
    # Set up the scrollable outer code container
    # Everything structure-related goes here since Pre has no defaults
    PRE = ""

    # Text presentation classes translated straight from your inline styles
    CODE = "block whitespace-pre text-foreground text-[13px]! p-4 select-text"


class CodeBlock(Pre, CoreComponent):
    @classmethod
    def create(cls, code_string: str, **props) -> Pre:
        props["data-slot"] = "code-block"
        cls.set_class_name(ClassNames.PRE, props)

        # We construct a styled inner code element to house the string
        inner_code = rx.el.code(code_string, class_name=ClassNames.CODE)

        # Return the pre container with the semantic inner code segment nested inside
        return super().create(inner_code, **props)


# Create a handy namespace shortcut if you like, or just map it directly
code = CodeBlock.create
