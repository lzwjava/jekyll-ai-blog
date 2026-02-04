---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Install vs Update in npm
translated: false
type: note
---

The main differences between `npm install` and `npm update`:

## **npm install**
- **Installs** packages listed in `package.json` that aren't yet in `node_modules`
- Respects the **exact version ranges** specified in `package.json` (e.g., `^1.2.3`)
- Creates or updates `package-lock.json` to lock those versions
- If you run it when packages are already installed, it generally does nothing (unless lock file is missing)

## **npm update**
- **Updates** existing packages in `node_modules` to the latest versions that still satisfy the ranges in `package.json`
- Won't install packages that aren't already present
- Updates `package-lock.json` with the new versions
- For example, if you have `^1.2.3` in package.json and version 1.2.3 installed, `npm update` might upgrade it to 1.9.0 (but not 2.0.0)

## **Quick example:**

```json
// package.json shows: "lodash": "^4.17.0"
// currently installed: 4.17.0
// latest available: 4.17.21
```

- `npm install` → keeps 4.17.0 (already satisfies the requirement)
- `npm update` → upgrades to 4.17.21 (latest within the `^` range)

**In practice:** Use `npm install` for fresh setups or adding new packages. Use `npm update` when you want to get newer versions of your existing dependencies within their allowed ranges.