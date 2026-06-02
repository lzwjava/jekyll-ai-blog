---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp Terminal Without AI Features
translated: false
type: note
---

**Question:** Do some people disable Warp's AI/agent functionality and use it purely as a terminal?

**Answer:**

Yes, absolutely. This is a documented and common usage pattern. Several reasons people do it:

---

## Why People Disable Warp AI

**Privacy / corporate policy** — Warp's AI sends your command context to their servers. At banks and enterprises (your exact situation), this is often blocked or policy-forbidden. Many engineers disable it purely for compliance.

**It gets in the way** — The AI suggestions pop up uninvited. For experienced engineers who type fast and know what they want, the autocomplete overlay is noise, not signal.

**They already have better AI** — If you're using Claude Code or a custom CLI agent (`ww`, `zz`), Warp's built-in AI is redundant and weaker.

---

## How to Actually Disable It

```
Settings → AI → uncheck "Enable AI features"
```

Also worth disabling:
```
Settings → Features → Disable "Warp Drive" (cloud command sharing)
Settings → Privacy → set telemetry to minimal
```

After this, Warp behaves as a pure terminal — blocks, splits, tabs, workflow search still work fine. The AI layer is opt-in infrastructure, not baked into the renderer.

---

## The Rust/GPU Renderer Is the Real Value

Warp is written in Rust with a GPU-accelerated renderer (Metal on Mac). That's what makes it feel snappier than iTerm2 or Terminal.app — and that has nothing to do with AI. People who care about rendering performance keep Warp for this reason alone.

---

## Community Sentiment

On Reddit (`r/commandline`, `r/MacOS`) and Hacker News, the split is roughly:

- **"I use Warp with AI off, it's the best iTerm2 replacement"** — common
- **"I won't use it because it requires a login"** — the bigger complaint actually
- **"The block UI alone is worth it"** — frequent

The **login requirement** is the more controversial issue than AI — Warp requires an account even for local use (as of 2024). Some people reject it entirely for that reason. Others accept it and disable AI.

---

## Your Specific Situation

Given you're at a global bank via contract:

- AI features should likely be off regardless
- Warp's block-based UX + splits still give you value over iTerm2
- Your actual AI layer is Claude Code / your own CLI agents — Warp is just the glass

Treat it as **a better terminal renderer with good UX primitives**, and disable everything that phones home.
