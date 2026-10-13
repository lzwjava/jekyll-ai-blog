---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 阶段1完成：一个真正的小型数据库
translated: true
type: note
---

**第一阶段已完成并提交** —— 引擎从单表演示变成了一个真正的 mini-DB：

## 新增内容（v0.2）

| 功能 | 之前 | 现在 |
|---|---|---|
| **JOIN** | ✗ | INNER JOIN，支持对称的 `"on"` 列映射、限定的 `users.name` / `orders.total` 引用 |
| **聚合** | ✗ | count/sum/avg/min/max + `GROUP BY`（`{"op":"aggregate",...}`） |
| **WHERE 操作** | gt/gte/lt/lte/ne | + `IN`、`LIKE`（`%`/`_`）、`BETWEEN` |
| **ALTER TABLE** | ✗ | 添加/删除列（行重新建立键） |
| **DISTINCT** | ✗ | `select ... "distinct":true` |
| **批次** | 即发即忘（fire-and-forget） | `{"ops":[...]}` 现在是**原子性**的——任何失败的操作都会回滚之前的所有操作 |
| **LLM 上下文** | 无状态 | 系统提示词中的 6 轮（请求 → 计划）记忆，因此“and those older than 40”这类后续请求也能生效 |

测试从 22 个增加到 **49 项检查，全部通过**；编译器零警告。过程中还捕获了两个实际 bug（聚合双重释放、`on` 映射解析到错误侧）。

## 由离线演示验证（真实 LLM 路径相同）

```
create users / orders → insert 3 users → insert orders (id looked up by name)
name LIKE 'a%' → age BETWEEN 25..30 → count/sum per city → collapse
JOIN orders×users with WHERE total>50, ORDER BY → ALTER add email → atomic batch
```

## 建议的下一个里程碑

**第二阶段 — 内部机制**（我的首选）：有序主键**索引/B-tree**（当前瓶颈是全表扫描）、追加式 **WAL + 崩溃恢复** 取代整个文件重写，以及类似 MVCC 的读快照，使批处理内的 `SELECT` 看到稳定视图。

**第三阶段 — AI 层**：**流式**补全（SSE），让结果随 LLM 思考过程逐步出现；**`EXPLAIN` 风格的计划打印**（`> explain "show me users"` 会打印模型决定的 JSON 计划——非常适合演示和调试）；以及 **schema 幻觉防护**，在执行*之前*根据真实 schema 验证每个计划字段，并自动让模型重试一次。

**第四阶段 — 测试**：一个 sqllogictest 风格的（查询 → 预期行）语料库，每晚对引擎运行，外加一个 plan-JSON 模糊测试器。

如果希望它感觉像“真正的数据库”，下一步我会做第二阶段 → WAL；如果希望 AI 交互感觉最先进，就做第三阶段 → 流式。你对哪个方向感兴趣？