---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Angular NGCC Ivy 兼容性桥接器
translated: true
type: note
---

**Question:** Angular 中的 NGCC 是做什么用的？

**Answer:**

**NGCC** 全称是 **Angular Compatibility Compiler**（Angular 兼容性编译器）。

它是 Angular 中的一个工具（主要在 **Angular 9** 到 **Angular 15** 期间使用），旨在帮助使用新 **Ivy** 渲染引擎的应用，能够正常使用那些仍以旧版 **View Engine**（Ivy 之前的旧渲染系统）编译的 Angular 库。

### NGCC 的具体作用

- 当你从 npm 安装了一个以 **View Engine** 格式发布的 Angular 库时（这在 2020–2021 年之前非常普遍），
- NGCC 会在你的**项目构建过程中**（或者有时通过安装后的 `node_modules` 处理过程）**自动将**该库的代码转换为 Ivy 兼容格式。
- 这种转换通过转换库的 metadata 和渲染指令来实现，从而使 Ivy 能够正确理解并使用它们。

如果没有 NGCC，基于 Ivy 的应用在依赖非 Ivy (View Engine) 库时，将无法编译或运行。

### 重要历史背景

- Angular 9 (2020) → Ivy 成为 **default** 渲染器，但为了向后兼容加入了 NGCC。
- Angular 12 → View Engine 从框架本身中移除（只有库仍然需要 NGCC）。
- **Angular 16** (2023 年 5 月) → **NGCC 被完全移除**。
  → View Engine 格式的库不再有效。
  → 所有库现在必须以 Ivy 格式发布（自 2021–2022 年以来，大多数主流库都已更新）。

### 现状 (2026)

- 如果你使用的是 **Angular 16 或更高版本**，你将不再看到也不再需要 NGCC。
- 如果你的构建因 View Engine 或缺失 NGCC 的相关错误而失败 → 这意味着你依赖了一个从未迁移到 Ivy 的非常陈旧且疏于维护的库。
- 这种情况下的解决方案：更新或替换该有问题的依赖项。

简而言之：
NGCC 是一个**临时桥梁**，让生态系统在 2020–2023 年间实现了从 View Engine 到 Ivy 的平滑过渡。它目前已经过时，并已从 Angular 16 中移除。

**References:**

- [Angular Update Guide - v16](https://update.angular.dev/?v=15.0-16.0)
- [Angular Changelog](https://github.com/angular/angular/blob/main/CHANGELOG.md)
- [Blog: The Removal of Angular Compatibility Compiler (ngcc) in Angular 16](https://katsuba.dev/articles/the-removal-of-angular-compatibility-compiler-ngcc-in-angular-16)
- [Official Angular blog on library distribution improvements](https://blog.angular.dev/upcoming-improvements-to-angular-library-distribution-76c02f782aa4)
