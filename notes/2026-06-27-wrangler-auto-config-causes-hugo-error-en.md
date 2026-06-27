---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wrangler auto-config causes Hugo error
translated: false
type: note
---

Question: Why is my Cloudflare Worker deploy running `npx hugo` and failing, when sec-edgar-gpt is a Worker, not a Hugo site?

Answer:

Wrangler's auto-config detected your repo, guessed it was a static site, and injected `npx hugo` as a build step. It's not in your build command (that says "None") — it comes from `runAutoConfig` / `maybeRunAutoConfig` in the trace. `npx hugo` then fails with `could not determine executable to run` because Hugo isn't an npm package (it's a Go binary), so npx can't find anything to execute.

Two things are wrong: (1) auto-config shouldn't fire for a Worker, and (2) even if it did, Hugo isn't installable via npx.

Fix — pin everything explicitly so Wrangler stops guessing.

Make sure `wrangler.toml` declares the Worker clearly:

```toml
name = "sec-edgar-gpt"
main = "src/index.js"   # your actual entry
compatibility_date = "2026-06-27"

# kill auto-build inference
[build]
command = ""
```

An empty `[build]` command tells Wrangler there's nothing to build, which suppresses the framework-detection path that injected `hugo`.

Also check your Cloudflare dashboard build settings — the deploy command is `npx wrangler deploy`, which is fine, but if a newer Wrangler is doing auto-config, pin the version:

```bash
npm i -D wrangler@latest   # or a known-good version
npx wrangler deploy
```

If the `[build]` block alone doesn't stop it, disable auto-config explicitly:

```bash
WRANGLER_DISABLE_AUTOCONFIG=1 npx wrangler deploy
```

Or set it as a build variable in the dashboard. The root cause is the auto-config heuristic misclassifying the repo; the empty build command plus disabling auto-config is the clean kill.

If you paste your `wrangler.toml` and repo structure I'll tell you exactly which line is triggering the Hugo guess.
