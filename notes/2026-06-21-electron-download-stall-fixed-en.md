---
audio: false
generated: true
image: false
lang: en
layout: post
title: Electron download stall fixed
translated: false
type: note
---

Confirmed — `Electron.app` is unpacked and `path.txt` resolves correctly. The desktop dependencies are fully installed.

## Done

The stall is fixed and verified:

|                 | Before                       | After                             |
| --------------- | ---------------------------- | --------------------------------- |
| `npm ci`        | hung indefinitely            | exits 0 in ~21s                   |
| Electron binary | stalled on direct GitHub CDN | 109 MB downloaded via `npmmirror` |
| `Electron.app`  | absent                       | ✓ present & unpacked              |

**Root cause:** Electron's postinstall downloads its binary direct from GitHub, bypassing your `localhost:7890` proxy → stalled → `npm ci` never returned → `hermes update` blocked in `subprocess.wait()`.

**Fix:** `~/.npmrc` now points `electron_mirror` (and `electron_builder_binaries_mirror`) at `npmmirror.com`. This is persistent, so future installs won't hit this again.

You can now re-run `hermes update` — the Python/dependency steps will complete since the Node side is already done and cached. If it re-runs `npm ci` it'll be near-instant (binary is cached).

One note: the `hermes update` earlier *did* finish its Python work (it upgraded `hermes-agent` 0.15.1 → 0.17.0 before reaching the Node step), so only the Node-dependency phase was incomplete — which is now resolved.
