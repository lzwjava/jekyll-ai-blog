---
audio: false
generated: true
image: false
lang: en
layout: post
title: Electron download fix via mirror
translated: false
type: note
---

Everything checks out:

- **Mirror reachable** — `npmmirror.com` returns `HTTP/2 302` (redirect to the binary) quickly through your proxy, vs. the stalled direct GitHub connection.
- **npm passes it through** — `npm config get electron_mirror` returns the value, so Electron's postinstall will see `npm_config_electron_mirror` and download from the mirror. (The `Unknown user config` warning is harmless — npm still forwards the setting to lifecycle scripts; it's just a deprecation notice for a future npm major.)

## Summary

**Why it was stuck:** `hermes update` → "Updating Node.js dependencies" → `npm ci` → Electron's `install.js` postinstall trying to download its ~100 MB binary **directly from GitHub** (bypassing your `localhost:7890` proxy). That direct connection stalled, so `npm ci` never returned and the Python updater sat blocked in `subprocess.wait()` — exactly where your Ctrl-C traceback landed.

**What I did:**
1. Killed the orphaned `node install.js` / `npm ci` processes and removed the empty `electron-download-*` temp dir.
2. Created `~/.npmrc` pointing Electron (and electron-builder binaries) at the fast `npmmirror.com` mirror.
3. Verified the mirror is reachable and that npm forwards the config to the postinstall.

**Next step — just re-run the update:**

```
hermes update
```

It should now sail through "Updating Node.js dependencies" because the Electron binary will come from the mirror instead of stalling on GitHub. If you'd like, I can run the `npm ci` step myself right now to confirm the download completes end-to-end before you re-run `hermes update` — say the word.
