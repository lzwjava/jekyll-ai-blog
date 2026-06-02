---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OXC 在 JavaScript 工具中的快速增长
translated: true
type: note
---

Question: oxc.rs 如何在 JavaScript 生态系统中被采用？

Answer:

## OXC 在 JavaScript 生态系统中的采用情况

自 2023 年末首次发布以来，OXC 就获得了强劲且快速的采用。以下是不同维度的细分：

---

### 🏢 知名公司采用者

OXC 感谢其 5,200 名早期采用者以及以下公司：
- **Shopify**，其前端平台团队在 Shopify admin console 中使用 Oxlint。
- **Airbnb**，他们在 126,000+ 个文件中使用多文件分析（`oxc/no-barrel-file` 和 `import/no-cycle`），在 CI 上仅用 7 秒完成。

其他知名用户包括 **Preact**、**ByteDance** 和 **Shopee** 用于 linting，而 **Rolldown** 和 **Nuxt** 使用 OXC 进行 parsing，**Nova**、**swc-node** 和 **knip** 使用 `oxc_resolver` 进行模块解析。

---

### 📦 NPM 下载量

截至 2026 年初，`oxc-parser` npm 包每周下载量约为 **~2.6 百万次**，表明其已深度集成到下游构建工具和管道中。

---

### 🔧 工具级采用

**Oxlint (Linter)**

Oxlint 于 2025 年 6 月发布稳定版 v1.0，并有专职全职维护者和不断壮大的核心团队。现在它包含超过 **695 条规则**，覆盖了团队已经使用的绝大多数插件，并提供自动迁移工具。

**Oxfmt (Formatter)**

Oxfmt 现在通过了 **Prettier 的 100% JavaScript 和 TypeScript 一致性测试**，从 Prettier 迁移几乎无缝，无需预期格式差异。

**Rolldown (Bundler — VoidZero)**

OXC 为 **Rolldown** 的整个 parsing、transformation 和 minification 管道提供动力，Rolldown 是下一代 bundler，计划取代 **Vite** 中的 Rollup——当今最受欢迎的前端构建工具之一。

---

### 🌱 生态系统集成

OXC 还提供 AI 迁移技能（`npx skills add oxc-project/oxc --skill migrate-oxlint`），帮助团队自动从 ESLint 配置迁移到 Oxlint，从而降低采用门槛。

---

### ⚠️ 注意事项 / 仍在成熟中

- **Oxfmt**（formatter）和 **Oxc Transformer** 仍处于 alpha/beta 阶段。
- Oxlint 的 JS 插件系统处于早期预览阶段；性能优化仍在应用中，预计未来几个月将实现多倍加速。
- 类型感知 linting（alpha）依赖于 `tsgolint`，后者基于微软的 Go 实现的 TypeScript 重写（`typescript-go`），将成为 TypeScript v7.0——仍处于实验阶段。

---

### 总结

OXC 的采用正在快速增长，尤其是在 **大规模 linting**（Shopify、Airbnb）方面，并通过 Rolldown/Vite 成为 **基础设施级**。parser 在整个生态系统中广泛使用，每周下载量数百万。主要差距仍在于 formatter 和 transformer 的成熟度，与 Prettier 和 Babel 等成熟工具相比。

参考资料：

- [Oxlint v1.0 Stable — oxc.rs](https://oxc.rs/blog/2025-06-10-oxlint-stable)
- [GitHub — oxc-project/oxc](https://github.com/oxc-project/oxc)
- [oxc-parser on npm](https://www.npmjs.com/package/oxc-parser)
- [Oxlint JS Plugins Preview](https://oxc.rs/blog/2025-10-09-oxlint-js-plugins.html)
- [Type-Aware Linting Alpha](https://oxc.rs/blog/2025-12-08-type-aware-alpha)
