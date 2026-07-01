---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 从 Angular 14 开始的最简升级路径
translated: true
type: note
---

**Question:** 在 Angular 14 到 21 之间，对于一个仍在使用 Webpack 等工具的 Angular 14 项目，我们可以轻松升级到哪个版本？

**Answer:**

您当前的项目使用的是 **Angular 14**（开发和生产构建默认均使用 Webpack）。

Angular 团队在 **Angular 16** 中引入了实验性的基于 esbuild 的构建，并在 **Angular 17** 中正式推出了 **Vite + esbuild** application builder（最初为可选，后成为新项目的默认选项）。

即便是在 **Angular 21**（2026 年 2 月的最新版本）中，**基于 Webpack 的 builder 仍然完全稳定且受到官方支持**。升级到 Angular 21 后，您可以继续使用经典的 `browser` builder (Webpack) —— 并没有强制迁移到 Vite/esbuild 的要求。

然而，为了从 Angular 14 开始在 **保留 Webpack** 的前提下实现 **最简单、最安全的升级路径**（对构建配置改动最小，无需处理新 builder 的迁移问题），最佳的中转版本是：

- **Angular 15 或 Angular 16** —— 从 14 升级非常直接（大部分通过 `ng update` 自动完成），默认仍 100% 使用 Webpack，引入了 standalone components（可选）等实用特性，且不会对构建系统产生破坏性改动。
- **Angular 17** —— 依然非常容易，但这是第一个存在新 Vite/esbuild builder 的版本（新项目默认使用）。从旧版本升级的现有项目除非您显式进行迁移，否则会 **保持使用 Webpack**。
- **Angular 18+ (直至 21)** —— 使用官方 schematics 升级依然顺畅，但从 Angular 18 开始，`ng update` 过程有时会提示/鼓励迁移到新的 builder。您可以选择 **拒绝 (decline)** 并继续保留 Webpack。

### 推荐的升级策略（保留 Webpack 的最简路径）

1. **Angular 14 → Angular 16** (甚至可以直接到 17)
   - 步子小，破坏性改动极少
   - Webpack 保持原样且为默认设置
   - 您可以获得现代特性（standalone components 趋于稳定、改进的 hydration、更强的 typing 等）
   - 命令：`ng update @angular/cli @angular/core`（一次升级一个大版本最安全）

2. 然后 **Angular 16/17 → Angular 21** (或者根据偏好停在 18/19/20)
   - 重复使用 `ng update`
   - 当询问是否迁移到新的 application builder (Vite/esbuild) 时 → **选择 no** 以保留 Webpack
   - 旧的 builder 在 2026 年仍受完全支持 —— 无需急于更改

### 快速总结表

| 目标版本 | 从 14 升级的难度 | 默认是否仍使用 Webpack？ | 备注 / 难度原因 |
| ---------------- | ---------------------------- | -------------------------------- | -------------------------- |
| Angular 15 | 非常容易 | 是 | 改动极小，良好的过渡步骤 |
| Angular 16 | 非常容易 | 是 | 引入 esbuild 预览（仅限手动开启） |
| Angular 17 | 容易 | 是（针对升级的项目） | Vite/esbuild 仅对*新*项目是默认项 |
| Angular 18–19 | 容易–中等 | 是（如果拒绝迁移） | 会出现新 builder 的迁移提示 |
| Angular 20–21 | 中等 | 是（如果拒绝迁移） | 默认配置更现代，但 Webpack 仍受支持 |

**2026 年 2 月的结论：**
您可以安全地一路升级到 **Angular 21** 并 **继续使用 Webpack** —— 只需要在 `ng update` 过程中拒绝任何向新 Vite/esbuild builder 迁移的提示即可。
如果您希望路径最平滑且几乎没有构建相关的意外，请先升级到 **Angular 16 或 17**（仍处于纯 Webpack 时代），稳定后再跳转到最新版本 (21) 并选择不使用新 builder。

通过这种方式，您可以在不触动构建系统的情况下，获得安全修复、性能改进和现代 Angular 特性。

**References:**

- [Angular Roadmap](https://angular.dev/roadmap)
- [Migrating to new build system (Webpack still supported)](https://angular.dev/tools/cli/build-system-migration)
- [Angular versioning and releases](https://angular.dev/reference/releases)
- [Angular Is Moving from Webpack to Vite (via esbuild)](https://norato-felipe.medium.com/angular-is-moving-from-webpack-to-vite-via-esbuild-what-it-means-for-you-87e3b7804639)
