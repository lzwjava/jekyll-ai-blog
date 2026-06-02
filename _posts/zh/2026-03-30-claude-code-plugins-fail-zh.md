---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么 Claude Code 超级插件会失败
translated: true
type: note
---

Question: 为什么 Claude Code 的 Superpower plugin 有时会在任务中途卡住或停止，导致 LLM call 在执行过程中中断？

Answer: 问题：为什么 Claude Code 中的 Superpowers plugin 有时会在任务中途停止，导致 LLM call 中断？

Answer：

这是一个广为人知的痛点。发生这种情况有几个复合原因。

---

## 核心问题：多步骤 Pipeline 非常脆弱

Superpowers 工作流是一个**长链条的 LLM calls**：

```
Explore context → Ask questions → Propose approaches
    → Present design → Write design doc → Spec review
        → User reviews → Transition to implementation
```

每一个箭头都是一个**独立的 LLM call**。其中任何一个中断，整个链条就会停止。

---

## 原因 1：API Timeout

Claude Code 对 LLM calls 有一个已知的 2 分钟 Timeout 限制。复杂的 Superpowers 步骤（例如 "Propose 2-3 approaches"）涉及：

- 读取整个 project context
- 对多个 design options 进行推理
- 生成结构化的多部分 response

这很容易**超过 2 分钟**，导致无声的中断。

---

## 原因 2：SSE Stream 停滞（没有 Chunk 到达）

连接可能保持打开状态，但在中途停止交付 SSE chunks —— LLM stream 本身没有 idle timeout 或 chunk-activity watchdog。单个 tools 有自己的 timeout，但 LLM stream 没有。Stream-idle timeout 应该在每个收到的 chunk 上重置，而 total request timeout 则是一个独立的硬上限。

这就是为什么你会看到 spinner 在旋转但没有任何反应 —— 技术上连接是“活跃的”，但已经冻结了。

---

## 原因 3：Context Window 过载

Superpowers 会预先读取大量文件。如果你的项目规模很大：

- Context window 填满
- Model 在中断前显著变慢
- 或者 API 静默截断并失败

---

## 原因 4：MCP / Hook Timeouts 干扰 Session

MCP server 或 hook timeouts 可能会发送中断信号，导致 API response 连接断开，并被解释为中断。当配置了 7 个以上 MCP servers 时，这种情况尤其容易发生。

---

## 原因 5：Superpowers 本身是一个笨重的 Plugin

安装 Superpowers plugin 后，Claude Code 有时会变得完全没有响应 —— session-start hook 触发并可能冻结 session。即使没有完全冻结，session-start 的开销也增加了脆弱性。

---

## 中断时该怎么办

### 选项 1：从 Checkboxes 恢复

当 session 中断时如果任务已部分完成，Plan 中未勾选的 checkboxes 是下一个 session 知道从何处恢复的唯一方式。勾选它们是状态日志（state log），而不仅仅是形式。

只需告诉 Claude：**"Continue from where you left off — pick up at 'Propose approaches'"**

### 选项 2：将任务分解为较小的部分

不要让 Superpowers 一口气运行完整的 pipeline，而是手动触发每个阶段：

```
/brainstorming   ← 运行这个，等待它完成
然后
/execute-plan    ← 仅在 spec 完成后运行
```

### 选项 3：减轻 Context 负载

- 保持 `CLAUDE.md` 在 20K 字符以内
- 在进行长时间的 Superpowers session 之前禁用不使用的 MCP servers

### 选项 4：增加 Timeout 设置

```bash
# 为 session hooks 设置更高的 timeout
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=30000 claude
```

---

## 总结

LLM call 在 Superpowers 执行中途中断的原因包括：

| Cause | Likelihood |
|---|---|
| 2-minute API timeout | 非常常见 |
| SSE stream stalls silently | 常见 |
| Context window overload | 在大型项目中常见 |
| MCP hook interference | 如果配置了多个 MCP 则可能发生 |
| Plugin session-start overhead | 偶尔 |

**解决方法**是将 Superpowers 的每个阶段视为手动检查点（checkpoint） —— 不要指望整个 pipeline 能一次性不间断运行完成。

References:

- [Claude Code Timeout Issue #5615](https://github.com/anthropics/claude-code/issues/5615)
- [When Claude Goes Silent - API Timeouts](https://medium.com/@lgallard/when-claude-goes-silent-navigating-api-timeouts-and-model-selection-in-claude-code-aed23146b952)
- [Superpowers Plugin Overview](https://claude.com/plugins/superpowers)
- [The Superpowers Plugin Workflow Guide](https://www.builder.io/blog/claude-code-superpowers-plugin)
- [Subagent hang issue - opencode](https://github.com/anomalyco/opencode/issues/13841)
