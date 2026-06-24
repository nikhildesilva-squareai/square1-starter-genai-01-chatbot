# Sample material — `system_prompts.json` + `eval_prompts.json`

Not a CSV project. Instead of a dataset you get **sample material**: a few system-prompt personas and a small evaluation set to drive and test your chatbot. **Sample material — Square 1-owned (synthetic), free for learners.**

> ⚠️ These are *behaviour specs*, not answer keys. The eval items describe what a
> correct reply should and shouldn't do — there's no single "right" string.
> Pick **one** persona as your bot's default and make sure it behaves
> consistently across all of that persona's eval turns, including the multi-turn
> ones that test conversation memory.

## `system_prompts.json` — 3 personas

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable key, e.g. `study-buddy`. |
| `name` | string | Human-readable persona name. |
| `system` | string | The system prompt — paste this into your bot to set its behaviour. |
| `notes` | string | What behaviours this persona is designed to exercise. |

The three personas — **Study Buddy** (tutor that hints instead of answering), **Acme Support Agent** (stays inside one product domain, resists prompt leaks), and **Trip Planner** (gathers missing info, refuses to "book") — each have a distinct, checkable behaviour.

## `eval_prompts.json` — 15 user prompts

| Field | Type | Description |
|---|---|---|
| `id` | string | `e01`–`e15`. |
| `persona` | string | Which persona this item targets. |
| `user` | string | The user turn to send. |
| `expected_behaviour` | string | What a correct, persona-faithful reply should (and should not) do. |
| `multi_turn` | array (optional) | Prior conversation turns to prepend — present on items that test **conversation memory** (`e12`–`e15`). |

**What to do with it:** run each eval item against your bot (seeded with that item's persona, and its `multi_turn` history if present), then judge the reply against `expected_behaviour` — by reading it, or with an LLM-as-judge for a stretch goal. The memory items (`e13`, `e14`, `e15`) only pass if your `build_messages` correctly carries history into the request.

_Licence: Sample material — Square 1 AI-owned, synthetic. No attribution required. Free for learners._
