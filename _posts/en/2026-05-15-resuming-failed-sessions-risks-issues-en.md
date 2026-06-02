---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resuming Failed Sessions Risks Issues
translated: false
type: note
---

Question: Will resuming a Claude session that previously failed due to "skip-dangerously-permission" cause issues, and will it prompt for a command?

Answer:

Yes, it likely will cause issues. When a previous session failed due to a permission-related flag like `--skip-dangerously-permission`, the session state may contain partial or inconsistent data. Resuming such a session with:

```bash
claude --resume 551e937c-4223-4a22-81ba-5ee0690071d4
```

can trigger errors because Claude may detect that the previous run didn’t complete safely. Depending on the implementation:

* It might prompt you to rerun with `--skip-dangerously-permission` again.
* It could fail with a permission or integrity error.
* In some setups, it may refuse to resume and require creating a fresh session.

**Best practice:** If a session previously failed due to permission issues, either:

1. Ensure proper permissions and restart the session fresh.
2. Or resume with the same flags (`--skip-dangerously-permission`) to match the previous environment, but be aware of potential instability.

References:

* [Anthropic Claude CLI documentation](https://www.anthropic.com/claude) (general guidance on session flags and resume behavior)
* Practical experience: CLI tools that store session state usually fail to resume safely if the last run was unsafe or interrupted.
