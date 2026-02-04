---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Fixing npm Issues Step by Step
translated: false
type: note
---

These are three different troubleshooting steps that target different parts of your npm setup. Here's what each does:

## **rm package-lock.json**
- Deletes the **version lock file** that records exact versions of all dependencies
- Useful when: the lock file is corrupted or has conflicting version information
- Next `npm install` will generate a fresh lock file by resolving versions from scratch based on `package.json`
- **Warning:** This can change which exact versions get installed, potentially breaking things

## **rm -rf node_modules**
- Deletes all **installed packages** from your project
- Useful when: packages are corrupted, incomplete, or you have weird state issues
- Forces a complete reinstall of everything
- Most common troubleshooting step because it's the safest

## **npm cache clean --force**
- Clears npm's **global cache** (usually in `~/.npm`)
- Useful when: downloaded packages in the cache are corrupted
- Rarely needed - npm's cache is usually self-healing
- **Note:** Modern npm versions discourage this unless you have a specific reason

## **When to use each:**

**Common troubleshooting progression:**
1. Start with just `rm -rf node_modules && npm install` (fixes 90% of issues)
2. If that doesn't work: add deleting lock file
3. If still broken: clear cache as last resort

**Example scenario:**
```bash
# Standard "turn it off and on again" for npm:
rm -rf node_modules
npm install

# Nuclear option when something is really broken:
rm -rf node_modules
rm package-lock.json
npm cache clean --force
npm install
```

The lock file and node_modules are project-specific, while the cache is global across all your projects. That's why clearing cache is more drastic and rarely necessary.