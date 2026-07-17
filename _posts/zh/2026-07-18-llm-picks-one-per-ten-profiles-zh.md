---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM从每十个档案中选取一个
translated: true
type: note
---

已推送（`7029c8a`）。

新方案：

- 每次收集10个资料（必要时滚动屏幕）
- 将所有10份简介一次性发送给LLM
- LLM从每组中精准选出1个取消关注对象
- 遵循1/10比例，保守分配取消关注操作

LLM提示词现在要求返回 `{"index": <1-10>, "reason": "..."}` —— 它会比较全部10个资料的相对价值，选出单个最不值得保留的账号。这样可避免因孤立判断某用户价值临界而误取消关注。
