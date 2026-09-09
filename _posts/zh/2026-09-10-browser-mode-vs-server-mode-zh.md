---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 浏览器模式 vs 服务器模式
translated: true
type: note
---

问题：浏览器模式和服务端模式（在Web开发/渲染中）是什么？

回答：

这两种模式描述了应用程序逻辑与渲染发生的**位置**：

---

**浏览器模式（客户端渲染）**

- 代码直接在用户的**浏览器**中运行（通过JavaScript）
- 服务器发送最小化的HTML外壳；浏览器下载JavaScript的包并渲染用户界面
- 示例：React SPA、Vue SPA
- 优点：首次加载后交互速度快，无需为每个操作请求服务器
- 缺点：首次加载速度慢，SEO面临挑战，敏感信息无法隐藏

---

**服务端模式（服务器端渲染）**

- 代码在**服务器**上运行；服务器发送完整渲染的HTML给浏览器
- 浏览器接收可直接显示的内容
- 示例：Next.js SSR、Nuxt SSR、传统PHP/Rails
- 优点：首次渲染速度快，SEO表现更好，敏感信息保留在服务器端
- 缺点：每次请求都会访问服务器，交互速度可能较慢

---

**快速对比**

| | 浏览器模式 | 服务端模式 |
| --- | --- | --- |
| 渲染位置 | 客户端（浏览器） | 服务器 |
| 首次加载速度 | 较慢 | 较快 |
| SEO | 较困难 | 较好 |
| 交互性 | 加载后非常快 | 取决于注水（Hydration） |
| 敏感信息/API密钥 | 存在暴露风险 | 安全 |

---

现代框架如 **Next.js** 和 **Nuxt** 允许你混合使用这两种模式——部分组件在服务端渲染，部分在客户端渲染——从而兼得两者优势。

参考资料：

- [客户端渲染 vs 服务端渲染 – MDN](https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Client-Server_overview)
- [Next.js: 服务端与客户端组件](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
