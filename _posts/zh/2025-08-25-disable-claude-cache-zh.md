---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Claude代码中禁用缓存
translated: true
type: note
---

在 **Claude Code** 中，这段代码片段

```json
"cache_control": {
  "type": "ephemeral"
}
```

意味着模型生成的响应（或产物）**不会被缓存以供重复使用**。

### 存在意义

通常情况下，Claude Code（及其他 Anthropic SDK）可能会缓存响应以加速后续相同提示的处理。但当你设置 `"cache_control": { "type": "ephemeral" }` 时，你是在告知 API：

* **不要将此结果持久化到缓存中**
* 如果后续出现完全相同的请求，**不要重复使用该响应**
* 将响应视为**短暂存在**——仅限本次调用有效

### 使用场景

这在以下情况下特别有用：

* 请求包含**敏感或个人数据**，不希望被缓存
* 发送的是**一次性查询**，无需重复利用
* 希望每次都能获得**全新输出**，即使请求文本完全相同

简而言之，`"ephemeral"` 使 Claude 的输出成为*瞬时性*的——仅在此次交互中有效，不会在多次调用间进行缓存。

需要我进一步解释这与 Claude Code 中默认 `cache_control` 行为的区别吗（例如 `type: "default"`、`"none"` 与 `"ephemeral"` 的差异）？
