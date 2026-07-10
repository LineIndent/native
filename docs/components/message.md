---
title: "Message"
description: "Displays a message in a conversation, with optional avatar, header, footer, and alignment."
order: 13
---

--INTRO([Message, Displays a message in a conversation, with optional avatar, header, footer, and alignment.])--

--USAGE(message)--

--SOURCE(message)--

The `Message` component lays out a single message in a conversation. It handles the avatar, alignment, header, and footer around the message surface.

For AI apps, you can render reasoning steps, tool calls and assistant messages using the `Message` component.


# Examples

## Avatar

Use `message.avatar` to render an avatar next to the message. Set `align="end"` on the message to align the avatar to the end of the message.

**Props used:** `align` on `message.root`.

--DEMO(message_with_avatar)--

| align   | Description                                         |
| ------- | --------------------------------------------------- |
| `start` | Align the message to the start of the conversation. |
| `end`   | Align the message to the end of the conversation.   |

## Group

Use `message.group` to stack consecutive messages from the same sender. Render an empty `message.avatar` on the earlier messages to keep them aligned with the avatar on the last one.

**Props used:** none required beyond default `message.group` composition.

--DEMO(message_with_group)--

## Header and Footer

Use `message.header` for a sender name and `message.footer` for metadata such as a delivery or read status.

**Props used:** none required beyond default `message.header`/`message.footer` composition.

--DEMO(message_header_footer)--

## Actions

Place message-level actions in `message.footer`, such as copy, retry, or feedback buttons.

**Props used:** none required — place `button(...)` inside `message.footer`.

--DEMO(message_with_actions)--

## Attachment

Use the [`Attachment`](/docs/components/attachment) with the messages to displays a file or image attachment with media, metadata, upload state, and actions.

**Props used:** see the [Attachment](/docs/components/attachment) docs for attachment-specific props.

--DEMO(message_with_attachment)--

# Accessibility

`Message` is a presentational layout wrapper. Accessibility comes from the content you place inside it.

## Label icon-only actions

Action buttons in `message.footer` are usually icon-only, so give each one an `aria-label`.

```python
message.footer(
    button(
        hi("Refresh03Icon"),
        variant="ghost",
        size="sm",
        title="Retry",
        aria_label="Retry",
    ),
)
```

## Status updates

For in-progress messages, use a [`Marker`](/docs/components/marker) with `role="status"` so assistive tech announces the update as it appears.

```python
message.root(
    message.content(
        marker.root(
            marker.icon(spinner()),
            marker.content("Compacting conversation"),
            role="status",
        ),
    ),
)
```

# API Reference

## message.root

The message row wrapper.

| Prop        | Type               | Default   | Description                                       |
| ----------- | ------------------ | --------- | ------------------------------------------------- |
| `align`     | `Literal["start", "end"]` | `"start"` | The alignment of the message in the conversation. |
| `class_name` | `str`           | -         | Additional classes to apply to the row.           |

## message.group

Groups consecutive messages from the same sender.

| Prop        | Type     | Default | Description                                    |
| ----------- | -------- | ------- | ---------------------------------------------- |
| `class_name` | `str` | -       | Additional classes to apply to the group root. |

## message.avatar

The avatar slot, aligned to the bottom of the message. When the message has a `message.footer`, the avatar shifts up to stay aligned with the message surface instead of the footer.

| Prop        | Type     | Default | Description                                     |
| ----------- | -------- | ------- | ----------------------------------------------- |
| `class_name` | `str` | -       | Additional classes to apply to the avatar slot. |

### message.content

Wraps the header, message surface, and footer.

| Prop        | Type     | Default | Description                                      |
| ----------- | -------- | ------- | ------------------------------------------------ |
| `class_name` | `str` | -       | Additional classes to apply to the content slot. |

### message.header

Displays content above the message, such as a sender name. Stays aligned to the start regardless of `align`.

| Prop        | Type     | Default | Description                                |
| ----------- | -------- | ------- | ------------------------------------------ |
| `class_name` | `str` | -       | Additional classes to apply to the header. |

### message.footer

Displays content below the message, such as status or actions. Aligns to the message side.

| Prop        | Type     | Default | Description                                |
| ----------- | -------- | ------- | ------------------------------------------ |
| `class_name` | `str` | -       | Additional classes to apply to the footer. |
