---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Angular 旧版代码扫描工具已弃用
translated: true
type: note
---

In Angular 9 和更早的 Angular 版本中，**TSLint** 和 **Codelyzer** 协同工作，用于强制执行代码质量和 Angular 特定的最佳实践：

## TSLint

TSLint 是一个针对 TypeScript 代码的静态分析工具，它：

- 检查代码质量问题、bugs 和样式不一致
- 在整个 TypeScript 文件中强制执行编码规范
- 为格式化、命名约定（naming conventions）和代码模式（code patterns）提供可配置的规则
- 帮助维护代码库的一致性

## Codelyzer

Codelyzer 是一套专门为 Angular 应用程序设计的 TSLint 规则，它：

- 强制执行 Angular style guide 建议
- 检查 component、directive 和 service 的命名约定
- 验证 template 语法和最佳实践
- 确保正确使用 Angular decorators 和 lifecycle hooks
- 捕获 Angular 特有的 anti-patterns

## How They Worked Together

你可以在 `tslint.json` 文件中配置它们：

```json
{
  "extends": ["tslint:recommended", "codelyzer"],
  "rules": {
    "component-class-suffix": true,
    "directive-selector": [true, "attribute", "app", "camelCase"],
    // other rules
  }
}
```

## Important Note: They're Deprecated

TSLint 和 Codelyzer 现在都已 **deprecated**：

- TSLint 在 2019 年被宣布弃用
- Angular 团队已迁移到 **ESLint**，并使用 **angular-eslint** 作为替代方案
- Angular 11+ 默认使用 ESLint

如果你正在处理 Angular 9 或更旧的项目，可能仍会遇到这些工具，但对于现代 Angular 开发，你应该迁移到 ESLint 和 angular-eslint 来实现 linting 功能。
