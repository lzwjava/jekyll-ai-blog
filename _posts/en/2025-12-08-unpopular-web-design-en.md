---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Web Design Opinions
translated: false
type: note
---

Question: What are some unpopular or controversial opinions about web design and web development technology?

Answer:

Here are some genuinely unpopular (often down-voted or heavily debated) opinions in the modern web design and front-end development community as of 2025. These are things many experienced developers quietly believe but rarely say out loud in public forums:

- **Tailwind CSS and utility-first frameworks have made most designers worse at actual CSS**
  Most “Tailwind experts” can’t write maintainable custom CSS without it and have no understanding of specificity, cascade, or architecture. The framework hides complexity until you need to customize anything non-trivial, then everything falls apart.

- **Figma killed good interface design**
  Endless prototyping, auto-layout abuse, and component obsession have produced a generation of UIs that look polished but feel soulless. Everyone copies the same Apple/Google-inspired patterns because Figma makes it too easy.

- **Dark mode is mostly performative and often harms readability**
  True black backgrounds with bright white text have lower perceived contrast for many people. “System preference” default is a cop-out — most apps should pick one mode and optimize for it instead of shipping two half-baked themes.

- **90% of websites don’t need JavaScript frameworks (React, Vue, Svelte, etc.)**
  The performance, bundle size, and complexity penalty is unjustifiable for marketing sites, blogs, documentation, portfolios, and most SaaS dashboards. Vanilla HTML + tiny JS (or even Alpine.js/HTMX) is faster and more maintainable.

- **“Design systems” are often over-engineered bureaucracy generators**
  Giant Storybook libraries with hundreds of components slow teams down more than they help. Most companies would ship faster with a well-named CSS classes and a loose style guide.

- **Framer Motion / fancy scroll animations are accessibility red flags**
  Preferring `scroll-snap` abuse, parallax, and lenis smooth-scroll makes sites nauseating for vestibular-disorder users and is often just visual noise disguised as “premium feel.”

- **Webflow and no-code tools create terrible code and lock-in**
  The generated markup and CSS are bloated, semantically poor, and nearly impossible to migrate away from. They’re great for prototypes, terrible for anything meant to last >2 years.

- **Mobile-first is outdated — most users are on large phones or desktops now**
  Starting from 320 px breakpoints leads to cramped desktop layouts. “Content-out” or “desktop-down” often produces better hierarchy for the actual devices people use in 2025.

- **“Above the fold” still matters enormously and pretending it doesn’t is cope**
  If your hero text isn’t readable without scrolling on a laptop screen, you’ve already lost half your visitors. Layout shift metrics have made people forget basic human impatience.

- **Most “modern” fonts (Inter, Satoshi, etc.) are overused and ugly up close**
  They look great at 14 px body text on Retina screens but become blurry or inconsistent on Windows/non-Retina displays. System fonts (-apple-system, Segoe UI, Roboto) are still king for readability.

- **AI-generated websites (e.g., Dora, Framer AI) will always feel slightly “off”**
  They get 80% there instantly but the last 20% (micro-interactions, edge cases, brand voice) still requires human taste that AI doesn’t have yet.

- **The hatred of skeumorphism was an overcorrection**
  Flat design went too far. Subtle depth, texture, and realistic metaphors (buttons that look pressable) often improve affordance and delight.

These opinions tend to trigger strong reactions in design Twitter/Reddit/Dribbble circles, which is exactly why they remain unpopular despite being held by many senior practitioners.
