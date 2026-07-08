import uuid

import reflex as rx
from reflex.components.component import ComponentNamespace
from reflex_components_core.el import Div, Span

from ..core.core import CoreComponent, cn


class ClassNames:
    ROOT = (
        "group/avatar relative flex size-8 shrink-0 rounded-full select-none "
        "after:absolute after:inset-0 after:rounded-full after:border after:border-border "
        "after:mix-blend-darken data-[size=xl]:size-14 data-[size=lg]:size-10 "
        "data-[size=sm]:size-6 dark:after:mix-blend-lighten"
    )
    IMAGE = "aspect-square size-full rounded-full object-cover"
    FALLBACK = (
        "flex size-full items-center justify-center rounded-full bg-muted text-sm "
        "text-muted-foreground group-data-[size=sm]/avatar:text-xs"
    )
    BADGE = (
        "absolute right-0 bottom-0 z-10 inline-flex items-center justify-center "
        "rounded-full bg-primary text-primary-foreground bg-blend-color "
        "ring-2 ring-background select-none "
        "group-data-[size=sm]/avatar:size-2 group-data-[size=sm]/avatar:[&>svg]:hidden "
        "group-data-[size=default]/avatar:size-2.5 group-data-[size=default]/avatar:[&>svg]:size-2 "
        "group-data-[size=lg]/avatar:size-3 group-data-[size=lg]/avatar:[&>svg]:size-2"
    )
    GROUP = (
        "group/avatar-group flex -space-x-2 "
        "*:data-[slot=avatar]:ring-2 *:data-[slot=avatar]:ring-background"
    )
    GROUP_COUNT = (
        "relative flex size-8 shrink-0 items-center justify-center rounded-full "
        "bg-muted text-sm text-muted-foreground ring-2 ring-background "
        "group-has-data-[size=lg]/avatar-group:size-10 "
        "group-has-data-[size=sm]/avatar-group:size-6 "
        "[&>svg]:size-4 group-has-data-[size=lg]/avatar-group:[&>svg]:size-5 "
        "group-has-data-[size=sm]/avatar-group:[&>svg]:size-3"
    )


class AvatarRoot(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        custom_classes = props.pop("class_name", "")
        size = props.pop("size", "default")
        props["data-slot"] = "avatar"
        props["data-size"] = size
        return super().create(
            *children, class_name=cn(ClassNames.ROOT, custom_classes), **props
        )


class AvatarImage(CoreComponent):
    """
    Renders an <img> and probes its `src` client-side on mount. If the image
    fails to load, it hides itself and reveals the sibling AvatarFallback
    (matched via the nearest ancestor with data-slot="avatar").

    Note: if this is rendered inside rx.foreach, the auto-generated uuid will
    be baked in once at template-build time and shared across all rendered
    items. In that case pass an explicit `id` derived from your loop data,
    e.g. id=f"avatar-img-{user.id}".
    """

    @classmethod
    def create(cls, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-image"

        img_id = props.get("id") or f"avatar-img-{uuid.uuid4().hex[:8]}"
        props["id"] = img_id

        src = props.get("src", "")

        js = f"""
        (function() {{
            var img = document.getElementById('{img_id}');
            if (!img) return;
            var root = img.closest('[data-slot="avatar"]');
            var fallback = root ? root.querySelector('[data-slot="avatar-fallback"]') : null;
            var tester = new Image();
            tester.onload = function() {{
                img.style.display = '';
                if (fallback) fallback.style.display = 'none';
            }};
            tester.onerror = function() {{
                img.style.display = 'none';
                if (fallback) fallback.style.display = 'flex';
            }};
            tester.src = '{src}';
        }})()
        """

        props["on_mount"] = rx.call_script(js)

        cls.set_class_name(cn(ClassNames.IMAGE, custom_classes), props)
        return rx.el.img(**props)


class AvatarFallback(Span, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Span:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-fallback"
        props["style"] = {"display": "none", **props.get("style", {})}
        return super().create(
            *children, class_name=cn(ClassNames.FALLBACK, custom_classes), **props
        )


class AvatarBadge(Span, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Span:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-badge"
        return super().create(
            *children, class_name=cn(ClassNames.BADGE, custom_classes), **props
        )


class AvatarGroup(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-group"
        return super().create(
            *children, class_name=cn(ClassNames.GROUP, custom_classes), **props
        )


class AvatarGroupCount(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "avatar-group-count"
        return super().create(
            *children, class_name=cn(ClassNames.GROUP_COUNT, custom_classes), **props
        )


class Avatar(ComponentNamespace):
    root = staticmethod(AvatarRoot.create)
    image = staticmethod(AvatarImage.create)
    fallback = staticmethod(AvatarFallback.create)
    badge = staticmethod(AvatarBadge.create)
    group = staticmethod(AvatarGroup.create)
    group_count = staticmethod(AvatarGroupCount.create)
    class_names = ClassNames


avatar = Avatar()
