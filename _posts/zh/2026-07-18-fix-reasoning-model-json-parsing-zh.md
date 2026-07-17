---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复推理模型JSON解析
translated: true
type: note
---

修复并推送 (`7afc39b`)。

两个问题：

1. `max_tokens=100` 设置过小 — `deepseek/deepseek-v4-flash` 是一个推理模型，因此它将全部 100 个 token 用于内部推理（finish_reason=length），从未生成可见输出。已调整为 2000。
2. 当模型将 JSON 包裹在 markdown 代码块或推理文本中时，`json.loads(response)` 会失败。现在改用正则表达式从响应中提取 `{...}` 形式的 JSON 对象。

再次尝试 `ww x unfollow` — `llm_error` 的情况应该已经消除。
