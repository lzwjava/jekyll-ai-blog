---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disable Plan Skill and Agent Delegation
translated: false
type: note
---

The plan mode is a skill, but the slowness you're seeing is from delegation (subagent spawning for reviews). Two things to disable:

1. **Disable the plan skill** so the agent doesn't write plans:

```bash
hermes skills config
```

Or remove it:

```bash
rm -rf ~/.hermes/skills/software-development/plan/
```

2. **Disable delegation** to stop subagent spawning (this is the real bottleneck):

```bash
hermes config set delegation.max_concurrent_children 0
```

Or disable the `delegation` toolset entirely:

```bash
hermes tools disable delegation
```

After either change, `/reset` to start a fresh session.

The delegation spawning (review → spec check → code quality review, each as a separate subagent) is what's burning time and tokens. Disabling the `delegation` toolset forces the agent to do everything inline — faster, fewer API calls.
