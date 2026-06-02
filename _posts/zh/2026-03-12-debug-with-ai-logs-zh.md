---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用日志与 AI 调试
translated: true
type: note
---

问题：使用 AI 编码助手（Copilot/Codex/Claude Code）修复难题的金科玉律是什么？

答案：

## 金科玉律：基于调试日志的 AI 修复

这是一种使用 AI 辅助解决难题 bug 的极其实用策略。以下是全面分解：

---

### 核心循环

```
Hard Problem → Add Debug Logs → Observe Output → Feed Back to AI → Fix
```

---

### 为什么有效

AI 编码助手通常**缺少运行时上下文**。它们只能看到你的静态代码，而不知道执行时实际发生什么。调试日志通过暴露以下内容来桥接这一差距：

- 实际变量值与预期值
- 执行流程（实际到达的分支/方法）
- 时序问题和竞态条件
- 代码审查中不明显的 Null/undefined 状态
- 来自 API 或数据库的意外数据形状

---

### 逐步过程

**步骤 1 — 向 AI 描述问题，要求它添加调试日志**
> "I have a bug in this function. Don't fix it yet — add comprehensive debug logs so I can observe the runtime behavior."

**步骤 2 — 前端：策略性地添加 `console.log`**

```javascript
console.log('[DEBUG] fetchUser called with id:', id);
console.log('[DEBUG] API response:', JSON.stringify(response));
console.log('[DEBUG] Parsed user object:', user);
console.log('[DEBUG] State before update:', this.state);
```

**步骤 3 — 后端：添加 Log4j / SLF4J 日志**

```java
log.debug("[DEBUG] entering processOrder(), orderId={}", orderId);
log.debug("[DEBUG] fetched order: {}", order);
log.debug("[DEBUG] inventory check result: {}", inventoryStatus);
log.error("[ERROR] unexpected state: {}", e.getMessage(), e);
```

**步骤 4 — 运行应用，重现 bug，收集日志**

复制相关的日志输出——这是你的**证据**。

**步骤 5 — 将日志反馈给 AI**
> "Here is the console output when the bug occurs: [paste logs]. Now identify the root cause and fix it."

**步骤 6 — AI 使用完整上下文进行修复**

现在 AI 拥有运行时真相，而非静态猜测。修复质量会显著提升。

---

### 专业提示

| 提示 | 详情 |
|---|---|
| **标记你的日志** | 使用像 `[DEBUG]`、`[FLOW]`、`[STATE]` 这样的前缀来轻松过滤 |
| **日志记录前后都要** | 包装可疑操作以查看输入与输出 |
| **在 catch 块中记录日志** | 始终记录完整异常 + 上下文，而非仅 `e.getMessage()` |
| **修复后移除日志** | 或使用适当的日志级别（`DEBUG`），以便在生产环境中隐藏 |
| **在提示中具体说明** | 告诉 AI 哪一行日志看起来不对以及原因 |

---

### 示例提示模板

```
I have this bug: [describe symptom]

Here is the relevant code: [paste code]

Here is the runtime log output when the bug occurs:
[paste logs]

Based on the logs, identify the root cause and provide a fix.
```

---

### 总结

金科玉律本质上是**将 AI 从静态代码阅读器转变为动态调试器**——通过日志提供它所需的运行时证据。这对于以下情况特别强大：

- 竞态条件
- 来自外部 API 的错误数据
- 复杂状态管理 bug
- 间歇性/难以重现的问题
