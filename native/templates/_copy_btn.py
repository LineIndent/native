import json
import random
import string

import reflex as rx

from components.hugeicon import hi


def generate_component_id() -> str:
    """Generate a unique component ID."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def create_copy_button(content: str) -> rx.Component:
    uid = generate_component_id()
    btn_id = f"btn-{uid}"
    icon_id = f"icon-{uid}"

    copy_icon_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" color="currentColor" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 15C9 12.1716 9 10.7574 9.87868 9.87868C10.7574 9 12.1716 9 15 9L16 9C18.8284 9 20.2426 9 21.1213 9.87868C22 10.7574 22 12.1716 22 15V16C22 18.8284 22 20.2426 21.1213 21.1213C20.2426 22 18.8284 22 16 22H15C12.1716 22 10.7574 22 9.87868 21.1213C9 20.2426 9 18.8284 9 16L9 15Z"/><path d="M16.9999 9C16.9975 6.04291 16.9528 4.51121 16.092 3.46243C15.9258 3.25989 15.7401 3.07418 15.5376 2.90796C14.4312 2 12.7875 2 9.5 2C6.21252 2 4.56878 2 3.46243 2.90796C3.25989 3.07417 3.07418 3.25989 2.90796 3.46243C2 4.56878 2 6.21252 2 9.5C2 12.7875 2 14.4312 2.90796 15.5376C3.07417 15.7401 3.25989 15.9258 3.46243 16.092C4.51121 16.9528 6.04291 16.9975 9 16.9999"/></svg>'
    tick_icon_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" color="currentColor" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 14.5C5 14.5 6.5 14.5 8.5 18C8.5 18 14.0588 8.83333 19 7"/></svg>'
    safe_content = json.dumps(content)

    return rx.el.button(
        hi("Copy01Icon", id=icon_id, class_name="size-4"),
        id=btn_id,
        class_name="px-[0.75rem]",
        on_click=rx.call_script(
            f"""
                const icon = document.getElementById('{icon_id}');
                navigator.clipboard.writeText({safe_content});

                // Swap to tick
                icon.innerHTML = `{tick_icon_svg}`;

                // Revert after 1.5s
                setTimeout(() => {{
                    icon.innerHTML = `{copy_icon_svg}`;
                }}, 1500);
            """
        ),
    )
