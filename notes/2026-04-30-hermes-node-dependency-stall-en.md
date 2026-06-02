---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Update Node Dependency Stalls
translated: false
type: note
---

Question: Why does `hermes update` get stuck at "→ Updating Node.js dependencies..."?

Answer:

This is a **known issue** with `hermes update`. The process hangs at the `→ Updating Node.js dependencies...` step because it runs `npm install --silent` under the hood, and `npm install` can be slow or appear to hang for several reasons:

---

## Root Cause

In `hermes_cli/main.py`, when a `package.json` is found, the update script runs:

```python
subprocess.run(["npm", "install", "--silent"], cwd=PROJECT_ROOT, check=False)
```

The `--silent` flag suppresses all output, so it looks like it's frozen even when it's actively working.

This is the main reason it *appears* stuck — there is no progress output, and `npm install` can take a long time (minutes) to resolve and download the full Node.js dependency tree.

---

## Common Reasons It Actually Hangs or Is Very Slow

1. **Slow npm registry** — `npm install` fetches packages from the npm registry, which can be slow depending on your network or region.

2. **Large dependency tree** — After running, `npm install` can produce a 2000+ line diff in `package-lock.json`, indicating a large and complex dependency tree that takes time to resolve.

3. **Inconsistent lockfile** — The committed `package-lock.json` may not be fully consistent with `package.json`, so `npm install` silently re-resolves the whole graph instead of doing a fast install.

4. **Node.js version mismatch** — The repo enforces `node >=20`, so if you're on an older Node.js version, installs may fail silently or behave unexpectedly.

---

## How to Fix / Workaround

**Option 1: Wait it out**
It is likely just working silently. Give it 3–5 minutes before concluding it's truly stuck.

**Option 2: Run the npm install manually with visible output**

```bash
cd ~/.hermes/hermes-agent
npm install
```

This will show progress and errors, unlike the silent subprocess call.

**Option 3: Use `npm ci` instead (faster, deterministic)**
The recommended fix from the GitHub issue is to replace `npm install --silent` with `npm ci --silent`, which installs exactly from the lockfile without re-resolving dependencies — making it faster and not dirtying the working tree.

You can manually do this:

```bash
cd ~/.hermes/hermes-agent
npm ci
```

**Option 4: Check your Node.js version**

```bash
node --version
```

Make sure it is **v20 or higher** (v22 LTS is recommended).

**Option 5: Run `hermes doctor`**

```bash
hermes doctor
```

This checks Node.js dependencies and surfaces any specific issues.

---

## Summary

The update is **not truly frozen** in most cases — it just has no visible output because of `--silent`. The underlying `npm install` is re-resolving a large dependency tree. The safest immediate fix is to `cd ~/.hermes/hermes-agent && npm ci` manually to see what's happening.

References:

- [Bug: hermes update runs npm install instead of npm ci · Issue #4048](https://github.com/NousResearch/hermes-agent/issues/4048)
- [Bug: npm install hangs at "Installing Node.js dependencies" · Issue #8145](https://github.com/NousResearch/hermes-agent/issues/8145)
- [Hermes Agent FAQ & Troubleshooting](https://hermes-agent.nousresearch.com/docs/reference/faq)
