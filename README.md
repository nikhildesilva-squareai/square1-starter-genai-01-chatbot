# AI-Powered Chatbot — Square 1 AI starter

**Part of [Square 1 AI](https://square1-tutor.vercel.app) · Generative AI · Project 1.**

✅ **Data included.** The dataset is committed in [`dataset/`](dataset/) and is the **same standardized dataset every learner uses** — so results are comparable. It is 100% synthetic and Square 1-owned (no third-party or personal data). You can also download it as a single file from the project page on Square 1.

To run the commands below, copy the files into `data/` (`mkdir -p data && cp -r dataset/* data/`) or point the commands straight at `dataset/`.

MIT licensed — fork it, build on it, put it in your portfolio.

---

# AI-Powered Chatbot — starter

Starter for Square 1 AI **Generative AI · Project 1**. Build a streaming, multi-turn chatbot with a system-prompt persona, conversation memory, and token-budget trimming.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Get the material
The sample material lives on your project page (Resources): `system_prompts.json` (3 personas) and `eval_prompts.json` (15 eval turns). Put them in a `dataset/` folder next to `chat/` so `python -m chat.cli` can load a persona.

## Your task
Three tests define the contract — they run **offline** (no API key; the LLM is mocked) and fail until you implement the stubs in `chat/chat.py`:
```bash
pytest -q
```
Then wire `call_llm` to the Anthropic SDK and run the bot:
```bash
export ANTHROPIC_API_KEY=sk-ant-...      # Windows: set ANTHROPIC_API_KEY=...
python -m chat.cli
```
Pipeline: `build_messages` (system first + history in order) → `trim_history` (drop oldest turns past the budget; never the system prompt) → `call_llm` (Anthropic streaming) → `parse_reply` (text out, empty-safe). Append the reply back into history and loop.

**Model + key:** use a current id — `claude-sonnet-4-6` (default) or `claude-haiku-4-5-20251001` (cheaper). Read `ANTHROPIC_API_KEY` from the environment; **never hardcode it**. Never use a `claude-3-*` id. The 3 tests must keep passing with no key set.

Then run your bot against `eval_prompts.json` and write up how it did. Full brief, rubric, and references are on your Square 1 project page. MIT licensed.
