---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: SQL 代码库精通提示词指南
translated: true
type: note
---

以下是处理大型 SQL 代码库的一些有效 prompts：

## Understanding & Documentation

- "分析这段 SQL 代码并创建一个高层级的概述，说明它的功能，包括主要的数据流 (data flows)"
- "使用行内注释为该存储过程 (stored procedure) 的每个部分编写文档，解释其中的业务逻辑"
- "创建一个数据血缘 (data lineage) 图表，展示数据是如何流经这些存储过程的"
- "列出此代码中使用的所有 tables、views 和 temporary tables 及其用途"

## Analysis & Optimization

- "识别此 SQL 代码中潜在的性能瓶颈 (performance bottlenecks)"
- "找出任何可以合并的冗余查询或逻辑"
- "审查该代码是否存在 SQL injection 漏洞并提出修复建议"
- "分析优化这些查询所需的索引策略 (indexing strategy)"
- "指出任何应当更新的已过期 (deprecated) DB2 语法"

## Migration & Conversion

- "将此 DB2 存储过程转换为 PostgreSQL/MySQL/SQL Server 语法"
- "识别此代码中在迁移时需要寻找替代方案的 DB2 特定功能"
- "将这个大型的 monolithic procedure 拆分为更小的、模块化的组件"

## Debugging & Maintenance

- "找出代码中潜在的 null 处理问题"
- "识别应当添加错误处理 (error handling) 的位置"
- "定位任何应当参数化 (parameterized) 的硬编码值 (hardcoded values)"
- "检查事务管理 (transaction management) 问题或缺失的 commits/rollbacks"

## Specific Deep Dives

- "逐步解释第 450-520 行的逻辑"
- "如果此存储过程中出现 [特定条件]，会发生什么？"
- "当参数 X 的值为 Y 时，追踪其执行路径 (execution path)"

**Pro tips**: 将极长的 SQL 拆分为逻辑部分，提供有关业务目的的上下文，提前提及任何特定的疑虑，并提出后续问题以深入研究特定领域。
