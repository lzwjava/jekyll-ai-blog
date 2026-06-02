---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: OpenTelemetry Overview and Key Points
translated: false
type: note
---

Question: What is OpenTelemetry?

Answer:

OpenTelemetry (often abbreviated as **OTel**) is a set of open-source tools, APIs, SDKs, and specifications designed to create and manage telemetry data (metrics, logs, and traces) from applications and infrastructure in a vendor-neutral, standardized way.

### Key Points
- **Part of the Cloud Native Computing Foundation (CNCF)**: It’s the second-highest project by activity there (after Kubernetes).
- **Merger of OpenTracing and OpenCensus**: In 2019, the two earlier open-source tracing projects (OpenTracing and OpenCensus) combined to form OpenTelemetry to end fragmentation.
- **Fully vendor-agnostic**: Unlike older standards that were tied to specific vendors (e.g., Jaeger, Zipkin), OpenTelemetry lets you instrument your code once and send the data to any compatible backend (Datadog, New Relic, Jaeger, Prometheus + Grafana, Splunk, Honeycomb, Lightstep, Azure Monitor, AWS X-Ray, etc.).
- **Three main pillars**:
  1. **Traces** – Distributed tracing (tracking requests across services).
  2. **Metrics** – Numeric measurements over time (counters, gauges, histograms).
  3. **Logs** – Structured log entries, increasingly correlated with traces.
- **Components**:
  - Specifications & APIs (language-specific, stable)
  - SDKs (per language, where you configure exporters, processors, etc.)
  - OpenTelemetry Collector (a standalone agent/receiver that can receive, process, and export telemetry)
  - Automatic instrumentation libraries (zero-code or low-code instrumentation for popular frameworks)
- **Supported languages** (as of 2025): Fully supported in Go, Java, JavaScript/Node.js, Python, .NET/C#, Ruby, PHP, Rust, C++, Erlang/Elixir, Swift, and more are in progress or community-maintained.

### Why it matters
Before OTel, teams often had to add multiple instrumentation libraries (one for each observability vendor) or pick a single vendor early. OpenTelemetry lets you standardize on one instrumentation layer and switch or multi-export backends without code changes.

In short: OpenTelemetry is the modern, industry-standard way to make your applications observable in cloud-native and microservices environments.
