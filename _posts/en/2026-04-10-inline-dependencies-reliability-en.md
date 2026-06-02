---
audio: false
generated: true
image: false
lang: en
layout: post
title: Inline Dependencies for Reliability
translated: false
type: note
---

Searched codebase for "give a blog lesson about it", 22 results

Here's a blog lesson draft:

---

## Inline Your Dependencies: A Lesson from a Proxy Config

I recently simplified my Clash proxy configuration by removing an external rule provider and inlining the rules directly. It's a small change, but it illustrates a principle that applies far beyond proxy configs.

### The Before: External Dependency

```yaml
rule-providers:
  AIRule:
    type: http
    behavior: classical
    path: ./Rules/AI.yaml
    url: https://raw.githubusercontent.com/lzwjava/blog-source/.../AI.yaml
    interval: 1440
```

This looks clean. One line in the `rules` section — `RULE-SET,AIRule,Proxy` — handles all AI-related traffic. But hidden behind that elegance are several assumptions:

- GitHub is reachable at startup
- The URL still exists and hasn't moved
- The remote file hasn't changed in ways you don't want
- The cached local copy at `./Rules/AI.yaml` is fresh enough

Any one of these can fail silently. Your proxy rules break and you won't necessarily see an error — traffic just routes wrong.

### The After: Self-Contained

```yaml
rules:
  - DOMAIN-SUFFIX,claude.ai,Proxy
  - DOMAIN-SUFFIX,openai.com,Proxy
  - DOMAIN-SUFFIX,anthropic.com,Proxy
  - DOMAIN-SUFFIX,gemini.google.com,Proxy
  # ... etc
```

Verbose? Yes. But now the config is the single source of truth. It works offline, on first boot, in a Docker container, on a new machine — everywhere, always.

### The General Principle

External dependencies trade **convenience now** for **fragility later**. This shows up everywhere:

| Context | External dependency | Self-contained alternative |
|---|---|---|
| Proxy config | Remote rule file | Inline rules |
| CI pipeline | Download script from URL | Vendor the script |
| Frontend | CDN-hosted library | Bundle it |
| Docker image | `apt install` at runtime | Bake into image |
| Config | Env var fetched from remote | Local .env file |

The pattern is always the same: fetching something external at runtime introduces a point of failure outside your control.

### When External Dependencies Are Worth It

Inlining isn't always the right call. External dependencies make sense when:

- The ruleset is **large** (hundreds of IP CIDRs) and changes frequently
- You want **centralized updates** across many machines
- The dependency has a **stable, versioned URL** you control

In this case, the AI domain list was short (~15 entries), rarely changes, and I own the source anyway — so there was no real benefit to keeping it external.

### Takeaway

Before adding an external dependency, ask: *what happens if this is unavailable?* If the answer is "things break silently," consider whether you can just inline it. Self-contained systems are boring in the best way — they work the same way every time.
