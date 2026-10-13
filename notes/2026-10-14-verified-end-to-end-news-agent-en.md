---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verified End-to-End News Agent
translated: false
type: note
---

Built and verified end-to-end. Here's what's in `/home/lzw/projects/news-agent`:

```
pyproject.toml        uv project + `news-agent` entry point
sources.yaml          19-source registry (YC, HN, OpenAI, Anthropic, DeepMind,
                      Mistral, HF, Latent Space, Simon Willison, TechCrunch,
                      Verge, Ars, MIT TR, IEEE, VentureBeat, ...)
news_agent/
  config.py           Settings + registry loading
  models.py           SourceConfig / Article / SectionDraft (pydantic)
  state.py            AgentState — LangGraph channels + reducers
  sources.py          RSS/Atom adapter + HTML scraper adapter, dedupe keys, retries
  llm.py              provider factory (openrouter/deepseek/openai/custom), degrades to None
  nodes.py            the 8 node functions + 2 Send routers
  graph.py            StateGraph assembly
  render.py           HN-style HTML, markdown, JSON, RSS writers
  cli.py              run / sources / graph subcommands
README.md .env.example output/ (gitignored)
```

**The graph** (`uv run news-agent graph`):

```
START → select_sources ─Send→ fetch            (one parallel branch per feed)
          fetch* → normalize → rank → build_sections
          build_sections ─Send→ summarize_section  (one LLM editor per section)
                      └──────→ compile_digest      (LLM-off path)
          compile_digest → render → END
```

LangGraph specifics used: `TypedDict` state with `Annotated[list, operator.add]` reducers so the two dynamic `Send` fan-outs merge safely, `add_conditional_edges(..., [targets])` joins, a `MemorySaver` checkpointer (every run prints a `thread-id`, `--thread-id` resumes), and fault isolation — a dead feed or failed LLM call only writes to `errors`.

**Verified run:** 19/19 sources fetched → 348 raw → 40 ranked → 4 sections, all LLM-edited → `output/index.html`, `digest.md`, `digest.json`, `feed.xml`.

Details worth knowing:

- **Anthropic publishes no RSS**, so `anthropic-news` / `anthropic-research` use the `type: html` adapter (CSS selectors + `link_pattern`/`link_exclude`) — that's how nav links like `/research/team/*` get filtered out.
- **HN returns 419 for browser-like UAs** and **VentureBeat 429s non-browser UAs** — fixed with a simple default UA + per-source `user_agent` override and retry/backoff on 419/429/5xx.
- **LLM**: OpenRouter's `openai/gpt-4o-mini` and `gemini-2.5-flash` return 403 on your key, so the default is `deepseek/deepseek-v4.1-flash` (works; `--provider deepseek` also works). Structured output with a JSON-schema retry, and articles travel to the model as integer indexes so it can't invent links.
- Ranking is **section-balanced** (reserves slots per category) so labs can't crowd out the press, plus URL + near-duplicate title dedupe and a 48h window.

```bash
uv run news-agent                 # full run
uv run news-agent run --no-llm    # heuristic digest, no key needed
uv run news-agent run --only openai,anthropic-news --hours 24
```

Nothing is committed yet — say the word and I'll make a commit.
