"""
Interactive REPL:  python -m chat.cli

Wires the chat/ functions into a multi-turn loop: load a persona, keep history,
trim to the budget, stream the reply, append it back. Needs ANTHROPIC_API_KEY set.
Type 'quit' to exit.
"""
import json
import os
from pathlib import Path

from .chat import build_messages, trim_history, call_llm, parse_reply

PERSONA_ID = "study-buddy"  # change to a persona id from dataset/system_prompts.json
MAX_HISTORY_TOKENS = 2000


def load_persona(persona_id: str) -> str:
    path = Path(__file__).resolve().parent.parent / "dataset" / "system_prompts.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for p in data["personas"]:
        if p["id"] == persona_id:
            return p["system"]
    raise SystemExit(f"Unknown persona '{persona_id}'. See dataset/system_prompts.json")


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY in your environment first.")

    system = load_persona(PERSONA_ID)
    history: list[dict] = []
    print(f"[{PERSONA_ID}] chatbot ready. Type 'quit' to exit.\n")

    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit"}:
            break
        history.append({"role": "user", "content": user})
        history = trim_history(history, MAX_HISTORY_TOKENS)

        messages = build_messages(history, system)
        resp = call_llm(messages)
        reply = parse_reply(resp)

        print(f"Bot: {reply}\n")
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
