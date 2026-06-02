---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Memory Layers and Caching Efficiency
translated: false
type: note
---

Here's a deep dive into how memory works in Hermes, and how it balances efficiency vs effectiveness.

---

## Architecture: Three Layers of Memory

Hermes has a layered memory system, each serving a different persistence/retrieval tradeoff:

### Layer 1: Curated Memory (MEMORY.md + USER.md)

The core system. Two flat files in `~/.hermes/memories/`:

- **MEMORY.md** — agent's personal notes (environment facts, project conventions, tool quirks)
- **USER.md** — user profile (preferences, communication style, role, habits)

**How it works:**

1. At session start, `MemoryStore.load_from_disk()` reads both files, splits on `\n§\n` delimiter, and captures a **frozen snapshot** into `_system_prompt_snapshot`.
2. This snapshot is injected directly into the system prompt as a bounded block (MEMORY: 2200 chars, USER: 1375 chars). You can see it in your own system prompt — the `MEMORY (your personal notes)` and `USER PROFILE (who the user is)` sections.
3. Mid-session writes (via the `memory` tool) update the files on disk immediately, but do **NOT** mutate the system prompt. This is the **frozen snapshot pattern** — it keeps the prefix cache stable for the entire session. The snapshot only refreshes on next session start.

**Why this design?** Prefix caching. If memory mutated the system prompt mid-session, every subsequent API call would miss the cache. By freezing the snapshot, the system prompt is byte-identical across all turns → massive cost savings on providers that support prompt caching (Anthropic, OpenAI).

**Write safety:** Atomic temp-file + `os.replace()` + file locking (`fcntl.LOCK_EX`). Concurrent sessions can write without corrupting the file.

**Injection/exfiltration scanning:** Every write goes through `_scan_memory_content()` — regex patterns catch prompt injection attempts (`ignore previous instructions`, `you are now`, curl with `$KEY`, etc.) and invisible unicode characters. Since memory is injected into the system prompt, a poisoned memory entry is a direct injection vector.

### Layer 2: External Memory Providers (Plugin System)

One external provider can be active at a time, set via `memory.provider` in config.yaml. Available providers:

| Provider | Type | Retrieval |
|----------|------|-----------|
| **Honcho** | Cloud-hosted, dialectic Q&A | Semantic search + LLM reasoning + peer cards |
| **Holographic** | Local SQLite + HRR vectors | Entity resolution, trust scoring, compositional queries |
| **Mem0** | Cloud-hosted | Semantic search |
| **Supermemory** | Cloud-hosted | Semantic search |
| **Hindsight** | Cloud-hosted | Semantic search |
| **RetainDB** | Cloud-hosted | Semantic search |

**The MemoryProvider ABC** (`agent/memory_provider.py`) defines the lifecycle:

```
initialize()          → connect, create resources, warm up
system_prompt_block() → static text for system prompt (instructions, status)
prefetch(query)       → background recall before each turn
sync_turn(user, asst) → async write after each turn
get_tool_schemas()    → extra tools to expose (e.g. fact_store, honcho_search)
handle_tool_call()    → dispatch tool calls
shutdown()            → clean exit
```

**Honcho is the most sophisticated.** It has three recall modes:
- `context` — prefetch peer context (summary, representation, peer card) into system prompt
- `tools` — expose honcho_search/honcho_reasoning/honcho_profile as tools, agent decides when to query
- `hybrid` — both (default)

Honcho also does **dialectic Q&A** — it runs its own LLM reasoning over accumulated observations to synthesize user understanding. With `dialecticCadence` and `dialecticDepth` config, you control how often and how deep this runs (cost vs freshness tradeoff).

### Layer 3: Session Search (FTS5)

`session_search` tool — not memory per se, but the primary way to recall transient information. Backed by SQLite FTS5 with both `unicode61` tokenizer (word-level) and `trigram` tokenizer (CJK substring support). Searches across ALL past sessions' messages.

This is the **efficiency lever** — instead of stuffing everything into memory, the agent is instructed to use `session_search` for task progress, session outcomes, and completed work logs. Memory is reserved for durable facts that will still matter in weeks.

---

## How to Ask the Agent to Remember Something

Three approaches:

1. **Direct request:** Say "remember this" or "don't do that again" — the agent's system prompt instructs it to proactively save via the `memory` tool when it detects these signals.

2. **Background review:** After every turn, `spawn_background_review()` can fire a daemon thread that forks the agent, replays the conversation, and asks "should anything be saved?" This runs with a tool whitelist limited to `memory` and `skills` tools. Writes go straight to disk; the main conversation is never touched.

3. **Manual memory tool:** The agent can call `memory(action="add", target="user", content="...")` or `memory(action="add", target="memory", content="...")` at any time. The tool enforces char limits and deduplication.

**What goes where:**
- `target="user"` → WHO the user is (preferences, role, style) — 1375 char limit
- `target="memory"` → WHAT the agent learned (environment facts, conventions, quirks) — 2200 char limit

---

## Efficiency vs Effectiveness: The Balancing Mechanisms

### 1. Bounded char limits (not token limits)

Memory uses **character counts**, not tokens. This is model-independent — 2200 chars is ~550 tokens regardless of tokenizer. When you hit the limit, you must replace or remove entries. This forces curation: every entry must earn its place.

### 2. Frozen snapshot + prefix cache

The system prompt is stable across all turns. Memory writes update disk but not the prompt. This means:
- Zero cache invalidation cost per turn
- Memory is "eventually consistent" — fresh entries appear next session

### 3. Prefetch pattern (external providers)

External providers implement `prefetch(query)` — called before each API call. The key design rule: **implementations should be fast — use background threads for the actual recall and return cached results here.**

Honcho implements this with:
- `queue_prefetch(query)` after each turn → fires a background thread
- `prefetch(query)` on next turn → returns the cached result (non-blocking)
- `context_cadence` — minimum turns between context API calls (default 1)
- `dialectic_cadence` — minimum turns between expensive LLM reasoning calls

### 4. Three-tier recall strategy

The system prompt explicitly instructs the agent:

```
- Memory (MEMORY.md/USER.md): ALWAYS injected, every turn, zero cost
- External provider prefetch: injected if available, cadence-gated
- session_search: on-demand, only when the agent needs to recall past conversations
```

This creates a natural efficiency hierarchy:
- **Hot path:** Curated memory in system prompt (free, always present)
- **Warm path:** Provider prefetch (cached, cadence-gated)
- **Cold path:** session_search (FTS5 query, only when needed)

### 5. Memory vs Skills separation

The system prompt draws a sharp line:
- **Memory** = who the user is, environment facts, stable conventions
- **Skills** = how to do things, procedural knowledge, workflows

If you discover a new way to do something, it goes in a skill (SKILL.md), not memory. Skills are loaded on-demand via `skill_view()`, not injected every turn. This prevents memory from growing into a catch-all dump.

### 6. Security: injection scanning

Since memory is injected into the system prompt, every write is scanned for:
- Prompt injection patterns (`ignore previous instructions`, role hijacking)
- Exfiltration attempts (curl with `$KEY`, reading `.env`)
- Invisible unicode characters
- SSH backdoor patterns

---

## OpenClaw → Hermes

OpenClaw was the predecessor. The migration skill (`hermes claw migrate`) imports MEMORY.md, USER.md, SOUL.md, and command allowlists from `~/.openclaw/` into `~/.hermes/`. The memory format is the same (`§`-delimited entries), so the migration is mostly mechanical.

---

**TL;DR:** Hermes memory is a curated, bounded, file-backed store injected as a frozen system prompt snapshot (preserving prefix cache). External providers add semantic recall with cadence-gated prefetch. Session search handles transient recall. The agent is instructed to be selective — memory is for durable facts, session_search is for everything else.
