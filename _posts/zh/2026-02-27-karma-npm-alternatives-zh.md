---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Karma NPM 软件包及其替代方案
translated: true
type: note
---

**问题：** Karma 相关的 npm 包有哪些？

**回答：**

Karma（包名：**karma**）是一个流行的（但现在已**deprecated**）JavaScript 测试运行器，用于在真实浏览器中执行测试。它有一个庞大的相关 npm 包生态系统，大多是针对框架、浏览器、reporter、preprocessor等的**plugins**。

注意：截至 2024–2026 年，Karma 项目已被正式弃用，不再接收新功能或一般 bug 修复。社区推荐迁移到现代替代品，如 **Web Test Runner**、**Jest** 或 **Vitest**。

### 核心包

- **karma**
  → 主要的测试运行器本身
  → npmjs.com/package/karma

### 最常用的相关包（典型的 Angular / 经典设置）

- **karma-jasmine** — Jasmine 测试框架的适配器
- **jasmine-core** — 实际的 Jasmine 库（通常与之一同安装）
- **karma-chrome-launcher** — 启动 Chrome / Chromium
- **karma-firefox-launcher** — 启动 Firefox
- **karma-coverage** — 使用 Istanbul 的代码覆盖率报告

### 其他流行 / 经典 Karma 插件

- **karma-mocha** — Mocha 的适配器
- **karma-qunit** — QUnit 的适配器
- **karma-junit-reporter** — JUnit XML reporter（CI / Jenkins 友好）
- **karma-html-reporter** — 漂亮的 HTML 报告
- **karma-spec-reporter** — 干净的 spec 风格控制台输出
- **karma-browserify** — Browserify 集成
- **karma-webpack** — Webpack preprocessor（在旧项目中非常常见）
- **karma-sourcemap-loader** — 处理 source map
- **karma-ng-html2js-preprocessor** — 将 Angular 模板编译为 JS

### 搜索更多

npm 上有**超过 1000 个**与 Karma 相关的包。您可以通过搜索发现它们：

```bash
npm search karma
# 或更具体地
npm search karma-plugin
```

大多数插件遵循以下命名模式之一：

- `karma-*`（例如 karma-jasmine、karma-chrome-launcher）
- 在 package.json 中包含关键字 `karma-plugin`

如果您在 2026 年启动新项目，请考虑使用 **Jest**、**Vitest** 或 **@web/test-runner** 而非从 Karma 开始。

**参考：**

- [https://www.npmjs.com/package/karma](https://www.npmjs.com/package/karma)
- [https://www.npmjs.com/search?q=karma](https://www.npmjs.com/search?q=karma)
- [http://karma-runner.github.io/](http://karma-runner.github.io/)
- [https://www.npmjs.com/package/karma-coverage](https://www.npmjs.com/package/karma-coverage)
