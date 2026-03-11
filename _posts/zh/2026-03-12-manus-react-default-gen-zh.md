---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Manus 默认生成 React
translated: true
type: note
---

**问题：** Manus 用于其 web 输出使用什么框架？我看到许多初学者使用 Manus 搭建他们的第一个网站——它使用 React、Vue、Angular，还是其他什么？

**答案：**

Manus 本身 **不是像 React、Vue 或 Angular 那样的传统 web 框架**，你不会直接选择并编码使用它。它是一个 **AI 驱动的全栈网站/应用构建器**，基于自然语言提示为你生成完整的代码，包括 **前端框架代码**。它处理 **前端和后端**，并允许你导出或部署完成的项目。([Manus][1])

以下是框架方面的实际工作方式：

* **前端代码输出：** 当 Manus 生成你的网站时，它通常会产生使用流行技术的 **现代 JavaScript 前端代码**。用户和文档示例表明，它生成的项目使用像 **React** 这样的框架（通常带有像 **Vite** 和 **Tailwind CSS** 用于样式设计的工具）。用户报告导出 React 代码并自行部署。([LinkedIn][2])
* **你拥有源代码：** Manus 允许你 **导出生成的源代码**，这通常是一个基于 React 的项目，并使用 Tailwind 处理 CSS。这意味着你的网站不会被锁定在专有格式中——你可以带走它并托管在任何地方。([Manus][1])
* **不锁定单一框架：** 因为 Manus 根据指令生成代码，你 *可以* 指定不同的框架（例如，要求使用 Vue 或 Nuxt），尽管大多数常见用例示例默认使用 React。用户在一些报告中提到要求它使用像 Nuxt.js（Vue）这样的框架——表明多框架输出是可能的。([Manus][3])
* **Manus 本身不是框架：** Manus 作为云端 AI 平台运行并生成代码；它生成的 **网站是一个标准的前端应用**，使用它被指示生成的框架。它本身不会 *运行* 在 Angular 或 Vue 中——它只是 *生成代码*，供你的网站使用。([Manus][4])

简而言之：
• Manus 通常输出使用 **React（带有 Tailwind CSS）** 构建的网站（最常见）。([LinkedIn][2])
• 你 *可以* 指示它使用其他框架（Vue、Nuxt 等）。([Manus][3])
• Manus 本身不是前端框架——它是一个 **代码生成 AI 平台**，为你编写全栈应用。([Manus][4])

**参考资料：**

* 生成的前端代码通常是来自 Manus 的 React/Tailwind 可导出代码。([Manus][1])
* 用户报告从 Manus 导出并部署 React 代码。([LinkedIn][2])
* 它生成全栈应用并让你拥有/导出源代码。([Manus][1])

[1]: https://manus.im/tools/business-website-builder?utm_source=chatgpt.com "中小企业网站构建器：在线发展你的业务"
[2]: https://www.linkedin.com/posts/sudeepta-sahu-48155711_product-portfolio-app-activity-7376953814223872000-Bg_6?utm_source=chatgpt.com "从 Canva 到网站：我如何使用 Manus 和 Cursor | Sudeepta Sahu 在 LinkedIn 上发布的主题"
[3]: https://www.manus.im/home?utm_source=chatgpt.com "首页 - Manus"
[4]: https://manus.im/docs/website-builder/getting-started?utm_source=chatgpt.com "入门指南 - Manus 文档"