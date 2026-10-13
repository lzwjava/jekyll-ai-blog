---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 第三个里程碑：索引，验证器，EXPLAIN
translated: true
type: note
---

**第三个里程碑已完成。** 路线图的剩余事项已经完成——数据库现在有了真正的索引结构、生产级的计划验证和执行透明性：

## 1. 主键 B+ tree 索引（`btree.c`）

一个真正的内存态 B+ tree（order-64, copy-up leaf splits），用作惰性主键索引缓存：

- **插入操作增量维护它** —— 重复主键检查、自增和 `where: {"id": N}` 探测均为 O(log n)
- 更新/删除会将其标记为脏；下次查找时惰性重建（正确性从不依赖于此）
- 在此过程中发现并修复了 **三个真实的 B+ bug** —— 内部分裂时的子节点计数（越界读）、分裂后下降转向，以及一个导致键重复的 shift-scan 替换

**基准测试证明了这一点**（`make benchmarks`，50k 行）：

```
insert 50000 rows : 9654 ms   (pk-conflict via B+, 1 rebuild total)
pk select 50000   :  106 ms   (2.12 us/lookup, B+ tree)
full scan ×100    : 2909 ms   (29 ms per scan)
```

→ 索引查找比扫描快 **约 14,000 倍**，并且在 50k 次增量插入中，该树仅重建了一次。

## 2. Schema 验证器 + LLM 自我重试

`db_validate_plan` 以非破坏性方式针对实时 schema（表、`values`、`columns`、`order_by`、`group_by`、嵌套 `and`/`or`、join `on` 映射）检查每个计划。在真实 LLM 路径上，被拒绝的计划会**连同准确错误信息被送回模型一次**——这是防幻觉保护——然后才以清晰的 `PLAN ERROR` 放弃。

## 3. EXPLAIN（AI 决策内容）

```
isql> explain list anyone over 25;
[plan] {"op":"select","table":"users","columns":"*","where":{"age":{"gt":25}}}
[cost] select: scans/joins 3 row(s), pk index: no (full scan)
execute? [y/N]
```

`ISQL_EXPLAIN=1` 会为每条语句打印计划和代价（非常适合演示）。

## 状态：92 项检查通过（83 项引擎 + 9 项 B+ tree），崩溃恢复完好，0 警告

```
423a5f9  isql: AI-driven minimal database  (LLM parses SQL, C executes)
fd4fd7a  Phase 1: JOIN, aggregate, ALTER, IN/LIKE/BETWEEN, DISTINCT, atomic batches, multi-turn memory
fb9fc97  june: WAL crash-recovery + interactive BEGIN/COMMIT/ROLLBACK
10ccd59  julius: B+ pk index, validator + LLM retry, EXPLAIN
```

**剩余可做的事：** streaming completions (SSE)、一套正式的 `sqllogictest` 风格语料库、一个针对 plan/JSON 层的 fuzz harness。要我继续推进这些，还是就此打住？
