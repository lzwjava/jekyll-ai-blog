---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Mastering npm config list
translated: false
type: note
---

I'll explain the `npm config list` command and how to use it.

## Basic Usage

```bash
npm config list
```

This command displays your current npm configuration settings. It shows:
- User-specific settings (from `~/.npmrc`)
- Global settings
- Built-in npm defaults

## Common Variations

**List only user and global settings (without defaults):**
```bash
npm config list --json
```

**List in JSON format for easier parsing:**
```bash
npm config list -l
```

**Show all config options including defaults:**
```bash
npm config list -l
```

## What You'll See

The output typically includes settings like:
- Registry URL (`registry`)
- Package installation prefix (`prefix`)
- Cache location (`cache`)
- User info (`init-author-name`, `init-author-email`)
- Authentication tokens (partially hidden)
- Proxy settings

## Related Useful Commands

**Get a specific config value:**
```bash
npm config get registry
```

**Set a config value:**
```bash
npm config set registry https://registry.npmjs.org/
```

**Delete a config value:**
```bash
npm config delete proxy
```

**Edit config in your default editor:**
```bash
npm config edit
```

The command is helpful for debugging npm issues, checking your registry settings, or verifying authentication configuration.
