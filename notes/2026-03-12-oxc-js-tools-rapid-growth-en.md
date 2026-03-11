---
audio: false
generated: true
image: false
lang: en
layout: post
title: OXC Rapid Growth in JavaScript Tools
translated: false
type: note
---

Question: How is oxc.rs being adopted in the JavaScript ecosystem?

Answer:

## OXC Adoption in the JavaScript Ecosystem

OXC has seen strong and rapid adoption since its initial release in late 2023. Here is a breakdown across different dimensions:

---

### 🏢 Notable Company Adopters

OXC is thankful for its 5,200 early adopters and for companies such as:
- **Shopify**, where the front-end platform team uses Oxlint in the Shopify admin console.
- **Airbnb**, where they use multi-file analysis (`oxc/no-barrel-file` and `import/no-cycle`) on their 126,000+ files, completing in just 7 seconds on CI.

Other notable users include **Preact**, **ByteDance**, and **Shopee** for linting, while **Rolldown** and **Nuxt** use OXC for parsing, and **Nova**, **swc-node**, and **knip** use `oxc_resolver` for module resolution.

---

### 📦 NPM Downloads

The `oxc-parser` npm package alone has **~2.6 million weekly downloads** as of early 2026, indicating deep integration into downstream build tools and pipelines.

---

### 🔧 Tool-Level Adoption

**Oxlint (Linter)**

Oxlint reached its stable v1.0 release in June 2025, with a dedicated full-time maintainer and a growing core team. It now includes over **695 rules**, covering most plugins teams already use, with automated migration tooling available.

**Oxfmt (Formatter)**

Oxfmt now passes **100% of Prettier's JavaScript and TypeScript conformance tests**, making migration from Prettier nearly seamless with no formatting differences expected.

**Rolldown (Bundler — VoidZero)**

OXC powers the entire parsing, transformation, and minification pipeline of **Rolldown**, which is the next-generation bundler planned to replace Rollup inside **Vite** — one of the most popular frontend build tools today.

---

### 🌱 Ecosystem Integration

OXC also offers an AI migration skill (`npx skills add oxc-project/oxc --skill migrate-oxlint`) to help teams automatically migrate from ESLint configs to Oxlint, lowering the friction of adoption.

---

### ⚠️ Caveats / Still Maturing

- **Oxfmt** (formatter) and **Oxc Transformer** are still in alpha/beta stages.
- The JS plugin system for Oxlint is in early preview; performance optimizations are still being applied and multiple x speed-ups are expected over the coming months.
- Type-aware linting (alpha) relies on `tsgolint`, which is based on Microsoft's Go-based TypeScript rewrite (`typescript-go`), which will become TypeScript v7.0 — still experimental.

---

### Summary

OXC adoption is growing quickly, especially for **linting at scale** (Shopify, Airbnb), and is becoming **infrastructure-level** via Rolldown/Vite. The parser is broadly used across the ecosystem with millions of weekly downloads. The main gap remains in formatter and transformer maturity compared to well-established tools like Prettier and Babel.

References:

- [Oxlint v1.0 Stable — oxc.rs](https://oxc.rs/blog/2025-06-10-oxlint-stable)
- [GitHub — oxc-project/oxc](https://github.com/oxc-project/oxc)
- [oxc-parser on npm](https://www.npmjs.com/package/oxc-parser)
- [Oxlint JS Plugins Preview](https://oxc.rs/blog/2025-10-09-oxlint-js-plugins.html)
- [Type-Aware Linting Alpha](https://oxc.rs/blog/2025-12-08-type-aware-alpha)