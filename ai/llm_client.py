"""
Provider-agnostic LLM call. Every other file in this pipeline (registry,
renderer, prompt_builder) has zero knowledge of which LLM you're using —
this is the only file that does. Pick a provider via the PROVIDER env var
or the `provider` argument.

    export ANTHROPIC_API_KEY=sk-ant-...   # provider="anthropic" (default)
    export OPENAI_API_KEY=sk-...          # provider="openai"
    export GEMINI_API_KEY=...             # provider="gemini"

Model strings below are current as of this writing — check each provider's
docs before relying on them long-term; these change more often than the
pipeline logic around them.
"""

import json
import os

from prompt_builder import build_system_prompt

MODELS = {
    "anthropic": "claude-sonnet-5",
    "openai": "gpt-5.1",
    "gemini": "gemini-3.1-flash-lite",
}


def strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


def _call_anthropic(system_prompt: str, user_prompt: str) -> str:
    from anthropic import Anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODELS["anthropic"],
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def _call_openai(system_prompt: str, user_prompt: str) -> str:
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=MODELS["openai"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


def _call_gemini(system_prompt: str, user_prompt: str) -> str:
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODELS["gemini"],
        contents=user_prompt,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    return response.text


PROVIDER_FNS = {
    "anthropic": _call_anthropic,
    "openai": _call_openai,
    "gemini": _call_gemini,
}


def generate_ui_json(user_prompt: str, provider: str | None = None) -> dict:
    provider = provider or os.environ.get("PROVIDER", "anthropic")
    if provider not in PROVIDER_FNS:
        raise ValueError(f"Unknown provider '{provider}'. Choose from: {list(PROVIDER_FNS)}")

    system_prompt = build_system_prompt()
    raw_text = PROVIDER_FNS[provider](system_prompt, user_prompt)
    cleaned = strip_code_fences(raw_text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Model output wasn't valid JSON: {e}\n\nRaw output:\n{raw_text}"
        )


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    provider = "anthropic"
    if args and args[0] in PROVIDER_FNS:
        provider, args = args[0], args[1:]

    prompt = " ".join(args) or "a button that says Save"
    print(f"[provider: {provider}]")
    tree = generate_ui_json(prompt, provider=provider)
    print(json.dumps(tree, indent=2))
