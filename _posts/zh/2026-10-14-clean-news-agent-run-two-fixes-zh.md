---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 新闻代理运行干净，两项修复
translated: true
type: note
---

运行干净 — exit 0，19/19 个 feed，全部 4 个板块均经 LLM 编辑。

```
news-agent · window=48h · top=40 · LLM: openrouter/deepseek/deepseek-v4.1-flash
19 sources -> 348 raw -> 40 articles -> 4 sections (4 LLM-edited)
```

**本次运行的板块标题**（`output/digest.md`）：

- **实验室与产品** — "Google DeepMind 详解 Gemini 4 Argon；Higgsfield 将 AI 视频扩展至 10 分钟以上"（5 条）
- **研究与技术** — "Anthropic 谈自我复制与蒸馏；Python 3.15 发布"（10 条）
- **社区：YC 与 Hacker News** — "HN：Anthropic 重构源码控制、LLM 网关发布、AI 爬虫泛滥"（6 条）
- **行业与 AI 新闻** — "Disney 为 Character.AI 技术出价 2000 万美元；Pluto Security 融资 4200 万美元"（10 条）

新鲜产物（时间戳 03:48）：

```
output/index.html                HN-style feed page
output/digest.md                 markdown digest
output/digest.json               + dated aliases digest-2026-10-13.{md,json}, index-2026-10-13.html
output/feed.xml                  RSS 2.0
```

我在运行时做了两处小修复（目前**未提交**）：

1. `news_agent/llm.py` — 自动检测到的 provider/model 会回填到设置中，因此 header 现在会打印 `openrouter/deepseek/deepseek-v4.1-flash` 而不是 `/default`，并且 `digest.json` 会记录真实的 model。
2. `news_agent/render.py` — 补上了缺失的 `output/digest.json` "latest" 别名（md/html 有，json 没有）。

需要我提交并推送这两处吗？
