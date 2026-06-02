---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Yin Wang Blog Technical Stack Analysis
translated: false
type: note
---

The website (<https://www.yinwang.org/>, titled "当然我在扯淡") appears to be a custom-built blog. Based on the provided HTML source:

- **Framework**: It's primarily built with **Vue.js** (version 3 likely), evident from Vue-specific attributes like `data-v-app`, `data-v-[hash]` for scoped CSS, and component references (e.g., `HomeView`, `PostView`, `router-link-active` for Vue Router handling navigation).
- **Build tool**: **Vite** is used for bundling and development, shown by the favicon (`/vite.svg`), module-preloaded scripts with hashed filenames (e.g., `/assets/index-DS_1rR7p.js`), and the overall asset structure typical of Vite's output.
- **Styling**: **Tailwind CSS** for utility-first classes (e.g., `bg-gray-50 dark:bg-gray-900`, `flex items-center`, responsive prefixes like `sm:px-4`).
- **Other notes**: No server-side rendering indicators (e.g., no Nuxt.js traces), so it's likely a static site or client-side rendered SPA. The content (posts, tags, pagination) suggests a simple custom setup for a personal blog, possibly with Markdown for post content.

It's **not all manually written**—the HTML is auto-generated during the build process from Vue components and templates. The core logic (routing, components) is coded in JS/TS, but the final output is optimized static files. No evidence of a full static site generator like Hugo or Jekyll; it's more of a lightweight Vue + Vite project.

[当然我在扯淡](https://www.yinwang.org/)
