---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upgrade OpenCode CLI
translated: false
type: note
---

Question: How do I upgrade OpenCode CLI?

Answer:

To upgrade **OpenCode**, you can use its built-in upgrade command directly in your terminal.

### ✅ Upgrade to the latest version

```bash
opencode upgrade
```

This will update OpenCode to the newest available version automatically. ([OpenCode][1])

---

### 🎯 Upgrade to a specific version

If you want a fixed version (for example rollback or testing):

```bash
opencode upgrade v1.2.0
```

or without `v` depending on version style:

```bash
opencode upgrade 1.2.0
```

---

### ⚙️ Optional: specify install method

If you installed OpenCode via a package manager and want to be explicit:

```bash
opencode upgrade --method npm
```

Supported methods include: `curl`, `npm`, `pnpm`, `bun`, `brew`. ([OpenCode][1])

---

### 🧠 Important notes

* By default, OpenCode may also auto-check for updates on startup.
* You can disable auto-update in config if needed (useful for stable environments).
* Upgrading can also be used to **downgrade**, just pass an older version number.

---

If you want, tell me how you installed OpenCode (npm / brew / curl), and I can give you the exact safest upgrade path for your setup.

[1]: https://opencode.ai/docs/cli/?utm_source=chatgpt.com "CLI | OpenCode"