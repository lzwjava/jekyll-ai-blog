---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 浏览器/服务器模式 vs C/S 和 B/S
translated: true
type: note
---

问题：浏览器/服务器模式与C/S（客户端/服务器）和B/S（浏览器/服务器）架构相比如何？

答案：

它们实际上是**密切相关的概念**——浏览器/服务器模式本质上是经典B/S与C/S架构区分的一个现代、精细化的版本。

---

## 经典架构模型

**C/S（客户端/服务器）**
- 专用**原生客户端应用**（桌面应用）与服务器通信
- 示例：Outlook桌面版、WinForms应用、原生移动应用
- 逻辑分布在胖客户端和后端服务器之间
- 每台机器需要安装

**B/S（浏览器/服务器）**
- **浏览器作为通用客户端**——无需安装
- 所有UI通过HTTP以HTML/CSS/JS形式交付
- 示例：通过Chrome/Firefox/Safari访问的Web应用
- 服务器处理大部分逻辑；浏览器仅负责渲染

---

## 它们如何映射到浏览器/服务器模式

| 概念 | 映射到 | 说明 |
|---|---|---|
| C/S 架构 | — | 原生客户端；通常不属于“浏览器模式” |
| B/S 架构 | **同时**包含浏览器模式和服务器模式 | B/S是总称；*模式*决定了渲染发生的位置 |
| 浏览器模式 | B/S + 客户端渲染 | 首次加载后浏览器承担主要工作 |
| 服务器模式 | B/S + 服务器端渲染 | 服务器承担主要工作，发送已渲染的HTML |

---

## 关键洞察

```
C/S  →  胖原生客户端 + 后端服务器
B/S  →  浏览器作为客户端 + 后端服务器
         ├── 浏览器模式（逻辑在浏览器中运行）
         └── 服务器模式（逻辑在服务器上运行，结果发送给浏览器）
```

> B/S 架构**取代了**大多数Web应用中的C/S架构。
> 浏览器/服务器*模式*是B/S的**内部细分**，描述了渲染和逻辑的存放位置。

---

## 实际差异

| | C/S | B/S（服务器模式） | B/S（浏览器模式） |
|---|---|---|---|
| 客户端类型 | 原生应用 | 浏览器 | 浏览器 |
| 安装 | 需要 | 无需 | 无需 |
| 渲染 | 客户端应用 | 服务器 | 浏览器JS |
| 网络依赖 | 中等 | 高 | 高（仅初始） |
| SEO友好 | 不适用 | ✅ 是 | ⚠️ 较困难 |
| 离线支持 | ✅ 通常支持 | ❌ 不支持 | ⚠️ 部分支持（PWA） |
| 示例 | WPF、Qt应用 | PHP、Rails、Next.js SSR | React SPA、Vue SPA |

参考来源：
- [客户端-服务器模型 – Wikipedia](https://en.wikipedia.org/wiki/Client%E2%80%93server_model)
- [浏览器/服务器与客户端/服务器架构](https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Client-Server_overview)
- [Next.js 渲染策略](https://nextjs.org/docs/app/building-your-application/rendering)