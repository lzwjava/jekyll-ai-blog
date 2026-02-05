---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: JavaScript 库的 TypeScript 类型定义
translated: true
type: note
---

没错，完全正确！`@types/` 包是为 JavaScript 库提供的 TypeScript 类型定义文件。

它的工作原理如下：

许多流行的 JavaScript 库（如 React、Express、Lodash）是在 TypeScript 出现之前，或是未考虑 TypeScript 的情况下用纯 JavaScript 编写的。当你在 TypeScript 项目中使用这些库时，TypeScript 无法识别该库的函数所期望或返回的类型。

`@types/` 包提供了这些类型定义。例如：
- `@types/react` - React 的类型定义
- `@types/node` - Node.js 的类型定义
- `@types/express` - Express 的类型定义

这些包维护在 [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped) 仓库中，这是一个旨在提供高质量 TypeScript 类型定义的社区项目。

**你什么时候需要它们？**
- 如果一个包是用 JavaScript 编写的，且没有包含自己的类型定义。
- 现代的包通常会包含自己的类型定义（直接捆绑在包内），这种情况下你不需要单独安装 `@types/` 包。

**示例：**

```bash
npm install lodash          # JavaScript 库
npm install -D @types/lodash  # TypeScript 定义
```

`@types/` 包完全不会改变 runtime 行为 —— 它只是在开发和 compilation 阶段帮助 TypeScript 理解库的 API。