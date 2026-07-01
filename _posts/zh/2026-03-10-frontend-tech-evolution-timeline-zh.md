---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 前端技术演变时间线
translated: true
type: note
---

# 前端 Web 开发完整演进史

---

## 第一时代：静态网页 — HTML（1990 年代早期）

1989–1991 年，Tim Berners-Lee 在 CERN 发明了 World Wide Web，创造了仍然构成了 web 基础的核心技术：HTTP（HyperText Transfer Protocol）、HTML（HyperText Markup Language），以及用于寻址网页的 URI/URL。

在 1990 年代早期，网站不过是简单的 HTML 文档。这些页面仅包含静态文本和图像，用户交互非常有限。

**这一时代的关键特征：**

- 页面是“只读”的 — 用户可以浏览，但无法进行有意义的交互
- 没有动态更新；内容只有在开发者手动编辑文件时才会改变
- 除了基本的浏览器默认样式外，没有其他样式
- web 主要用于学术界和研究机构

---

## 第二时代：CSS 和视觉化网页（1990 年代中期）

随着网页复杂度的增加，对更好样式的需求变得明显。CSS 于 1996 年引入，允许开发者将内容与设计分离，并提升网页的美观度。

在 web 的早期，大多数浏览器并不遵守标准化的 CSS 规范。在一个浏览器中看起来正常的网站，在另一个浏览器中可能完全乱套，这让开发非常令人沮丧。

这种跨浏览器不一致性困扰了开发者超过十年之久。

---

## 第三时代：JavaScript 诞生（1995 年）

1995 年，Brendan Eich 在短短 10 天内创建了一种新的浏览器脚本语言，名为 Mocha。随后它被重命名为 LiveScript，几个月后又改名为 JavaScript。

JavaScript 引入了操纵 **Document Object Model (DOM)** 的能力 — 页面结构的内存表示 — 允许开发者响应用户事件、验证表单，并在不重新加载页面的情况下动画化元素。然而，早期的 JavaScript 笨拙、跨浏览器不一致，并且被许多严肃工程师视为玩具语言。

---

## 第四时代：AJAX — 动态网页觉醒（2000 年代早期）

**AJAX**（Asynchronous JavaScript and XML）带来了突破性时刻：

AJAX 技术早在 1996 年就存在，但未被充分利用。2004 年，Google 在 Gmail 和 Google Maps 上实现了标准化的 AJAX 版本。不久后，他们开始在其他 web 应用中实施它。

AJAX 允许页面在后台从服务器获取数据，而无需完整页面重新加载。这具有变革性 — Google Maps 可以平滑平移和缩放，Gmail 可以加载邮件而无需刷新整个浏览器窗口。web *application*（不仅仅是 web *page*）的概念开始成形。

---

## 第五时代：jQuery — 少写代码，多做事（2006 年）

jQuery 于 2006 年发布，是首批获得广泛采用的库之一。它简化了 DOM 操纵、事件处理和 AJAX 请求，让开发者写更少的代码，做更多的事。

**jQuery 的革命性之处：**

- **跨浏览器兼容**：屏蔽了 Internet Explorer、Firefox 等浏览器之间的所有不一致性
- **简洁的选择器**：可以用 `$(".myClass")` 针对 DOM 元素，而不是冗长的原生 API 调用
- **可链式方法**：`$("div").hide().fadeIn().addClass("active")` — 全在一行
- **插件生态**：数千个社区插件，用于滑块、模态框、日期选择器等

在 jQuery 兴起之前，Prototype.js 和 MooTools 等库引入了面向对象编程和更高级的 DOM 操纵概念，为前端框架的演进铺平了道路。

jQuery 主宰了 web 近十年，并且今天仍存在于大量网站上。然而，随着应用复杂度的增加，在大型代码库中管理 jQuery“意大利面代码”变得痛苦。没有强制结构、没有状态管理、没有组件模型。

---

## 第六时代：MVC 框架和 SPA 革命（2010–2013 年）

### Backbone.js（2010 年）

大约 2010 年，Backbone.js 作为首批前端框架之一出现，为构建单页应用（SPAs）提供了组织结构。它引入了 Models、Views 和 Collections，但将大多数架构决策留给开发者 — 对于大型团队来说，自由度太大，指导太少。

### AngularJS（2010 年）— Google 的完整框架

Google 于 2010 年发布 AngularJS，标志着现代框架时代的开始。AngularJS 是一个完整的 MVC（Model-View-Controller）框架，旨在构建快速、响应式和动态的单页应用（SPAs）。

AngularJS 引入了几个强大理念：

- **双向数据绑定**：UI 和数据模型自动保持同步
- **依赖注入**：使代码更易测试和模块化
- **指令**：自定义 HTML 属性，扩展浏览器的词汇（例如 `ng-repeat`、`ng-model`）

缺点：AngularJS 学习曲线陡峭，并且由于其“脏检查”机制，在非常大的数据集上存在性能问题。

---

## 第七时代：React — 组件革命（2013 年）

Facebook 于 2013 年发布的 React 通过其基于组件的架构和 virtual DOM，进一步革新了 web 开发，使构建交互式用户界面更容易。

React 的核心创新：

**Virtual DOM**：ReactJS 引入了 virtual DOM，通过高效更新用户界面的必要部分来提升性能。React 计算旧虚拟 DOM 树和新虚拟 DOM 树之间的差异，并仅将最小变更集应用到真实 DOM，而不是重新渲染整个页面。

**基于组件的架构**：像 React 这样的框架引入了可重用 UI 组件的概念，允许开发者从更小、模块化的构建块组成复杂用户界面。这种方法促进了代码重用、可扩展性和更容易维护。

React 故意**是一个库，而不是完整框架** — 它仅专注于 View 层。这意味着开发者必须与其他工具结合（React Router 用于导航、Redux/MobX 用于状态管理等），提供了灵活性，但也需要更多配置决策。

---

## 第八时代：Angular 2+ — 完整重写（2016 年）

Google 认识到 AngularJS 的架构局限性，并于 2016 年将其完全重写为简称为 **Angular**（版本 2+）。与 AngularJS 的关键区别：

- 默认使用 **TypeScript** 编写，为前端带来静态类型
- 基于组件的架构（受 React 影响）
- 用更明确的**单向数据流**选项替换双向绑定
- Angular 引入了包含声明式模板、依赖注入和丰富工具生态的完整框架。Angular 的架构使其适合构建复杂应用，提供双向数据绑定和强大的路由系统等功能。

Angular 是一个**有主见、开箱即用**的框架 — 非常适合受益于强制约定的大型企业团队。

---

## 第九时代：Vue.js — 渐进式框架（2014 年）

Vue.js 是一个渐进式框架，结合了 AngularJS 和 ReactJS 的最佳特性，提供灵活且直观的发展体验。

由 Evan You（前 Google 工程师，曾参与 AngularJS 开发）创建，Vue 的关键卖点：

- **平缓的学习曲线**：HTML 模板感觉自然；初学者可以逐步采用
- **渐进式采用**：可以在现有页面的单个小部件上使用 Vue，或用它构建整个 SPA
- **Single File Components (SFCs)**：组件的 HTML、CSS 和 JavaScript 全都在单个 `.vue` 文件中
- 比 Angular 更小的捆绑包大小，比 React 更简单的心理模型

Vue 在亚洲（尤其是中国）以及那些觉得 React 的 JSX 语法刺眼或 Angular 复杂度过高的开发者中变得非常流行。

---

## 第十时代：现代工具层（2012 年至今）

随着应用的复杂化，一整个支持工具生态系统出现了：

**包管理器：**

- **npm**（Node Package Manager，2010 年）— 安装和管理 JavaScript 依赖
- **Yarn**（2016 年，Facebook 出品）— npm 的更快、更确定性的替代品

**模块打包器：**

- 像 Webpack 这样的打包器革新了前端资产生成和部署，允许高效模块加载和代码拆分。
- **Vite**（2020 年）— 使用原生 ES modules 的更新、更快的替代品

**转译器：**

- **Babel** — 将现代 JavaScript（ES6+）转换为浏览器兼容的 ES5
- **TypeScript** — 为 JavaScript 添加静态类型；现在是大型代码库的主导选择

**CSS 工具：**

- **Sass/LESS** — CSS 预处理器，添加变量、嵌套和混入
- **Tailwind CSS** — 自 ~2019 年以来席卷生态系统的工具优先 CSS 框架

---

## 第十一时代：元框架和全栈渲染（2016 年至今）

SPAs 的一个主要弱点是 **SEO 差和初始加载慢**，因为浏览器必须下载并执行 JS 才能渲染内容。这导致了融合前端和后端的元框架：

像 Next.js（基于 React）、Nuxt.js（基于 Vue）和 Remix（基于 React）这样的框架因其混合方法而获得 traction，支持静态站点生成（SSG）和服务器端渲染（SSR），以获得更好的性能和 SEO。

- **Next.js**（Vercel，2016 年）：最受欢迎的 React 元框架；支持 SSR、SSG 和 ISR（Incremental Static Regeneration）
- **Nuxt.js**：Next.js 的 Vue 等价物
- **SvelteKit**：基于 Svelte 的编译器框架，生成无 virtual DOM 开销的原生 JS
- **Astro**（2021 年）：“islands architecture” 框架，适用于内容导向站点，默认零 JS

---

## 第十二时代：新挑战者和未来（2019 年至今）

**Svelte** 完全挑战了范式 — 而不是向浏览器运送运行时框架，Svelte 是一个**编译器**，在构建时将组件转换为高效的原生 JavaScript。没有 virtual DOM，开销最小。

**Solid.js** 提供类似 React 的语法，但使用细粒度响应性（类似于 signals）而不是 virtual DOM，实现近原生性能。

大多数前端框架现在已经稳定，并正在进一步优化以提高性能并更开发者友好。现代库提供的绝大多数繁重任务很可能很快就会原生实现。因此，一代高性能轻量级框架正在开发中。

**WebAssembly (WASM)** 也开辟了新前沿：WebAssembly 使 C++ 和 Rust 等语言的高性能代码能够在浏览器中运行，可能允许非 JavaScript 语言驱动前端逻辑。

---

## 总结时间线

| Year | Milestone |
| ------ | ----------- |
| 1991 | HTML invented by Tim Berners-Lee |
| 1995 | CSS 1.0 spec; JavaScript created by Brendan Eich |
| 1996 | CSS officially recommended by W3C |
| 2004 | Google popularizes AJAX with Gmail & Maps |
| 2006 | jQuery released |
| 2009 | Node.js — JavaScript goes server-side |
| 2010 | AngularJS (Google); Backbone.js |
| 2013 | React (Facebook) |
| 2014 | Vue.js (Evan You) |
| 2016 | Angular 2 rewrite; Next.js |
| 2019 | Svelte 3; Tailwind CSS goes mainstream |
| 2020 | Vite bundler; Deno |
| 2021 | Astro, SolidJS gain traction |
| 2024+ | AI-assisted coding, signals-based reactivity, edge rendering |

---

## 整体图景

前端演进可以总结为三个范式转变：

1. **文档 → 应用**：从静态 HTML 页面到由 JavaScript 驱动的交互式 SPAs
2. **命令式 → 声明式**：从手动操纵 DOM（jQuery）到描述 UI *应该是什么样子*，让框架搞定 *如何更新*（React、Vue、Angular）
3. **纯客户端 → 混合渲染**：从纯客户端 SPAs 回归服务器端和客户端渲染的混合，以获得性能和 SEO（Next.js、Nuxt、Astro）

每一代都解决了前一代的痛点 — 并引入了新痛点。前端生态系统的快速变化步伐既是其最大优势，也是其最臭名昭著的特征。

References:

- [The Evolution of Front-End Development: From HTML to Modern Frameworks (Medium - Matt Coleman)](https://medium.com/@mattlcoleman88/the-evolution-of-front-end-development-from-html-to-modern-frameworks-110c995ec7fc)
- [The Evolution of Web Development: From HTML to Modern Frameworks (Medium - MCSG)](https://medium.com/@MakeComputerScienceGreatAgain/the-evolution-of-web-development-from-html-to-modern-frameworks-b10a98ad91b6)
- [History of Frontend Frameworks — LogRocket Blog](https://blog.logrocket.com/history-of-frontend-frameworks/)
- [The Evolution of Web Development: From HTML to Modern Full-Stack Frameworks — DEV Community](https://dev.to/byte-sized-news/the-evolution-of-web-development-from-html-to-modern-full-stack-frameworks-344)
- [History and Evolution of Web Development — GeeksforGeeks](https://www.geeksforgeeks.org/blogs/history-and-evolution-of-web-development/)
- [The Evolution of Frontend Frameworks: From Vanilla JS to Modern Component-Based Architectures](https://articles.readytowork.jp/the-evolution-of-frontend-frameworks-from-vanilla-js-to-modern-component-based-architectures-ea8ade52ffc1)
