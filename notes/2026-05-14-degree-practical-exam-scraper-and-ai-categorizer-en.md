---
audio: false
generated: true
image: false
lang: en
layout: post
title: Degree Practical Exam Scraper and AI Categorizer
translated: false
type: note
---

The command works end-to-end. Here's what was added and a real run of `ww degree practical --pages 2` against the live site:

**Added:**

- `ww/degree/degree.py` — scraper + AI analyzer
- Registered `degree` in `ww/main.py` with help text

**Usage:**

- `ww degree` — AI-categorized overview (newest page, ~20 entries)
- `ww degree practical` — filter for 实践考核 / scores articles
- `ww degree list` — raw scraped list, no AI
- `--pages N` — fetch up to 11 pages (203 total entries)
- `--model <name>` — override OpenRouter model

**Practical-exam articles you should care about (from `ww degree practical --pages 2`):**

- [2026-04-20] [关于查询2026年4月25-26日自考实践考核考场座位号的通知](https://jxjy.gdufs.edu.cn/info/1178/19297.htm) — Seat numbers for your April 2026 practical exam.
- [2025-12-19] [广东外语外贸大学2026年上半年实践考核报考通知-面向社会考生](https://jxjy.gdufs.edu.cn/info/1178/18914.htm) — 2026 H1 practical-exam registration notice.
- [2025-12-10] [关于推迟2026年上半年实践考核报考时间的通知](https://jxjy.gdufs.edu.cn/info/1178/18899.htm) — Postponement of 2026 H1 registration time.
- [2025-12-02] [关于发布自学考试实践考核课程考试大纲的通知](https://jxjy.gdufs.edu.cn/info/1178/18890.htm) — Practical-exam syllabi.
- [2025-11-21] [关于公布2025年11月自学考试实践考核成绩的通知](https://jxjy.gdufs.edu.cn/info/1178/18879.htm) — Nov 2025 practical-exam scores release.
- [2025-10-24] [关于查询2025年11月1-2日自考实践考核考场座位号的通知](https://jxjy.gdufs.edu.cn/info/1178/18846.htm) — Nov 2025 seat numbers.
- [2025-05-19] [关于公布2025年4月自学考试实践考核成绩的通知](https://jxjy.gdufs.edu.cn/info/1178/18678.htm) — April 2025 practical-exam scores.
- [2025-04-08] [关于公布2025年4月19-20日自考实践考核考场座位号的通知](https://jxjy.gdufs.edu.cn/info/1178/18617.htm) — April 2025 seat numbers.

The recurring categories are: **registration (报考)**, **seat numbers (座位号)**, **scores (成绩)**, and **syllabi (大纲)** — those four phrases are what the AI is keying on, so any new notice with them will surface automatically.
