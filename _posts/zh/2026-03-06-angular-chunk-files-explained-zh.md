---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular Chunk 文件详解
translated: true
type: note
---

Question: Angular Compiler CLI 中的 `chunk-xxx.js` 文件是什么？

Answer:

## Angular 中的 `chunk-xxx.js` 是什么？

### 概述

`chunk-xxx.js`（例如 `chunk-ABC123.js`、`0.chunk.js`、`common.chunk.js`）是由 Angular 的构建工具链在编译过程中生成的 **JavaScript bundle fragments**。Chunks 技术上不是 Angular 本身的一部分——它们是 Webpack（或在较新 Angular 版本中的 esbuild）的一部分，Angular 内部使用它来构建您的应用。当工具链将 TypeScript 文件转译为 JavaScript 时，它会创建代表应用各部分的“chunks”。

---

### Chunks 为什么存在？

Angular 的构建系统执行 **code splitting** —— 而不是将整个应用打包成单个 JS 文件，它将代码拆分成更小的片段（“chunks”），这些片段可以单独加载。这通过以下方式提升性能：

- 减少初始页面加载大小
- **仅在需要时** 加载代码（按需加载）
- 允许浏览器缓存独立的片段

---

### Chunk 文件类型

#### 1. **Lazy-Loaded Module Chunks**

应用 lazy loading 最简单的方式是使用 Angular Router 的内置功能，通过 `loadChildren`。基于使用的 `import()` 语句，Webpack 知道如何拆分 JS 文件，以便按需加载。当您服务或编译应用时，您会在控制台看到这些代码拆分的 JS 文件（chunks）。

例如：

```
products-products-module.js
orders-orders.module.js
```

#### 2. **Common Chunk (`common.js`)**

一旦您有一些共享部分——一个共享模块，其中包含被 products 和 orders lazy-loaded 模块都使用的组件——Angular CLI 默认会将所有共享代码（在至少两个位置使用的代码）分组到一个 `common.js` chunk 中。这通常是个好主意，因为共享代码被去重了。不过，请记住，这个 JS 文件 **在启动时加载**，这可能会影响应用的启动速度。

Common chunk 是所有超过一个 feature module 使用的组件的存放位置。例如，如果您有一个自定义 grid component 在自定义 grid module 中，并且您将这个 grid module 导入到 user 和 admin feature module 中，它就会进入 common chunk。

#### 3. **Named/Hash Chunks（例如 `chunk-XXXXX.js`）**

在 Angular 升级到版本 16 并使用 builder `@angular-devkit/build-angular:browser-esbuild` 后，与早期版本相比，会添加 `chunk-xxx.js` 文件。这些文件的名称不是固定的，因此静态文件引用无法轻松匹配。

---

### 控制 Chunk 行为

您可以通过 `angular.json` 控制 common chunk：

```json
{
  "architect": {
    "build": {
      "options": {
        "commonChunk": true
      }
    }
  }
}
```

如果在您的特定场景中复制一些代码更好，您可以将 `angular.json` 配置中的 `commonChunk` 设置为 `false`，以避免生成 `common.js` 文件。不过要小心——这意味着共享代码会在 lazy-loaded JS 文件中重复，因此根据您的具体情况谨慎选择。

---

### Chunk 中包含什么？

Angular 和 CLI 通过 Webpack 和 JSONP 包装模块代码，以便从服务器加载和执行。Lazy-loaded chunk 包含编译后的组件、其模板及其模块注册。

---

### 总结表格

| Chunk Type | Example Name | Contents |
|---|---|---|
| Lazy module chunk | `auth.module.chunk.js` | Code for a lazy-loaded feature module |
| Common chunk | `common.js` | Shared code between 2+ lazy modules |
| Hash chunk (esbuild) | `chunk-ABC123.js` | Split output from esbuild bundler |
| Named chunk | `0.chunk.js` | Unnamed/numbered lazy split |

参考资料：

- [Common Chunk and Lazy Loading in Angular – juri.dev](https://juri.dev/blog/2021/02/common-chunk-lazy-loading-angular-cli/)
- [What is a chunk in Angular? – Quora](https://www.quora.com/What-is-a-chunk-in-Angular)
- [chunk-xxx.js added after browser-esbuild – GitHub Issue #26377](https://github.com/angular/angular-cli/issues/26377)
- [What's in My Angular Chunks? – fluin.io](https://fluin.io/blog/whats-in-my-angular-chunks)
