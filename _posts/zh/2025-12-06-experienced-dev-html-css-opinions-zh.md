---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 经验丰富的开发者对HTML CSS有争议的看法
translated: true
type: note
---

问题：经验丰富的开发者对 HTML 和 CSS 有哪些不流行的看法？

回答：

以下是一些关于 HTML/CSS 的真正不受欢迎（或至少有争议）的观点，你会经常从经验丰富的UI开发者那里听到，即使主流社区不同意：

- **CSS 是一种糟糕的编程语言，根本不应该成为一种编程语言**
  层叠是一个错误。全局作用域、不可预测的特异性冲突以及无法真正封装样式，使得没有严格的纪律（BEM、SMACSS 等）大规模的 CSS 难以维护。许多资深开发者认为，我们从一开始就应该构建一个真正的组件作用域样式系统，而不是在20年后才加上 Shadow DOM。

- **语义化 HTML 被严重高估了**
  除了可访问性（这很重要）之外， `<section>`、`<article>`、`<main>` 和 `<div class="article">` 之间的差异在2025年对浏览器和搜索引擎来说毫无意义。谷歌多次表示，它几乎不使用语义化 HTML 进行排名。大多数“语义纯粹主义者”只是盲目模仿。

- **Tailwind 和 utility-first CSS 是大规模编写 CSS 的唯一理智方式**
  大多数人仍然使用组件范围的 CSS（CSS Modules、styled-components 等），但越来越多的（并且非常直言不讳的）少数人认为编写实际的 CSS 文件是疯狂的，并且 utility classes 在各方面都更优越：更快的原型设计、一致的设计系统、无需命名、更容易重构。

- **CSS-in-JS 是一个巨大的错误，我们现在都在为此付出代价**
  运行时样式注入会损害性能（尤其是在 React 上的hydration），包会变得非常大，并且你失去了单独缓存 CSS 的能力。许多经历过 styled-components/Emotion 时代的人现在都说“再也不来了”。

- **对于几乎所有情况，Flexbox 都优于 CSS Grid**
  Grid 在理论上很优雅，但实际上大多数布局都是一维的（列表、卡片、导航栏）。Flexbox 更简单、更可预测，并且需要的hack更少。Grid 在90% 的时间里都是杀鸡用牛刀。

- **在2025年，你不需要 CSS reset 或 normalize**
  现代浏览器已经足够一致，完整的重置只会增加臃肿，并与浏览器完全合理的默认设置作斗争。几行 `box-sizing: border-box` 和字体继承修复是大多数项目所需的全部。

- **BEM 很糟糕，会创建难以阅读的类名**
  `.header__nav__item--active` 是一堆只写一次、从不阅读的垃圾。大多数使用 BEM 多年的团队已经放弃它，转而使用 utility classes 或 scoped component styles。

- **HTML 应该保持简单，我们不应该添加脚本功能**
  这是来自“HTML 旨在用于文档”人群的一个有争议的观点：`<canvas>`、Web Components、`<dialog>`、`<template>` 等将其变成了 Frankenstein 应用平台。我们应该让 HTML 保持愚蠢，并从一开始就在 JS 框架中完成所有事情。

- **对于80% 的网站，不使用框架编写原始 HTML/CSS 比 React/Vue/Svelte 更快，并能产生更好的结果**
  大多数网站仍然主要是静态内容。启动一个完整的 SPA 框架会增加兆字节和复杂性，而没有任何好处。

这些观点往往非常两极分化——你会在 Reddit/Hacker News 上因为其中一些观点而获得大量差评，但你会发现许多资深开发者默默地点头表示赞同。
