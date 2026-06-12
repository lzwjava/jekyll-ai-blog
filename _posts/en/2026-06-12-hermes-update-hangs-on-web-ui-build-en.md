---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Update Hangs on Web UI Build
translated: false
type: note
---

**Question:** Why does `hermes update` (Hermes Agent) get stuck at "→ Building web UI..." after installing the repo root + ui-tui and web workspace packages?

**Answer:**

It's almost certainly not stuck — it's silent. The "Building web UI..." step runs the web workspace's build script, which is:

```
tsc -b && vite build
```

The `hermes update` spinner swallows the subprocess's stdout until the step finishes, and `tsc -b` (TypeScript project-references build) emits **zero output while type-checking**. On a cold cache (fresh `node_modules`, no `.tsbuildinfo`), `tsc -b` over ~2,200+ modules can take several minutes — especially on your 16 GB M2 Air where tsc + npm's leftover memory pressure can push you into swap. The vite part itself takes ~3s once tsc clears, as shown in a recent identical report on the repo: the same update sequence on macOS shows "added 769 packages in 7s ✓ repo root + ui-tui, web workspaces (desktop skipped) → Building web UI..." sitting on a spinner, then eventually completing with "vite v7.3.2 ... ✓ 2257 modules transformed ... ✓ built in 2.92s ✓ Web UI built".

Debug it in 30 seconds instead of guessing:

```bash
# 1. Is anything actually working? Look for tsc/vite eating CPU
ps aux | grep -E 'tsc|vite|esbuild' | grep -v grep
# tsc at ~100% CPU = building, not hung

# 2. If you want real output, kill the update and build manually
cd ~/.hermes/hermes-agent/web
npx tsc -b --verbose   # shows per-project progress
npm run build          # full vite output

# 3. Then resume
hermes update
```

Two things worth fixing while you're in there:

1. **Node version.** The same logs show npm EBADENGINE warnings: `@icons-pack/react-simple-icons@13.13.0` requires node >=24 while the system has v22.x. It's a warning not a failure, but you're one transitive dep away from a silent runtime break. `nvm install 24 && nvm use 24` (or `mise use node@24`).

2. **Swap check on the Air.** If `ps` shows tsc alive but crawling, check `vm_stat | grep -E 'Pageouts|swap'`. With 16 GB and a fat npm install just finished, tsc can thrash. Quitting browsers/Electron apps before `hermes update` genuinely helps here.

If `tsc -b` errors out (rather than hanging), the spinner UI can also mask the non-zero exit — the manual `npm run build` in step 2 will surface the actual TypeScript error immediately. If the web frontend never gets built (e.g. npm unavailable or reduced PATH), the documented manual fallback is `cd ~/.hermes/hermes-agent/web && npm install && npm run build`, then relaunch — the dashboard serves whatever exists in `web_dist`. Production builds output to `hermes_cli/web_dist/`, which the FastAPI server serves as a static SPA; `hermes update` only rebuilds the frontend automatically if npm is available.

One more data point: in the linked issue the *real* hang was one step later — "→ Building desktop packaged app..." stalls inside electron-builder during packaging. Your run says `(desktop skipped)`, so you've dodged that one; yours is just tsc being mute.

**References:**

- [Issue #38974 — stuck during `hermes update` on macOS](https://github.com/NousResearch/hermes-agent/issues/38974)
- [Hermes Agent docs — Web Dashboard build pipeline](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard)
- [Manual web UI build fallback](https://hermes-agent.ai/how-to/use-hermes-web-ui)
