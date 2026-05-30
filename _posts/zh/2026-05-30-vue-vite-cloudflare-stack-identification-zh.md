---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Vue Vite Cloudflare栈识别
translated: true
type: note
---

**问题：** 根据页面源码，liber.davirain.xyz 的前端技术栈是什么？

**答案：**

从 HTML 中一目了然：

```html
<script type="module" crossorigin src="/assets/index-BBl0IX-N.js"></script>
<link rel="stylesheet" crossorigin href="/assets/index-B8One0Ye.css">
<div id="app"></div>
```

**技术栈分析：**

| 信号 | 结论 |
|--------|-----------|
| `<div id="app"></div>` | **Vue 3**（React 通常使用 `id="root"`，Vue 按惯例使用 `id="app"`） |
| `assets/index-[hash].js` | **Vite** 构建输出——`BBl0IX-N` 的哈希模式是 Vite 的默认块命名方式 |
| 单个 JS + CSS 捆绑包 | SPA，无 SSR |
| `<script>` 标签上的 `type="module"` | 现代 ESM 构建，Vite 默认 |
| `data-theme="light" data-display="cormorant"` | 自定义主题系统（Cormorant 是一种衬线字体——适合阅读类应用） |
| `lang="zh"` | 中文语言环境 |
| Cloudflare Insights 信标 | 部署在 **Cloudflare Pages** 上 |

**总结：** Vue 3 + Vite，部署在 Cloudflare Pages 上。

这与 DaviRain 快速搭建原型的做法一致——Vue 3 + Vite 是快速构建中文阅读界面的最快方式。`data-display="cormorant"` 表明他仔细考虑了阅读体验的排版（Cormorant Garamond 是一种经典的书本衬线字体）。