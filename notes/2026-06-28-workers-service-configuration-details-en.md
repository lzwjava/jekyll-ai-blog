---
audio: false
generated: true
image: false
lang: en
layout: post
title: Workers Service Configuration Details
translated: false
type: note
---

This is a Cloudflare **Workers** service (not Pages — despite the breadcrumb, the URL path is `/workers/services/`). It's `sec-edgar-gpt`, deployed from your GitHub repo. Here's what each section means:

## Variables and secrets

Runtime config injected into your Worker. **Variables** are plaintext (e.g. `API_BASE_URL`), **secrets** are encrypted and write-only (e.g. `OPENAI_API_KEY`, SEC EDGAR auth). Accessed via `env.MY_VAR` in your handler. Currently none defined.

## Trigger events

How the Worker gets invoked beyond HTTP:

- **Cron triggers** — scheduled execution (`*/5 * * * *`), runs your `scheduled()` handler
- **Queue/messaging** — consume from Cloudflare Queues

## Observability

Debugging telemetry, all currently **disabled**:

- **Logs** — `console.log` persistence in dashboard (otherwise ephemeral)
- **Traces** — distributed tracing spans
- **Exports** — ship logs to external sinks (Datadog, etc.)
- **Sampling** — capture a fraction of requests to control cost/volume
- **Tail Worker** — a separate Worker that receives this Worker's logs/events programmatically

You'd want to flip **Logs** on for a GPT-backed service — cheap and useful for debugging API failures.

## Runtime

- **Placement** — `Default` runs at the edge nearest the user. `Smart` placement moves execution closer to your backend/origin if that reduces latency (useful when you make many round-trips to SEC EDGAR or an LLM API).
- **Compatibility date** (`Jun 27, 2026`) — pins Workers runtime behavior to that date's semantics, so future runtime changes don't break you.
- **Compatibility flags** — opt into specific runtime features (e.g. `nodejs_compat` for Node built-ins).

## Build

CI/CD from Git:

- **Build command: None**, **Deploy command: `npx wrangler deploy`** — on push to `main`, Cloudflare runs wrangler to ship it
- **Version command: `npx wrangler versions upload`** — uploads a non-production version without promoting it (for preview/gradual rollout)
- **Watch paths: `*`** — any file change triggers a build
- **Branch control** — `main` is production; other branches get preview deployments
- **Build cache: Enabled** — caches dependencies between builds for speed
- **API token** — scoped token the build pipeline uses to deploy on your behalf

## General

Name and the delete button (irreversible — wipes versions, deployments, config).

---

**Pages vs Workers note:** The header says "Workers & Pages" because they were unified. Real *Pages* projects center on static-asset builds with a `_worker.js` or Functions directory and have a "Build output directory" setting. Yours is a pure Worker — `wrangler deploy`, compatibility flags, cron triggers — so treat it as a Worker. The `nodejs_compat` flag is the one thing worth checking if you're pulling SEC filings and need Node streams/buffers.
