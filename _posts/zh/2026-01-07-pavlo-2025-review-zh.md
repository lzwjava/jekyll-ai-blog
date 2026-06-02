---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: Andy Pavlo 2025年数据库年度回顾
translated: true
type: note
---

Question: Andy Pavlo 对 2025 年数据库进展的总结是什么？

Answer: Andy Pavlo 对 **2025** 年的总结（发布于 2026 年 1 月）将其描述为 **PostgreSQL** 巩固统治地位的一年，行业通过收购经历了大规模整合，且 AI 集成从“Vector 炒作”转向了标准化协议。

Pavlo 的核心观察包括：

### 1. “PostgreSQL 统治”时代

* **PostgreSQL v18:** 2025 年 11 月发布的第 18 版是一个重大里程碑。其最重要的更新是 **asynchronous I/O storage subsystem**，这使得该数据库终于得以摆脱长期以来对 OS page cache 的依赖。
* **功能对齐 (Feature Parity):** 增加了 **Skip Scan** 支持，允许查询在缺少前导键的情况下使用多键 B+Tree 索引——这是 Oracle 拥有数十年的一项功能，现在通过 Postgres 实现了“民主化”。
* **Cloud 标准化:** 随着 Microsoft 在 2025 年推出 **HorizonDB**，各大主流 Cloud provider (AWS, Google, Microsoft, Oracle) 现在都提供专门的高性能 PostgreSQL 服务。

### 2. AI 集成与 “Vibe Coding”

* **Model Context Protocol (MCP):** 如果说 2023–2024 年的主题是增加 Vector search，那么 2025 年则是关于 **MCP**。这个由 Anthropic 领导的协议成为了让 LLM 与数据库交互的标准，无需编写自定义的“胶水代码”。
* **Vibe Coding:** Pavlo 注意到 “vibe coding” 的兴起——即 LLM 生成大量的应用程序和数据库代码——正在从根本上改变开发者与数据系统的交互方式。
* **Database Auto-Tuning:** 他认为 self-driving databases 的未来是 LLM 处理高层上下文与专用算法处理底层 knob tuning 的混合体。

### 3. 重大的市场整合 (Market Consolidation)

这一年的特点是大规模的 “PostgreSQL 购物狂潮” 和其他备受瞩目的 M&A 活动：

* **Databricks:** 以 **10 亿美元**收购了 **Neon** (serverless Postgres)，并将其更名为 **Lakebase**。
* **Snowflake:** 以 **2.5 亿美元**收购了 **Crunchy Data**，以增强其自身的 Postgres 兼容产品。
* **IBM:** 以约 **30 亿美元**收购了 **DataStax**，以在 GenAI 数据层中获得更牢固的地位。
* **Salesforce:** 以 **80 亿美元**收购了 ETL 老牌公司 **Informatica**。

### 4. “Parquet 之战” (The Parquet Wars)

2025 年发布了五种新的开源文件格式，以挑战 Apache Parquet 在 Data Lake 中的霸主地位：

* **F3** (CMU + 清华大学): 使用 WebAssembly (Wasm) 直接在文件中嵌入解码器。
* **Vortex** (SpiralDB) 和 **FastLanes** (CWI)。
* **AnyBlox** 和 **Amudai** (Microsoft)。

### 5. 法律与行业动态

* **MongoDB vs. FerretDB:** 围绕 SSPL License 和开源兼容性产生了一场引人注目的法律纠纷。
* **数据库财富:** Pavlo 强调，由于 Oracle 股价飙升，**Larry Ellison** 在 2025 年成为了世界首富，这标志着数据库技术的“老牌劲旅”在财务上依然无可匹敌。

References:

* [Databases in 2025: A Year in Review // Andy Pavlo - CMU](https://www.cs.cmu.edu/~pavlo/blog/2026/01/2025-databases-retrospective.html)
* [2025 in Review with Mike Stonebraker and Andy Pavlo - DBOS](https://www.dbos.dev/webcast-2025-in-review-with-mike-stonebraker-and-andy-pavlo)
* [Data 2025: The Year in Review - Pigsty Blog (English Translation)](https://blog.vonng.com/en/db/db-year-review-2025/)

您是否希望我深入探讨 PostgreSQL v18 新存储子系统的技术细节或新的 F3 文件格式？
