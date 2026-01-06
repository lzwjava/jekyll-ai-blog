---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-flash-preview
title: Andy Pavlo 2025 Database Year Review
translated: false
type: note
---

Question: What is Andy Pavlo's summary of database progress for 2025?

Answer: Andy Pavlo’s summary for **2025** (published in January 2026) characterizes it as the year **PostgreSQL** cemented its dominance, the industry saw massive consolidation through acquisitions, and AI integration shifted from "vector hype" to standardized protocols.

Pavlo's key observations include:

### 1. The Era of "PostgreSQL Dominance"

* **PostgreSQL v18:** The release of version 18 in November 2025 was a major milestone. Its most significant update was the **asynchronous I/O storage subsystem**, which finally allows the database to move away from its long-standing reliance on the OS page cache.
* **Feature Parity:** It added **Skip Scan** support, allowing queries to use multi-key B+Tree indexes even if the leading keys are missing—a feature Oracle has had for decades but is now "democratized" via Postgres.
* **Cloud Standardization:** With Microsoft launching **HorizonDB** in 2025, every major cloud provider (AWS, Google, Microsoft, Oracle) now offers a specialized, high-performance PostgreSQL service.

### 2. AI Integration & "Vibe Coding"

* **Model Context Protocol (MCP):** If 2023–2024 was about adding vector search, 2025 was about **MCP**. This Anthropic-led protocol became the standard for letting LLMs interact with databases without custom "glue code."
* **Vibe Coding:** Pavlo noted the rise of "vibe coding"—where LLMs generate large swaths of application and database code—is fundamentally changing how developers interact with data systems.
* **Database Auto-Tuning:** He argues that the future of self-driving databases is a hybrid of LLMs for high-level context and specialized algorithms for low-level knob tuning.

### 3. Major Market Consolidation

The year was defined by a massive "PostgreSQL shopping spree" and other high-profile M&A activity:

* **Databricks:** Acquired **Neon** (serverless Postgres) for **$1 billion**, rebranding it as **Lakebase**.
* **Snowflake:** Acquired **Crunchy Data** for **$250 million** to bolster its own Postgres-compatible offerings.
* **IBM:** Bought **DataStax** for approximately **$3 billion** to secure a stronger foothold in the GenAI data layer.
* **Salesforce:** Acquired the ETL veteran **Informatica** for **$8 billion**.

### 4. The "Parquet Wars"

Five new open-source file formats were released in 2025 to challenge Apache Parquet's supremacy in data lakes:

* **F3** (CMU + Tsinghua): Uses WebAssembly (Wasm) to embed decoders directly in the file.
* **Vortex** (SpiralDB) and **FastLanes** (CWI).
* **AnyBlox** and **Amudai** (Microsoft).

### 5. Legal & Industry Shifts

* **MongoDB vs. FerretDB:** A notable legal dispute arose regarding the SSPL license and open-source compatibility.
* **The Wealth of Databases:** Pavlo highlighted that **Larry Ellison** became the world's richest person in 2025 due to Oracle's surging stock, signaling that the "old guard" of database technology is still financially unparalleled.

References:

* [Databases in 2025: A Year in Review // Andy Pavlo - CMU](https://www.cs.cmu.edu/~pavlo/blog/2026/01/2025-databases-retrospective.html)
* [2025 in Review with Mike Stonebraker and Andy Pavlo - DBOS](https://www.dbos.dev/webcast-2025-in-review-with-mike-stonebraker-and-andy-pavlo)
* [Data 2025: The Year in Review - Pigsty Blog (English Translation)](https://blog.vonng.com/en/db/db-year-review-2025/)

Would you like me to dive deeper into the technical specifics of PostgreSQL v18's new storage subsystem or the new F3 file format?