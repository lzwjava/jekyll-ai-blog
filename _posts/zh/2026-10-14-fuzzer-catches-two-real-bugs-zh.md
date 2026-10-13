---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模糊测试工具捕获两个真实错误
translated: true
type: note
---

**最终里程碑已交付并提交。** 本轮共有四个提交——streaming、golden corpus、fuzzer——而 fuzzer 立刻通过捕获两个真实 bug 证明了自身价值。

## 1. Streaming (SSE)

- `llm_sse.c` — 独立、可测试的 SSE 解析器（覆盖 8 个单元检查：分块边界/行中拆分）
- 计划现在**在模型生成时流式输出到终端**（`ISQL_STREAM=0` 可禁用）；忽略 `stream:` 的服务器/代理会优雅降级为普通 JSON 解析
- `mock_llm.py` 提供 SSE 模式，用于端到端测试

## 2. sqllogictest corpus

`tests/corpus.logic` — 25 个自然语言用例，每个都配有对应的黄金计划（记录 LLM 输出），并按预期对引擎执行。它既是回归保护网，也是 prompt 示例来源。`make corpus` → **25/25 通过**。

## 3. Fuzz harness——以及它捕获的 bug

`./fuzz 1000000 [seed]` 对三个目标进行高强度测试：向 `json_parse` 输入对抗性字节流（深嵌套高达 200k、截断、转义）、随机引擎计划（包括批处理和嵌套的 `and/or` where 子句）、以及序列化器往返。**跨 3 个种子执行 200 万次迭代：零崩溃、零违规**——并且在种子 42 的第 67 次迭代时：

- **Bug 1（往返）**：`json_to_string` 在 `realloc` 增长后从未终止其缓冲区——跨越 64 字节边界的值返回的字符串带有**未初始化的垃圾尾部**（神秘的输出中 `20753`）。我们曾序列化的每个大型 JSON 都受到轻微污染；只有 fuzzer 能发现它。
- **Bug 2（语料库测试工具）**：`snprintf(val, "\"%s\"", val)` 使 src/dst 重叠，导致每个种子字符串的第一个字符丢失（`alice` → `lice`）。

同时进行了加固：解析器中加入了**嵌套深度保护（400）**，防止幻觉产生的深层计划使栈溢出；引擎现在会拒绝 `WHERE` 中的未知列（与 SQLite 保持一致）。

## 完整项目状态

```
make test       100 unit checks (83 engine + 9 B+tree + 8 SSE) — 0 failures
make corpus      25 golden-logic checks — 0 failures
make fuzz        2M iterations / 3 seeds — clean
crash_recovery   kill -9 → all committed data survives
```

提交：`Phase 1`（SQL 功能）→ `june`（WAL + 事务）→ `julius`（B+ 索引、验证器、EXPLAIN）→ `august`（streaming、corpus、fuzzing）。

这个项目画了一个完整的圆：AI 驱动一个真正的 C 数据库——schema 感知的计划生成 → 带一次自我修正的验证 → 索引化/流式/事务化执行 → 崩溃安全持久化——而这一切由一个测试金字塔维系，它现在确实能*捕获* bug。如果将来恢复工作，自然的下一步是：从真实 LLM 运行中生成 `sqllogictest` 语料库（用于提示调优的黄金计划），或者将重试循环精简为合适的 few-shot 对话。
