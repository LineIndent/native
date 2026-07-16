# Building a Streaming Chatbot

The `use_chat` state logic makes it effortless to create a conversational user interface for your chatbot application. It enables the streaming of chat messages from your AI provider, manages the chat state, and updates the UI automatically as new messages arrive.

To summarize, the streaming chat setup provides the following features:

- **Message Streaming**: All the messages from the AI provider are streamed to the chat UI in real-time.
- **Managed States**: Your state class manages the values for input, messages, status, error and more for you.
- **Seamless Integration**: Easily integrate your chat AI into any design or layout with minimal effort.

In this guide, you will learn how to implement a chatbot application with real-time message streaming. Check out our [chatbot with tools guide](https://www.google.com/search?q=/docs/ai-sdk-ui/chatbot-tool-usage) to learn how to use tools in your chatbot.

## Example

The request flow works like this:

1. The user submits a message and `send_message` triggers a backend background task.
2. Your event handler calls the provider and receives a real-time generator stream.
3. The state appends chunks to the last message as they arrive, yielding to trigger UI updates.

```
import reflex as rx

class ChatState(rx.State):
    messages: list[dict] = []
    status: str = "ready"

    async def send_message(self, text: str):
        self.messages.append({"role": "user", "content": text})
        self.status = "submitted"
        yield

        # Request to the streaming handler
        async for chunk in get_stream_response(self.messages):
            if self.status == "submitted":
                self.status = "streaming"
                self.messages.append({"role": "assistant", "content": ""})

            self.messages[-1]["content"] += chunk
            yield

        self.status = "ready"
        yield

def chat_interface() -> rx.Component:
    return rx.fragment(
        rx.foreach(
            ChatState.messages,
            lambda msg: render_message(msg)
        ),
        ChatInput(
            on_submit=lambda text: ChatState.send_message(text),
            disabled=ChatState.status != "ready"
        )
    )

```

```
import openai

async def get_stream_response(messages: list[dict]):
    client = openai.AsyncOpenAI()

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,
    )

    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield content

```

> The UI messages have a new `parts` property that contains the message parts. We recommend rendering the messages using the `parts` property instead of the `content` property. The parts property supports different message types, including text, tool invocation, and tool result, and allows for more flexible and complex chat UIs.

In the `Page` component, the streaming hooks will request to your AI provider endpoint whenever the user sends a message using `send_message`. The messages are then streamed back in real-time and displayed in the chat UI.

## Customized UI

You can also manage the chat message states via code, show status, and update messages without being triggered by user interactions.

### Status

The state manages a `status` variable. It has the following possible values:

- `submitted`: The message has been sent to the API and we're awaiting the start of the response stream.
- `streaming`: The response is actively streaming in from the API, receiving chunks of data.
- `ready`: The full response has been received and processed; a new user message can be submitted.
- `error`: An error occurred during the API request, preventing successful completion.

```
# Inside your layout component
rx.cond(
    (ChatState.status == "submitted") | (ChatState.status == "streaming"),
    rx.hstack(
        rx.cond(ChatState.status == "submitted", Spinner()),
        rx.button("Stop", on_click=ChatState.stop_stream)
    )
)

```

### Error State

Similarly, the `error` state reflects the error object thrown during the request. It can be used to display an error message, disable the submit button, or show a retry button:

> We recommend showing a generic error message to the user, such as "Something went wrong." This is a good practice to avoid leaking information from the server.

```
# Inside your layout component
rx.cond(
    ChatState.has_error,
    rx.fragment(
        rx.text("An error occurred."),
        rx.button("Retry", on_click=ChatState.regenerate_last)
    )
)

```

### Cancellation and regeneration

It's also a common use case to abort the response message while it's still streaming back from the AI provider. You can do this by calling a cancel method that interrupts the async generator loop in your state.

```
rx.button(
    "Stop",
    on_click=ChatState.stop_stream,
    disabled=~((ChatState.status == "streaming") | (ChatState.status == "submitted"))
)

```

---

## API reference

### use_chat config (State options)

Creates a chat helper state. All values are customizable; the defaults query the stream API and render at native generator speed.

| Prop        | Type                          | Description                                     |
| ----------- | ----------------------------- | ----------------------------------------------- |
| `transport` | `ChatTransport`               | How messages reach your API route               |
| `messages`  | `list[dict]`                  | Initial messages to seed the conversation       |
| `on_finish` | `Callable[[str], None]`       | Runs when the assistant response completes      |
| `on_error`  | `Callable[[Exception], None]` | Runs when the stream connection fails           |
| `throttle`  | `float`                       | Seconds to sleep between yields while streaming |

## Event Callbacks

The chat state provides optional event callbacks that you can use to handle different stages of the chatbot lifecycle:

- `on_finish`: Called when the assistant response is completed. The event includes the response message, all messages, and flags for abort, disconnect, and errors.
- `on_error`: Called when an error occurs during the fetch request.
- `on_data`: Called whenever a data part is received.

These callbacks can be used to trigger additional actions, such as logging, analytics, or custom UI updates.

```
class ConfiguredChatState(rx.State):
    def on_finish(self, message: dict):
        self.save_to_history(message)

    def on_error(self, error: Exception):
        logger.error(f"Chat stream failed: {error}")

```

---

## Math

Display math sits in the flow rhythm and scrolls when it runs long. Inline math like eiπ+1=0 rides the line without stretching it.

### Display

The quadratic formula, as a block:

<math display="block">
  <mi>x</mi><mo>=</mo>
  <mfrac>
    <mrow><mo>−</mo><mi>b</mi><mo>±</mo><msqrt><mrow><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi></mrow></msqrt></mrow>
    <mrow><mn>2</mn><mi>a</mi></mrow>
  </mfrac>
</math>

### Overflow

A long expansion scrolls inside its own box instead of breaking the column:

<math display="block">
  <msup>
    <mrow>
      <mo>(</mo>
      <mi>a</mi>
      <mo>+</mo>
      <mi>b</mi>
      <mo>)</mo>
    </mrow>
    <mn>4</mn>
  </msup>
  <mo>=</mo>
  <msup>
    <mi>a</mi>
    <mn>4</mn>
  </msup>
  <mo>+</mo>
  <mn>4</mn>
  <msup>
    <mi>a</mi>
    <mn>3</mn>
  </msup>
  <mi>b</mi>
  <mo>+</mo>
  <mn>6</mn>
  <msup>
    <mi>a</mi>
    <mn>2</mn>
  </msup>
  <msup>
    <mi>b</mi>
    <mn>2</mn>
  </msup>
  <mo>+</mo>
  <mn>4</mn>
  <mi>a</mi>
  <msup>
    <mi>b</mi>
    <mn>3</mn>
  </msup>
  <mo>+</mo>
  <msup>
    <mi>b</mi>
    <mn>4</mn>
  </msup>
</math>
