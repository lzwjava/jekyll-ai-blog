---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix OpenClaw Plugin Configuration Warnings
translated: false
type: note
---

**Question:**
How to fix OpenClaw config warnings and plugin installation errors after update?

---

**Answer:**

These warnings and errors come from **plugin configuration issues + a failed plugin install**. They are not fatal, but you should clean them up to avoid runtime problems.

Let’s go through each issue and fix them properly.

---

# 1) Duplicate plugin path warning

```
ignored plugins.load.paths entry that points at OpenClaw's current bundled plugin directory
```

### ✅ Cause

You manually added a plugin path that OpenClaw already includes by default.

### ✅ Fix

Edit your config file (likely `~/.openclaw/config.json` or similar):

* Find:

```json
"plugins": {
  "load": {
    "paths": [...]
  }
}
```

* Remove any path that looks like:

```
.../openclaw/plugins
```

### ✅ Alternative (auto fix)

```bash
openclaw doctor --fix
```

---

# 2) openclaw-weixin missing `channelConfigs`

```
plugin openclaw-weixin: channel plugin manifest declares openclaw-weixin without channelConfigs metadata
```

### ✅ Cause

The plugin manifest (`openclaw.plugin.json`) is incomplete.

### ✅ Fix options

### Option A — Update plugin (recommended)

```bash
openclaw plugins update openclaw-weixin
```

### Option B — Manually fix (advanced)

Go to:

```
node_modules/openclaw-weixin/openclaw.plugin.json
```

Add something like:

```json
"channelConfigs": {
  "weixin": {
    "required": [],
    "optional": []
  }
}
```

⚠️ Only do this if you know what you're doing — updating is safer.

---

# 3) Stale plugin config: `brave`

```
plugin not found: brave
```

### ✅ Cause

You have a config entry for a plugin that is no longer installed.

### ✅ Fix

Remove it from your config:

```json
"plugins": {
  "entries": {
    "brave": ...
  }
}
```

---

# 4) Critical error: missing plugin directory

```
Plugin install payload missing:
@openclaw/brave-plugin
```

### ❗ This is the real problem

The plugin installation **failed or got corrupted**.

---

## ✅ Fix (clean reinstall)

Run:

```bash
cd ~/.openclaw
rm -rf npm/node_modules
rm -rf npm/package-lock.json

openclaw plugins install
```

---

## ✅ If still failing

Manually install:

```bash
cd ~/.openclaw/npm
npm install @openclaw/brave-plugin
```

---

## ✅ Or remove it completely (simpler)

If you don’t need Brave plugin:

1. Remove from config
2. Then run:

```bash
openclaw plugins sync
```

---

# 5) Summary (clean state checklist)

After fixing, you should have:

* ✅ No duplicate plugin paths
* ✅ No `brave` in config (unless installed)
* ✅ `openclaw-weixin` updated or fixed
* ✅ `node_modules` rebuilt cleanly

---

# 6) Why this happened

This usually occurs when:

* You upgraded OpenClaw (e.g. v2026.4.27 → v2026.4.29)
* Plugin structure changed
* Old config was not migrated cleanly

---

# 7) Recommended workflow (future)

After each update:

```bash
openclaw doctor --fix
openclaw plugins sync
```

---

If you want, I can help you:

* Inspect your full config
* Suggest a **minimal clean plugin setup** (best for low token usage — you mentioned 3M/day issue 👀)
