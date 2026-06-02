---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Experienced Developers' Controversial HTML CSS Opinions
translated: false
type: note
---

Question: What are some unpopular opinions about HTML and CSS held by experienced developers?

Answer:

Here are some genuinely unpopular (or at least controversial) opinions about HTML/CSS that you’ll frequently see from battle-scarred front-end developers, even if the mainstream community disagrees:

- **CSS is a terrible programming language and should never have been one**
  The cascade was a mistake. Global scope, unpredictable specificity wars, and the inability to truly encapsulate styles make large-scale CSS unmaintainable without extreme discipline (BEM, SMACSS, etc.). Many senior devs believe we should have built a real component-scoped styling system from the beginning instead of bolting on Shadow DOM 20 years later.

- **Semantic HTML is massively overrated**
  Outside of accessibility (which matters), the difference between `<section>`, `<article>`, `<main>`, and `<div class="article">` is meaningless noise to browsers and search engines in 2025. Google has repeatedly said it barely uses semantic HTML for ranking. Most “semantic purists” are just cargo-culting.

- **Tailwind and utility-first CSS is the only sane way to write CSS at scale**
  The majority still uses component-scoped CSS (CSS Modules, styled-components, etc.), but a growing (and very vocal) minority believes writing actual CSS files is insane and that utility classes are superior in every way: faster prototyping, consistent design systems, no naming things, easier refactoring.

- **CSS-in-JS was a huge mistake and we’re all paying for it now**
  Runtime style injection kills performance (especially hydration on React), bundles get massive, and you lose the ability to cache CSS separately. Many who lived through the styled-components/Emotion era now say “never again.”

- **Flexbox is better than CSS Grid for almost everything**
  Grid is elegant in theory, but in practice most layouts are 1-dimensional (lists, cards, navbars). Flexbox is simpler, more predictable, and needs fewer hacks. Grid is overkill 90% of the time.

- **You don’t need a CSS reset or normalize in 2025**
  Modern browsers are consistent enough that a full reset just adds bloat and fights the browser’s perfectly reasonable defaults. A few lines of `box-sizing: border-box` and font inheritance fixes are all most projects need.

- **BEM is awful and creates unreadable class names**
  `.header__nav__item--active` is write-once-read-never garbage. Most teams that used BEM for years have abandoned it for utility classes or scoped component styles.

- **HTML should have stayed dead simple and we never should have added scripting capabilities**
  A controversial take from the “HTML was meant to be documents” crowd: `<canvas>`, Web Components, `<dialog>`, `<template>`, etc. turned it into a Frankenstein app platform. We should have kept HTML dumb and done everything in JS frameworks from the start.

- **Writing raw HTML/CSS without a framework is faster and produces better results than React/Vue/Svelte for 80% of websites**
  Most sites are still mostly static content. Spinning up a full SPA framework adds megabytes and complexity for no benefit.

These opinions tend to be very polarizing — you’ll get heavily downvoted for some of them on Reddit/Hacker News, but you’ll find plenty of senior devs quietly nodding in agreement.
