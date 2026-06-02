---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Li Auto's GreptimeDB Deployment Scope
translated: false
type: note
---

Question: Do all Li Auto cars use GreptimeDB?

Answer:

No, not every Li Auto car uses GreptimeDB.

Li Auto (Li Xiang) has been collaborating with Greptime since 2023 and has deployed GreptimeDB in some of their intelligent driving and cockpit data systems, especially in newer models (L-series and MEGA) for time-series data storage and real-time analytics. GreptimeDB is used primarily in Li Auto’s cloud-side data platform and some vehicle-side telemetry scenarios.

However:

- Older models (Li Auto ONE, L9/L8/L7 launched before mid-2023) do not use GreptimeDB, as the partnership and large-scale deployment started later.
- Even in newer models, GreptimeDB is mainly used for specific time-series workloads (ADAS data, cockpit telemetry, etc.), not as the only or universal database across all systems in the car.
- Many other databases and storage systems (Redis, MySQL, ClickHouse, etc.) are still used in parallel depending on the use case.

So while GreptimeDB has become an important part of Li Auto’s data infrastructure and is deployed in their latest vehicles, it is not used in every Li Auto car ever produced.

References:

- Greptime official blog (2024): “GreptimeDB Powers Li Auto Intelligent Driving Data Platform”
- Li Auto & Greptime joint speech at ApacheCon Asia 2024
- GreptimeDB GitHub case studies and Li Auto engineering sharing sessions (2023–2025)
