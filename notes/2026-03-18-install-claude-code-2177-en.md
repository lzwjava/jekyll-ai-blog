---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install Claude Code Version 2.1.77
translated: false
type: note
---

**Question:** How do I install Claude Code version 2.1.77?

**Answer:**

## Installing Claude Code v2.1.77

There are two main approaches depending on your installation method.

---

### Method 1: Native Installer (Recommended) — Install a Specific Version

To install a specific version using the native installer, pass the version number as an argument to the install script:

**macOS / Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | bash -s 2.1.77
```

**Windows (PowerShell):**
```powershell
irm https://claude.ai/install.ps1 | iex
```
> Note: The Windows PowerShell method installs the latest by default. For a specific version on Windows, use WSL and run the Linux command above inside it.

---

### Method 2: npm (Legacy) — Install a Specific Version

The npm method still works but is no longer the recommended approach. Use this if you need to pin a specific version or work in an environment where npm is the standard package manager.

```bash
npm install -g @anthropic-ai/claude-code@2.1.77
```

> **Note:** This requires Node.js 18.0+. If you see `EACCES` permission errors, do **not** use `sudo`. Fix your npm permissions instead.

---

### Method 3: Pin the Version and Disable Auto-Updates

After installation, if you want to stay on `2.1.77` and prevent auto-updates:

Set `DISABLE_AUTOUPDATER` to `"1"` in the `env` key of your `settings.json` file to prevent automatic updates after pinning a version.

Your `~/.claude/settings.json` should look like:
```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

---

### Verify the Installation

```bash
claude --version
```

You should see `2.1.77` confirmed in the output.

---

### Important Notes

- The native installer is faster, requires no dependencies, and auto-updates in the background. Use the native installation method when possible.
- Claude Code requires a paid account — Claude Pro ($20/month) works for most developers. If you only need API access, an Anthropic Console account with credits works too.

---

**References:**

- [Claude Code Official Docs – Advanced Setup](https://code.claude.com/docs/en/setup)
- [Claude Code Installation – Vibe Coding With Fred](https://vibecodingwithfred.com/blog/claude-code-installation-guide/)
- [How to Install Claude Code – morphllm.com](https://www.morphllm.com/install-claude-code)
- [npm – @anthropic-ai/claude-code](https://www.npmjs.com/package/@anthropic-ai/claude-code)