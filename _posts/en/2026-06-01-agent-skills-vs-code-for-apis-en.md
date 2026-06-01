---
audio: false
generated: true
image: false
lang: en
layout: post
title: Agent Skills vs Code for APIs
translated: false
type: note
---

**Question:** Instead of writing fixed wrapper code for AMD Dev Cloud / DigitalOcean API calls (like in `snapshots.py`), should we just give the agent (Hermes/Claude Code) the API token and let it figure out what to do dynamically? And is the general principle: agents for flexible/exploratory tasks, code for fixed/complex tasks?

**Answer:**

Yes, exactly right. This is one of the core judgment calls in modern AI engineering. Let me sharpen the framework:

## The Principle: Skills vs. No-Skills

```
Fixed + Complex  →  Write code (skills)
Flexible + Simple →  Give agent the token (no-skills needed)
```

Your `snapshots.py` is a perfect example of **over-engineering a task that an agent handles trivially**. The DigitalOcean API is well-documented, Claude Code / Hermes knows it cold, and snapshot operations are exploratory by nature ("show me what's running", "create one", "delete old ones").

## What Agent-First Looks Like

Instead of `snapshots.py`, just:

```bash
export DIGITALOCEAN_TOKEN=xxx

claude "List all my droplets and their snapshots. Delete any snapshot older than 7 days on the amd-dev droplet."
```

Or with Hermes via OpenAI-compatible endpoint:

```python
system = """
You have access to the DigitalOcean API v2.
Base URL: https://api.digitalocean.com/v2
Auth header: Authorization: Bearer {token}

Use HTTP tool calls to accomplish tasks. Be precise, confirm before deleting.
"""
```

The agent reads the DO API docs it was trained on, constructs the right `GET /v2/droplets`, `GET /v2/droplets/{id}/snapshots`, `DELETE /v2/snapshots/{id}` calls — no wrapper needed.

## When to Write Code (The Real Threshold)

| Situation | Agent or Code? |
|---|---|
| "List snapshots, delete old ones" | Agent |
| "SSH tunnel + port forward to droplet" | Agent (probably) |
| "Spin up droplet, wait for cloud-init, run benchmark, snapshot, destroy" — reliably, in CI | **Code** |
| Complex retry logic with backoff + state machine | **Code** |
| Multi-step workflow you run 100x/day | **Code** |
| One-off exploration / ops task | Agent |

The threshold is: **would a bug here cost you money or data?** Snapshot deletion on wrong droplet = bad. For that, you want idempotent, reviewed code with `--dry-run`. For "what snapshots do I have?" — just ask the agent.

## The Deeper Insight: Agents Collapse the Skill Gap

What `snapshots.py` really encodes is **your past effort learning the DO API** — pagination, auth headers, error handling. An agent already has that knowledge. So the wrapper is negative ROI unless:

1. You need **deterministic behavior** (same action, same result, every time)
2. You need **composability** (this script is called by another script)
3. The API is **obscure/undocumented** (agent doesn't know it well)
4. You need **speed** (agent round-trips add latency)

For AMD Dev Cloud specifically — the DigitalOcean API is extremely well-known, Claude Code handles it natively, so almost everything in `ww/amd_dev_cloud/` is a candidate for deletion in favor of `claude "do X on my droplet"`.

## What to Actually Keep as Code

From your `ww` repo, the things worth keeping as scripts are:

- **GPU benchmark harness** — complex, needs exact reproducibility
- **Training job submission** — state machine, retry logic, cost control
- **SSH tunnel setup** — fiddly, you run it 10x/day, muscle memory
- **Dataset pipelines** — deterministic transforms, versioned

Everything that's just "call this API and show me the result" → delete and let the agent do it.

## Practical Setup for This

```bash
# ~/.zshrc or ww config
export DIGITALOCEAN_TOKEN=$(cat ~/.secrets/do_token)

# One alias to rule them all
alias amd='claude --system "You manage my AMD Dev Cloud droplet via DigitalOcean API. Token is in env DIGITALOCEAN_TOKEN. Always confirm before destructive actions."'

# Usage
amd "what snapshots do I have?"
amd "create a snapshot of droplet amd-mi300x right now"
amd "my droplet is 192.168.1.x, what's its current status?"
```

This is genuinely more powerful than `snapshots.py` because the agent can chain operations, handle errors, and adapt — things your fixed wrapper can't do without more code.

**The meta-point:** The right question isn't "should I write this script?" but "is this task worth crystallizing into code, or should it stay fluid in agent-space?" Most ops tasks belong in agent-space. Only graduate them to code when they earn it through repetition and reliability requirements.