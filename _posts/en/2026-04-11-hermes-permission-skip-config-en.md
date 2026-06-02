---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Permission Skip Configuration
translated: false
type: note
---

Question: Does Hermes Agent have something like `--dangerously-skip-permissions` like Claude?

Answer:

Yes — **Hermes Agent has an equivalent**, but it's **configuration-based instead of CLI flag**.

Claude:

```
claude --dangerously-skip-permissions
```

Hermes equivalent:

```
approvals.mode: off
```

This **disables all dangerous command prompts**, effectively the same behavior.

---

## Hermes permission system

Hermes normally **blocks dangerous commands** and asks for approval, such as:

* `rm -rf`
* `chmod 777`
* `DROP TABLE`
* `kill -9`
* `curl | sh`
* systemctl stop
* destructive filesystem operations

These require explicit confirmation in CLI. ([Hermes Agent][1])

---

## Hermes “skip permission” mode

You can disable approvals in config:

```yaml
approvals:
  mode: off
```

Modes:

* `manual` → always ask (default)
* `smart` → auto-approve safe, ask dangerous
* `off` → **skip all prompts (YOLO mode)**

This is explicitly documented as **skip all prompts**. ([Mintlify][2])

---

## CLI-style equivalent (like Claude)

You can simulate:

```bash
hermes --yolo
```

or config:

```yaml
approvals:
  mode: off
```

This makes Hermes:

* run shell commands automatically
* edit files automatically
* install packages automatically
* access network automatically
* no confirmation prompts

Exactly same spirit as:

```
--dangerously-skip-permissions
```

---

## Important difference vs Claude

Claude:

* global skip
* no safety layers

Hermes:

* still has sandbox options
* container isolation
* allowlist patterns
* Docker backend safety

Hermes can **skip approval but still sandbox execution**, which is safer. ([Hermes Agent][1])

---

## Even more dangerous mode (Hermes)

You can also:

```yaml
toolsets:
  - all
approvals:
  mode: off
```

This gives:

* terminal
* browser
* file system
* SSH
* Docker
* API calls
* messaging bots

Fully autonomous agent.

---

## TL;DR

Yes.

Claude:

```
--dangerously-skip-permissions
```

Hermes:

```
approvals.mode: off
```

Same behavior:

* no permission prompts
* full autonomous execution

Hermes also supports **smart auto-approval**, which Claude doesn't.

```
approvals.mode: smart
```

This is actually nicer for long-running agents.

References:

* [https://hermes-agent.nousresearch.com/docs/user-guide/security/](https://hermes-agent.nousresearch.com/docs/user-guide/security/)
* [https://www.mintlify.com/NousResearch/hermes-agent/reference/configuration-options](https://www.mintlify.com/NousResearch/hermes-agent/reference/configuration-options)
* [https://docs.bswen.com/blog/2026-02-21-dangerously-skip-permissions-explained/](https://docs.bswen.com/blog/2026-02-21-dangerously-skip-permissions-explained/)

[1]: https://hermes-agent.nousresearch.com/docs/user-guide/security/?utm_source=chatgpt.com "Security | Hermes Agent"
[2]: https://www.mintlify.com/NousResearch/hermes-agent/reference/configuration-options?utm_source=chatgpt.com "Configuration options - Hermes Agent"
