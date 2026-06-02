---
audio: false
generated: true
image: false
lang: en
layout: post
title: Updating OpenClaw Version
translated: false
type: note
---

Question: How do I update OpenClaw from v2026.4.27 to v2026.4.29?

Answer:

The update is actually very simple—OpenClaw has a built-in command for this.

### ✅ Recommended (1 command)

Just run this in your terminal:

```bash
openclaw update
```

This command will:

* Detect how you installed OpenClaw (npm or git)
* Download the latest version (e.g., v2026.4.29)
* Run diagnostics (`doctor`)
* Restart the gateway automatically ([OpenClaw][1])

---

### 🔍 Optional useful commands

If you want more control:

* Preview update (safe check):

```bash
openclaw update --dry-run
```

* Switch to beta/dev channel:

```bash
openclaw update --channel beta
```

* Check update status:

```bash
openclaw update status
```

---

### 🧪 After updating (important)

Sometimes things don’t fully apply until you verify:

```bash
openclaw doctor
openclaw gateway restart
openclaw health
```

These steps ensure your system is clean and working properly ([OpenClaw][1])

---

### ⚠️ If `openclaw update` doesn’t work

#### Case 1: Installed globally via npm/pnpm

Use:

```bash
npm install -g openclaw@latest
# or
pnpm add -g openclaw@latest
```

#### Case 2: Installed via script

Re-run installer:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

This upgrades in place automatically ([OpenClaw][2])

---

### ⚠️ Real-world warning (important)

Recent versions (4.x series) sometimes introduce breaking changes. For example:

* Environment variables renamed
* Config paths changed (`~/.moltbot` → `~/.openclaw`)

If your setup is customized, update carefully (or test with `--dry-run` first).

---

### 💡 Quick summary

* Fastest: `openclaw update`
* If issues: reinstall via npm or script
* Always run `doctor` after

---

If you want, tell me how you installed OpenClaw (npm / docker / source), and I can give you a **precise upgrade path tailored to your setup**.

[1]: https://docs.openclaw.ai/install/updating?utm_source=chatgpt.com "Updating - OpenClaw"
[2]: https://docs.openclaw.ai/updating?utm_source=chatgpt.com "Updating - OpenClaw"
