---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Angular 代码检查迁移：从 TSLint 到 ESLint
translated: true
type: note
---

是的，你的理解完全正确！以下是关于这些过渡过程的详细说明：

**Webpack**：从 Angular 2+ 开始，包括 Angular 9 和 Angular 14，Angular 一直使用 webpack 作为其底层的 bundler。在这两个版本之间，这一点没有改变。

**TSLint → ESLint 过渡**：这是正确的！

- **Angular 9 及更早版本**：使用 TSLint 来对 TypeScript 代码进行 linting
- **Angular 11**：TSLint 被正式弃用（deprecated），Angular 团队建议迁移到 ESLint
- **Angular 12+**：新项目开始默认通过 `@angular-eslint` 使用 ESLint
- **Angular 14**：继续使用 ESLint（TSLint 支持已被完全移除）

这次切换是因为 TSLint 的维护者在 2019 年宣布弃用该项目，并建议转向 ESLint。Angular 团队创建了 `@angular-eslint`，以为 ESLint 提供针对 Angular 的专用 linting 规则。

如果你正在将一个旧的 Angular 9 项目迁移到 Angular 14，作为升级过程的一部分，你需要从 TSLint 迁移到 ESLint。Angular 团队提供了迁移 schematics 来帮助自动完成这一过渡。