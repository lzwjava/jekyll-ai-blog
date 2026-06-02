---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 王垠博客技术栈分析
translated: true
type: note
---

该网站（<https://www.yinwang.org/，标题为"当然我在扯淡"）似乎是一个定制开发的博客。根据提供的HTML源码分析：>

- **框架**：主要基于 **Vue.js**（很可能是版本3），从Vue特有的属性可以看出，例如`data-v-app`、用于作用域CSS的`data-v-[哈希值]`，以及组件引用（如处理导航的`HomeView`、`PostView`、`router-link-active`）。
- **构建工具**：使用 **Vite** 进行打包和开发，这可通过网站图标（`/vite.svg`）、带有哈希文件名的预加载模块脚本（例如`/assets/index-DS_1rR7p.js`）以及Vite输出特有的整体资源结构来证明。
- **样式**：采用 **Tailwind CSS** 实现工具优先的类名（例如`bg-gray-50 dark:bg-gray-900`、`flex items-center`，以及响应式前缀如`sm:px-4`）。
- **其他说明**：未发现服务端渲染标识（如无Nuxt.js痕迹），因此很可能是一个静态网站或客户端渲染的单页应用。其内容（文章、标签、分页）表明这是一个为个人博客定制的简易架构，可能使用Markdown编写文章内容。

该网站**并非完全手写**——HTML是在构建过程中由Vue组件和模板自动生成的。核心逻辑（路由、组件）使用JS/TS编写，但最终输出为优化后的静态文件。没有使用Hugo或Jekyll等完整静态网站生成器的迹象，更像是一个轻量级的Vue + Vite项目。

[当然我在扯淡](https://www.yinwang.org/)
