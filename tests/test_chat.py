"""
Contract tests — fail against the starter stubs; make them pass.

These run OFFLINE: no ANTHROPIC_API_KEY, no network. The LLM is mocked, so the
tests only exercise the deterministic logic (build_messages, trim_history,
parse_reply) — never call_llm against the real API.
"""
from types import SimpleNamespace

from chat import build_messages, trim_history, parse_reply


def _block(text):
    """A fake Anthropic text content block."""
    return SimpleNamespace(type="text", text=text)


def test_trim_history_respects_budget_drops_oldest_first():
    # 6 turns; a tiny budget must force the OLDEST turns out, keeping the newest.
    history = [
        {"role": "user", "content": "one one one one one"},
        {"role": "assistant", "content": "two two two two two"},
        {"role": "user", "content": "three three three three three"},
        {"role": "assistant", "content": "four four four four four"},
        {"role": "user", "content": "five five five five five"},
        {"role": "assistant", "content": "six six six six six"},
    ]
    trimmed = trim_history(history, max_tokens=10)
    assert len(trimmed) < len(history)              # something was dropped
    assert trimmed == history[len(history) - len(trimmed):]  # kept a recent suffix
    assert trimmed[-1] == history[-1]               # newest turn is always kept
    assert history[0] not in trimmed                # oldest turn went first


def test_build_messages_system_first_and_order_preserved():
    history = [
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": "second"},
        {"role": "user", "content": "third"},
    ]
    payload = build_messages(history, system="You are a helpful tutor.")
    # System prompt carried at the top level (not buried in messages).
    assert payload["system"] == "You are a helpful tutor."
    # History order preserved exactly.
    assert [m["content"] for m in payload["messages"]] == ["first", "second", "third"]
    assert payload["messages"][0]["role"] == "user"


def test_parse_reply_handles_normal_and_empty():
    normal = SimpleNamespace(content=[_block("Hello "), _block("there!")])
    assert parse_reply(normal) == "Hello there!"

    empty = SimpleNamespace(content=[])
    assert parse_reply(empty) == ""
