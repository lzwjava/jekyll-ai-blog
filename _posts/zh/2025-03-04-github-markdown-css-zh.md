---
audio: false
generated: true
lang: zh
layout: post
title: GitHub 的 Markdown 样式设计
translated: true
type: note
---

### 核心要点

- 使用 "github-markdown-css" npm 包时，首先需要通过 `npm install github-markdown-css` 安装。
- 研究表明，接下来需要将 CSS 文件导入项目，并将 Markdown 内容包裹在带有 "markdown-body" 类的 div 中。
- 证据倾向于建议设置可选的宽度和内边距以匹配 GitHub 样式，并确保使用 DOctype 以避免样式问题。

### 安装

首先在项目目录中使用 npm 安装该包：

- 运行 `npm install github-markdown-css` 将其添加到依赖项中。

### 使用方法

安装后，将 CSS 集成到项目中：

- 导入 CSS 文件，例如在 JavaScript/React 中使用 `import 'github-markdown-css';`。
- 将渲染后的 Markdown 内容包裹在 `<div class="markdown-body">...</div>` 中以应用样式。
- 可选地，添加 CSS 设置宽度和内边距以模仿 GitHub 外观：

  ```css
  .markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
  }
  @media (max-width: 767px) {
    .markdown-body {
      padding: 15px;
    }
  }
  ```

- 确保 HTML 包含 DOctype（例如 `<!DOCTYPE html>`），以防止影响样式的怪异模式问题。

### 意外细节

您可能没想到，该包还支持通过相关包 [generate-github-markdown-css](https://www.npmjs.com/package/generate-github-markdown-css) 生成自定义 CSS，如果您需要定制样式的话。

---

### 调研笔记：github-markdown-css npm 包使用全面指南

本详细指南探讨了 "github-markdown-css" npm 包的使用方法，该包旨在在 Web 项目中复制 GitHub 的 Markdown 样式。它提供了安装和集成的分步方法，以及在不同开发环境（如 React 或纯 HTML）中优化使用的额外注意事项。这些信息来源于官方包文档、GitHub 仓库和相关网络资源，确保各级开发者都能透彻理解。

#### 背景与目的

由 [sindresorhus](https://github.com/sindresorhus) 维护的 "github-markdown-css" 包提供了一套最简 CSS，用于模拟 GitHub 的 Markdown 渲染样式。这对于希望其 Markdown 内容（如文档或博客文章）呈现与 GitHub 熟悉且简洁的样式保持一致的开发者特别有用。该包被广泛使用，截至最近更新，npm 注册表中有超过 1,168 个项目使用它，表明了其受欢迎程度和可靠性。

#### 安装过程

首先，您需要通过 npm（Node.js 包管理器）安装该包。命令很简单：

- 在项目目录中执行 `npm install github-markdown-css`。这会将包添加到您的 `node_modules` 文件夹，并更新 `package.json` 中的依赖项。

根据最近检查，该包的最新版本是 5.8.1，大约三个月前发布，表明其处于积极维护和更新状态。这确保了与现代 Web 开发实践和框架的兼容性。

#### 集成与使用

安装后，下一步是将 CSS 集成到项目中。该包提供了一个名为 `github-markdown.css` 的文件，您可以根据项目设置导入：

- **对于 JavaScript/现代框架（如 React、Vue）：**
  - 在 JavaScript 或 TypeScript 文件中使用导入语句，例如 `import 'github-markdown-css';`。这与 Webpack 或 Vite 等打包器配合良好，它们能无缝处理 CSS 导入。
  - 对于 React，您可能会看到开发者在组件文件中导入它，确保样式在全局或按需作用域内可用。

- **对于纯 HTML：**
  - 直接在 HTML 头部链接 CSS 文件：

    ```html
    <link rel="stylesheet" href="node_modules/github-markdown-css/github-markdown.css">
    ```

  - 注意，路径可能因项目结构而异；确保相对路径正确指向 `node_modules` 目录。

导入后，通过将渲染后的 Markdown 内容包裹在带有 "markdown-body" 类的 `<div>` 中来应用样式。例如：

```html
<div class="markdown-body">
  <h1>Unicorns</h1>
  <p>All the things</p>
</div>
```

这个类至关重要，因为 CSS 会针对 `.markdown-body` 内的元素应用类似 GitHub 的样式，包括排版、代码块、表格等。

#### 样式注意事项

要完全复制 GitHub 的 Markdown 外观，请考虑为 `.markdown-body` 类设置宽度和内边距。文档建议：

- 最大宽度为 980px，较大屏幕上内边距为 45px，移动设备（屏幕 ≤ 767px）上内边距为 15px。
- 您可以使用以下 CSS 实现：

  ```css
  .markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
  }
  @media (max-width: 767px) {
    .markdown-body {
      padding: 15px;
    }
  }
  ```

这确保了响应式设计并与 GitHub 的设计保持一致，增强了可读性和用户体验。

#### 技术说明与最佳实践

- **DOctype 要求：** 文档强调了潜在的样式问题，例如如果浏览器进入怪异模式，深色模式下的表格可能渲染不正确。为防止这种情况，请始终在 HTML 顶部包含 DOctype，例如 `<!DOCTYPE html>`。这确保了符合标准的渲染，避免了意外行为。
- **Markdown 解析：** 虽然该包提供了 CSS，但它不解析 Markdown 为 HTML。您需要一个 Markdown 解析器，如 [marked.js](https://marked.js.org/) 或 React 项目的 [react-markdown](https://github.com/remarkjs/react-markdown)，将 Markdown 文本转换为 HTML，然后才能用此 CSS 进行样式设置。
- **自定义 CSS 生成：** 对于高级用户，相关包 [generate-github-markdown-css](https://www.npmjs.com/package/generate-github-markdown-css) 允许生成自定义 CSS，可能对特定主题或修改有用。这对于可能认为该包仅用于直接使用的用户来说是一个意外细节。

#### 在特定上下文中的使用

- **React 项目：** 在 React 中，将 `github-markdown-css` 与 `react-markdown` 结合使用很常见。安装两者后，导入 CSS 并使用组件：

  ```javascript
  import React from 'react';
  import ReactMarkdown from 'react-markdown';
  import 'github-markdown-css';

  const MarkdownComponent = () => (
    <div className="markdown-body">
      <ReactMarkdown># Hello, World!</ReactMarkdown>
    </div>
  );
  ```

  确保还设置如前所示的宽度和内边距 CSS，以实现完整的 GitHub 样式。

- **使用 CDN 的纯 HTML：** 对于快速原型设计，您可以使用 CDN 版本，可在 [cdnjs](https://cdnjs.com/libraries/github-markdown-css) 获取，直接链接：

  ```html
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown.min.css">
  ```

  然后如前所述应用 `.markdown-body` 类。

#### 潜在问题与解决方案

- **样式冲突：** 如果您的项目使用其他 CSS 框架（如 Tailwind、Bootstrap），请确保没有特异性冲突。`.markdown-body` 类应覆盖大多数样式，但需彻底测试。
- **深色模式支持：** 该包包含对深色模式的支持，但请确保您的 Markdown 解析器和项目设置正确处理主题切换，特别是对于代码块和表格。
- **浏览器兼容性：** 鉴于该包的广泛使用，兼容性通常良好，但始终需在主流浏览器（Chrome、Firefox、Safari）中测试以确保渲染一致。

#### 比较分析

与其他 Markdown CSS 选项（如 [Markdown CSS](https://markdowncss.github.io/)）相比，"github-markdown-css" 因其直接复制 GitHub 样式而脱颖而出，非常适合需要镜像 GitHub 外观的文档。然而，与一些开箱即用提供多主题的替代方案不同，它在没有额外定制的情况下缺乏内置的主题选项。

#### 表格：主要特性与注意事项

| 特性                     | 描述                                                                 |
|--------------------------|---------------------------------------------------------------------|
| 安装命令                 | `npm install github-markdown-css`                                   |
| CSS 导入方法             | `import 'github-markdown-css';` 或 HTML 中的 `<link>`               |
| 必需类名                 | `.markdown-body` 用于应用样式                                       |
| 宽度与内边距             | 最大 980px，45px 内边距（桌面）；15px 内边距（移动端 ≤ 767px）      |
| DOctype 要求             | 必需，以避免怪异模式并确保正确渲染                                  |
| 自定义 CSS 生成          | 可通过 [generate-github-markdown-css](https://www.npmjs.com/package/generate-github-markdown-css) 实现 |
| 兼容性                   | 适用于 marked.js、react-markdown 等 Markdown 解析器；广泛的浏览器支持 |

#### 结论

对于寻求复制 GitHub Markdown 样式的开发者来说，使用 "github-markdown-css" 是直截了当的。通过遵循安装和集成步骤，并考虑额外的样式和技术说明，您可以为 Markdown 内容实现一致且专业的外观。对于高级定制，请探索生成包，并始终测试兼容性和渲染问题，尤其是在复杂项目中。

#### 主要引用

- [github-markdown-css npm 包页面](https://www.npmjs.com/package/github-markdown-css)
- [复制 GitHub Markdown 样式的最简 CSS GitHub 仓库](https://github.com/sindresorhus/github-markdown-css)
- [GitHub Markdown CSS 演示页面](https://sindresorhus.com/github-markdown-css/)
- [生成 github-markdown-css 的 CSS npm 包](https://www.npmjs.com/package/generate-github-markdown-css)
- [github-markdown-css CDN 由 cdnjs 提供](https://cdnjs.com/libraries/github-markdown-css)
