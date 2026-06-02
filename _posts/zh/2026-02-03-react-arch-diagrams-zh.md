---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 轻松绘制 React 架构图
translated: true
type: note
---

是的！我可以使用 React (JSX) 创建 architecture diagrams。以下是触发生成 diagram 的方式：

## 如何提问：

**有效的简单提示词：**
- "为 [你的系统] 创建一个 architecture diagram"
- "画一个展示 [组件及其关系] 的 diagram"
- "将 [应用/系统] 的架构可视化"
- "为 [流程] 制作一个 flowchart"
- "给我展示一个包含 [组件] 的 system diagram"

## 示例：

**示例 1 - 简单：**
```
"为包含 React frontend、Node.js backend、PostgreSQL database 和 Redis cache 的 web app 创建一个 architecture diagram"
```

**示例 2 - 详细：**
```
"绘制一个展示以下内容的 microservices architecture diagram：
- API Gateway
- Auth Service
- User Service
- Payment Service
- Message Queue
- 每个 service 对应的 Databases"
```

**示例 3 - 特定流程：**
```
"创建一个 data flow diagram，展示用户身份验证从 login 到访问受保护资源的工作流程"
```

## 我将创建的内容：

我将使用以下技术构建一个 **interactive React component**：
- **Shapes**（矩形、圆形、用于 database 的圆柱体）
- 展示 data flow/connections 的 **Arrows**
- 组件的 **Labels**
- 用于区分组件类型的 **Colors**
- 用于 styling 的 **Tailwind CSS**

这些 diagram 是交互式的、可扩展的，并且看起来非常专业！

**想要尝试吗？** 只需描述你想要可视化的系统或架构即可！
