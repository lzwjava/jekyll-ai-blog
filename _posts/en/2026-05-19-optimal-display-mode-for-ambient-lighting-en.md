---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimal Display Mode for Ambient Lighting
translated: false
type: note
---

Question: Is "system mode" better than dark mode or light mode? Should dark/light mode selection be based on ambient lighting around the monitor/laptop rather than time of day?

Answer:

## Your Core Intuition Is Correct

You're right on both points:

1. **The choice should depend on ambient light, not time of day** — science backs this up fully.
2. **System mode is the best practical setting** — because it delegates the decision to the OS, which can use sensors or scheduled rules based on actual ambient conditions.

---

## Why Ambient Light Matters More Than Time

The setting in which you use your device plays a crucial role. Ambient lighting interacts directly with screen output, influencing perceived brightness and contrast. The guidance from vision researchers is clear: use light mode in well-lit rooms and dark mode in dim or nighttime settings.

Interestingly, research flips a common assumption: a study from Østfold University College in Norway found that dark mode was actually **more effective at reducing eye fatigue in bright ambient lighting** than in dim lighting — the opposite of what most people expect.

And for reading specifically, there is no scientific evidence that dark mode physically reduces strain on eye muscles more than light mode. In fact, for reading long blocks of text, the human eye generally prefers light mode. However, dark mode is statistically proven to reduce subjective fatigue in low-light environments by reducing overall brightness hitting the retina.

Research from Nielsen Norman Group found that light mode won across all dimensions for visual-acuity and proofreading tasks, regardless of age.

---

## So: Dark, Light, or System Mode?

| Situation | Best Mode |
|---|---|
| Outdoors / bright natural light | **Light mode** |
| Indoor bright office lighting | **Light mode** |
| Dim room / evening indoors | **Dark mode** |
| Night, in bed, low light | **Dark mode** |
| Moving between environments | **System mode** ✅ |

**System mode wins** because:
- Modern OS (macOS, Windows, iOS, Android) can auto-switch based on time of day, which roughly approximates ambient light changes (sunrise/sunset).
- Some devices (especially phones) have ambient light sensors that influence this further.
- You don't have to think about it — it adapts automatically.

The key insight is: **it's not about the clock, it's about the light around your screen.** System mode is simply the best automation of that principle without requiring you to manually toggle every time you move.

---

## Context from Zhiwei Li's Notes

From reading the dark-mode related posts on your notes page at lzwjava.github.io, the background is about e-commerce and dark mode on desktop/laptop. Key takeaways from those notes:

- Very few major e-commerce websites offer a native, built-in dark mode toggle on their desktop website. This reflects a deliberate choice by most large retailers.
- From an analysis of the top 100 apps, only about half support dark mode, and even among those, roughly 12% require users to dig into settings to enable it. Apps focused on increasing transactions (like most major e-commerce platforms) tend not to prioritize dark mode.
- The recommended workaround for websites that don't support dark mode natively is to use a browser extension like **Dark Reader**, which applies dark theming to any site.

---

## Practical Recommendation for You

1. **Set OS to System/Auto mode** — let it handle the base switching.
2. **Install Dark Reader** browser extension for websites that ignore your OS theme.
3. **Trust your eyes over the clock** — if you're in a bright environment, switch to light regardless of the time; if it's dim, go dark.
4. **Adjust screen brightness** to match ambient light as well — this matters as much as the color scheme.

References:

- [Dark Mode vs Light Mode – Eye Strain Research (Alibaba Insights)](https://www.alibaba.com/product-insights/dark-mode-vs-light-mode-which-is-actually-better-for-eye-strain.html)
- [Dark vs Light Mode Eye Fatigue Study – IARIA 2024](https://personales.upv.es/thinkmind/dl/conferences/achi/achi_2024/achi_2024_3_150_20069.pdf)
- [Why Use Light Mode Over Dark Mode – XDA Developers](https://www.xda-developers.com/why-use-light-mode-over-dark-mode/)
- [Dark Mode vs Light Mode – Nielsen Norman Group](https://www.nngroup.com/articles/dark-mode/)
- [Does Dark Mode Prevent Eye Strain? – Lens.com](https://www.lens.com/questions-answered/does-using-dark-mode-prevent-digital-eye-strain/)
- [E-Commerce Dark Mode Status in 2026 – lzwjava.github.io](https://lzwjava.github.io/e-commerce-dark-mode-status-in-2026-en)
- [Dark Mode Rare in Desktop Shopping – lzwjava.github.io](https://lzwjava.github.io/dark-mode-rare-in-desktop-shopping-en)