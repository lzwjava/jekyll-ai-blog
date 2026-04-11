---
audio: false
generated: true
image: false
lang: en
layout: post
title: Manually Install Camoufox Bypassing npm
translated: false
type: note
---

Here's the blog formatted and saved:

---

# Manually Installing Camoufox to Bypass Slow npm Downloads

**Problem:** `npm install` on `@askjo/camofox-browser` stalls trying to download a ~627 MB browser binary.

**Fix:** Drop the binary directly into the cache dir `camoufox-js` already looks in.

---

## Step 1 — Identify Your Arch

```bash
uname -m
```

| Output | Arch | Zip to download |
|--------|------|----------------|
| `x86_64` | Intel/AMD Linux | `camoufox-146.0.1-alpha.25-lin.x86_64.zip` |
| `aarch64` | ARM64 / Apple M / Pi | `camoufox-146.0.1-alpha.25-lin.arm64.zip` |
| `arm64` | macOS Apple Silicon | `camoufox-146.0.1-alpha.50-mac.arm64.zip` |

---

## Step 2 — Download the Zip

Get it from **daijro/camoufox** releases, not apify/camoufox-js (that's just the JS wrapper, no binaries inside).

---

## Step 3 — Extract to the Cache Dir

```bash
mkdir -p ~/.cache/camoufox
cd ~/.cache/camoufox
unzip -o /path/to/camoufox-146.0.1-alpha.25-lin.x86_64.zip
```

The cache dir location is hardcoded in `camoufox-js`:

| OS | Path |
|----|------|
| Linux | `~/.cache/camoufox/` |
| macOS | `~/Library/Caches/camoufox/` |
| Windows | `%LOCALAPPDATA%\camoufox\camoufox\Cache\` |

---

## Step 4 — Create `version.json`

The zip doesn't include this — the official installer writes it. Without it, `camoufox-js` refuses to recognize the binary.

Find the version by running the binary after extraction:

```bash
$ ~/.cache/camoufox/camoufox --version
Camoufox Camoufox 146.0.1-beta.25
```

Split at the last hyphen:

```json
// ~/.cache/camoufox/version.json
{"version":"146.0.1","release":"beta.25"}
```

---

## Step 5 — Verify

```bash
$ ls ~/.cache/camoufox/
camoufox  camoufox-bin  camoufox.cfg  browser/  fonts/  libxul.so  omni.ja  version.json ...

$ ~/.cache/camoufox/camoufox --version
Camoufox Camoufox 146.0.1-beta.25
```

---

## Step 6 — Install Without Downloading

```bash
cd ~/projects/camofox-browser
npm install --ignore-scripts   # skips the slow postinstall
npm start                      # launches immediately
```

---

## Why It Works

`camoufox-js` calls `installedVerStr()` → `Version.fromPath()` which checks:

1. `~/.cache/camoufox/` exists and isn't empty
2. `~/.cache/camoufox/version.json` is present and valid
3. The version is within the supported range

If all pass → returns the cache dir path as the browser location. No download needed.

---

## Gotcha

> The zip is named `alpha.25` but the binary self-reports as `beta.25`. Always use the binary's own `--version` output for the version.json fields.

---

Saved to `memory/2026-04-11.md`.