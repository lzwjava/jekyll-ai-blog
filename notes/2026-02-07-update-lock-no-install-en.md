---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Update Lock File Without Installing
translated: false
type: note
---

The `--package-lock-only` flag in npm install tells npm to **only update the `package-lock.json` file without actually installing any packages** in your `node_modules` folder.

This is useful when you want to:

1. **Update the lock file** after manually editing `package.json` - you can regenerate `package-lock.json` to reflect your changes without downloading anything

2. **Resolve lock file conflicts** - if you're merging branches and have conflicts in `package-lock.json`, you can run `npm install --package-lock-only` to regenerate it based on your current `package.json`

3. **Check what versions would be installed** - you can see what the resolved dependency tree would look like without actually installing packages

4. **Save time in CI/CD pipelines** - if you only need to update the lock file for a commit, you don't waste time downloading packages

For example:

```bash
npm install --package-lock-only
```

This contrasts with `--dry-run` (which shows what would be installed but doesn't modify anything) and the normal `npm install` (which both updates the lock file and installs packages).
