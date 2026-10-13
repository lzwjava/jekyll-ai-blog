---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 已验证的端到端新闻智能体
translated: true
type: note
---

已端到端构建并验证。以下是 `/home/lzw/projects/news-agent` 中的内容：

```text
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

**Graph** (`uv run news-agent graph`):

```text
START → select_sources ─Send→ fetch            (one parallel branch per feed)
          fetch* → normalize → rank → build_sections
          build_sections ─Send→ summarize_section  (one LLM editor per section)
                      └──────→ compile_digest      (LLM-off path)
          compile_digest → render → END
```

用到的 LangGraph 特性：`TypedDict` 状态与 `Annotated[list, operator.add]` reducer，使两个动态 `Send` 扇出能安全合并；`add_conditional_edges(..., [targets])` 进行连接；`MemorySaver` 检查点（每次运行都会打印一个 `thread-id`，`--thread-id` 可恢复）；以及故障隔离——一个失效的 feed 或失败的 LLM 调用只会写入 `errors`。

**验证运行：** 19/19 个源抓取成功 → 348 条原始 → 40 条排名 → 4 个 section，全部经过 LLM 编辑 → `output/index.html`、`digest.md`、`digest.json`、`feed.xml`。

值得了解的细节：

- **Anthropic 不发布 RSS**，因此 `anthropic-news` / `anthropic-research` 使用 `type: html` 适配器（CSS 选择器 + `link_pattern`/`link_exclude`）——这就是 `/research/team/*` 这类导航链接被过滤掉的方式。
- **HN 对类似浏览器的 UA 返回 419**，**VentureBeat 对非浏览器 UA 返回 429** —— 通过一个简单的默认 UA + 每个源的 `user_agent` 覆盖，以及对 419/429/5xx 的重试/退避（backoff）修复。
- **LLM**：OpenRouter 的 `openai/gpt-4o-mini` 和 `gemini-2.5-flash` 在你的 key 上返回 403，所以默认是 `deepseek/deepseek-v4.1-flash`（可用；`--provider deepseek` 也可用）。结构化输出带有 JSON-schema 重试，文章以整数索引的形式传给模型，因此它无法编造链接。
- 排名是 **按 section 平衡（section-balanced）**（为每个类别保留名额），这样实验室不会挤掉媒体，另外还有 URL + 近似重复标题去重，以及 48 小时窗口。

```bash
uv run news-agent                 # full run
uv run news-agent run --no-llm    # heuristic digest, no key needed
uv run news-agent run --only openai,anthropic-news --hours 24
```

目前还没有任何提交——你说一声，我就创建提交。