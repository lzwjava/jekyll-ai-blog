---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: ESLint 与 TSLint 核心差异详解
translated: true
type: note
---

以下是 TSLint 和 ESLint 之间的主要区别：

**1. 语言聚焦 (Language Focus)**

- **TSLint**: 专门为 TypeScript 设计
- **ESLint**: 最初为 JavaScript 设计，但现在通过 `@typescript-eslint/parser` 支持 TypeScript

**2. 维护状态 (Maintenance Status)**

- **TSLint**: 2019 年宣布弃用 (Deprecated)，不再维护
- **ESLint**: 活跃维护并持续开发中

**3. 性能 (Performance)**

- **TSLint**: 通常较慢，直接使用 TypeScript 的 compiler API
- **ESLint**: 在大多数场景下更快，解析更高效

**4. 生态系统与插件支持 (Ecosystem & Plugin Support)**

- **TSLint**: 生态系统较小，可用的插件较少
- **ESLint**: 拥有庞大的生态系统，包含数千个插件和配置（例如 Prettier 集成、React 规则、accessibility 规则等）

**5. 配置 (Configuration)**

- **TSLint**: 使用 `tslint.json`
- **ESLint**: 使用 `.eslintrc.json`（或 .js、.yml 变体）

**6. 规则覆盖 (Rule Coverage)**

- **TSLint**: 仅限 TypeScript 特定规则
- **ESLint**: 涵盖 JavaScript + TypeScript，以及特定框架的规则（React、Vue、Angular）

**7. 社区与未来 (Community & Future)**

- **TSLint**: 已停止的项目，没有未来开发计划
- **ESLint**: 行业标准，随着新的 JavaScript/TypeScript 特性不断演进

**为什么发生这种转变**: TypeScript 团队和 TSLint 维护者决定，与其维护两个独立的 linting 工具，不如将精力集中在支持 TypeScript 的 ESLint 上。这为社区提供了一个强大且维护良好的工具，以满足所有 JavaScript 和 TypeScript 的 linting 需求。
