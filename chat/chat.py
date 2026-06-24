"""
Chat core for a streaming, multi-turn chatbot.

Split deliberately so the *logic* (build_messages, trim_history, parse_reply)
is pure and unit-testable OFFLINE, while only call_llm touches the network.
The 3 contract tests mock call_llm and must pass with NO API key set.

Conventions used throughout:
  - `history` is a list of {"role": "user"|"assistant", "content": str} dicts,
    oldest first. It does NOT contain the system prompt.
  - `system` is the persona string (see dataset/system_prompts.json).
"""
from __future__ import annotations
import os


def build_messages(history: list[dict], system: str) -> dict:
    """Assemble the Anthropic Messages API request payload.

    TODO:
      - return a dict with at least: "system" (the persona string, FIRST/top-level)
        and "messages" (the history, in order, oldest -> newest).
      - the system prompt must be carried in the top-level "system" field, not
        inside "messages" (the Anthropic API takes system separately).
      - preserve the order of `history` exactly; do not reorder or drop turns here.
    Return the payload dict (you'll add model + max_tokens in call_llm).
    """
    raise NotImplementedError("Implement build_messages")


def trim_history(history: list[dict], max_tokens: int) -> list[dict]:
    """Trim conversation history to fit a token budget.

    TODO:
      - estimate the token cost of the history (a simple word/char estimate is
        fine for the contract test; count_tokens is a stretch goal).
      - while the estimate exceeds `max_tokens`, drop the OLDEST turn first.
      - never drop more than necessary; keep the most recent turns.
      - the system prompt is NOT part of `history`, so it's never dropped here.
    Return the trimmed history (a list, oldest -> newest).
    """
    raise NotImplementedError("Implement trim_history")


def call_llm(messages: dict) -> object:
    """Call the Anthropic Messages API (with streaming) and return the response.

    This is the ONLY function that touches the network. Tests mock it.

    TODO:
      - read the key from os.environ["ANTHROPIC_API_KEY"] (never hardcode it).
      - use a CURRENT model id: "claude-sonnet-4-6" (default) or
        "claude-haiku-4-5-20251001" (cheaper/faster). NEVER a claude-3-* id.
      - stream with client.messages.stream(...) so tokens arrive incrementally;
        return the final message (e.g. stream.get_final_message()).
    """
    raise NotImplementedError("Implement call_llm")


def parse_reply(resp: object) -> str:
    """Extract the assistant's text from an Anthropic response object.

    TODO:
      - the response has a `.content` list of blocks; join the text of the
        text blocks (block.type == "text").
      - handle a normal reply AND an empty response (no text blocks / empty
        content) by returning "" rather than raising.
    Return the reply as a string.
    """
    raise NotImplementedError("Implement parse_reply")
