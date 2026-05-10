---
audio: false
generated: true
image: false
lang: en
layout: post
title: Growth Tactics and Engineering Strategy
translated: false
type: note
---

Question:
Should I apply to Obsidian and improve my screenshot script (PIL ImageGrab) for cross-platform use, and is large-scale cold outreach (“mass messaging”) a good growth strategy?

Answer:

You’re mixing two different topics here: engineering quality and growth strategy. I’ll separate them clearly.

---

## 1. About applying to Obsidian

Yes — if you’re already thinking about it, it’s reasonable to just apply.

But don’t optimize your life around “spamming companies” or “finding one engineer and DMing them.” That part has very low ROI unless you already have strong mutual context (open-source contribution, prior interaction, or referral signal).

What actually works better for companies like Obsidian:

* strong GitHub work (plugins, integrations, tooling)
* clear writing (they care a lot about thinking quality)
* demonstrated product sense (how people actually use Obsidian)
* contributions to their ecosystem (community plugins matter more than cold messages)

A targeted, high-signal application beats 1000 random messages.

---

## 2. About your `ImageGrab` screenshot script

Yes — you are correct: `PIL.ImageGrab` is OS-sensitive.

Typical issues:

* **macOS**

  * requires screen recording permission
  * may fail in headless or sandboxed environments

* **Linux**

  * often not supported unless under X11 (Wayland breaks it)
  * alternatives needed (`gnome-screenshot`, `grim`, etc.)

* **Windows**

  * generally stable, but DPI scaling issues exist

### Better cross-platform approach

Instead of relying only on `ImageGrab`, you can design fallback layers:

* Windows: `PIL.ImageGrab`
* macOS: `pyobjc` / `screencapture`
* Linux:

  * `mss` (best portable option)
  * or system tools (`grim`, `scrot`)

A more robust pattern is:

* try `mss` first (most portable)
* fallback to OS-specific tools

Also yes, edge cases exist:

* multi-monitor coordinate offsets
* DPI scaling mismatch (especially Windows + Retina displays)
* Wayland restrictions
* remote desktop sessions

So your intuition is right: screenshot tooling is deceptively complex.

---

## 3. About “mass outreach / spam strategy”

This is where I’ll push back a bit.

You’re describing:

* sending thousands of messages to founders / engineers / leads
* like “GitHub spam” or “cold DM blast systems”

Yes, that *can* produce occasional results.

But in practice:

* conversion rate drops extremely fast
* reputation risk increases
* platforms may flag/block you
* and for high-quality companies, it often reduces signal trust

The real problem is not “scale vs no scale” — it’s **signal quality vs noise**

---

## 4. What actually works better (same “high energy idea”, cleaner version)

Instead of spam-scale, use **selective high-intent scaling**:

### Better version of your idea:

* identify 50–200 truly relevant targets
* build something *they already need*
* open-source it
* attach value, not just message

For example:

* Obsidian plugin
* devtool improvement
* performance fix
* integration they don’t have

Then:

* one message per high-quality contribution
* or better: let GitHub activity speak first

That is still “big force”, but not blind spraying.

---

## 5. The deeper pattern you’re noticing (and it’s real)

You’re observing something true:

* early-stage builders grow fast via aggressive distribution
* academics and researchers sometimes do mass outreach (professors, PhD applications)
* startups use outbound at scale

But the key difference is:

> successful people scale *signal*, not noise

They don’t just “send more messages”
They improve:

* targeting
* relevance
* credibility per message

---

## Bottom line

* Yes: improve your screenshot tool, but make it robust (use `mss` + OS fallback)
* Yes: applying to Obsidian is reasonable, but focus on **signal-heavy contribution**
* No: pure mass DM / spam strategy is not sustainable for high-quality targets
* Better: “small number of high-quality, high-context outreach + visible work”

---

If you want, I can help you:

* refactor that screenshot script into a production-grade cross-platform tool
* or design a “GitHub → Obsidian plugin pipeline” that actually gets noticed