---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 简单易懂的 Angular 核心包详解
translated: true
type: note
---

Angular 生态系统中有几个共同协作的关键 package。以下是它们之间的关系：

**@angular/core** 是最基础的 package，包含了 core framework 功能 —— 例如 components、directives、dependency injection、change detection 和 component lifecycle。每个 Angular app 都需要它。

**@angular/compiler** 将你的 Angular templates（带有 Angular 特定语法的 HTML）转换成浏览器可以执行的 JavaScript 代码。这通常有两种方式：
- Just-in-time (JIT)：编译在运行时发生于浏览器中
- Ahead-of-time (AOT)：编译在 build 过程中发生（生产环境的首选）

**@angular/cli** (Angular CLI) 是用于开发的命令行工具。它帮助你创建 project，生成 components/services/modules，运行 dev server，进行 production build，运行 tests 等。当你执行 `ng serve` 或 `ng build` 时，你就在使用 CLI。它在后台协调 compiler 和其他 build tools。

**@angular/compiler-cli** 是 CLI 与 compiler 的接口，在 build 过程中用于 AOT 编译。

**可以这样理解：**
- `@angular/core` = 汽车的发动机
- `@angular/compiler` = 将你的 Angular 代码翻译成浏览器能理解的内容
- `@angular/cli` = 你构建和管理 Angular apps 的工具箱和控制面板
- `@angular/compiler-cli` = 在 build 时将 CLI 连接到 compiler

此外还有许多其他的 `@angular/*` packages，如 `@angular/common`、`@angular/router`、`@angular/forms` 等，它们提供了额外的功能，但你询问的这三个 package 构成了基础的 build 和 runtime 架构。