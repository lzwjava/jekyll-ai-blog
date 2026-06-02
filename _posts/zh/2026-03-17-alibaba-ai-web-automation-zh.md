---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 阿里巴巴的 AI 网页自动化工具
translated: true
type: note
---

我会搜索有关 Alibaba page-agent 项目的资料，为您提供全面介绍。**问题：** Alibaba 的 page-agent 介绍是什么？

**答案：**

## Page Agent 概述

Page Agent 是一个 JavaScript in-page GUI agent，它允许您使用自然语言控制 web 接口。它是由 Alibaba 开发的一个开源项目，将 AI-powered 自动化直接带到您的网页上。

### 核心概念

Page Agent 作为“生活在您网页中的 GUI Agent”运行，并启用 web 接口的自然语言控制。与传统的 web 自动化工具不同，它完全作为 JavaScript 在页面内运行，使集成无缝且高效。

### 关键特性

该项目提供几个独特特性，包括无需浏览器扩展、Python 或 headless browsers 的轻松集成——一切都直接发生在您的网页中。

它使用基于文本的 DOM 操作，消除了对截图、OCR 或多模态 LLMs 的需求，同时无需特殊权限。

Page Agent 支持自带 LLMs，并包含一个漂亮的 UI，支持 human-in-the-loop 功能，以及可选的 Chrome 扩展用于多页面任务。

### 主要用例

该工具设计用于几个应用：创建 SaaS AI Copilots，可以用最小代码集成到您的产品中，无需后端重写；自动化智能表单填充，将冗长的点击工作流转换为单句（适用于 ERP、CRM 和管理系统）；通过自然语言提高 web 应用的 accessibility；启用跨浏览器标签的多页面 agent 任务。

### 技术实现

Page Agent 使用 TypeScript 构建，可通过 NPM 安装。它支持与各种 LLMs 的集成，Qwen 是支持的模型示例。

### 快速开始

该项目提供多种集成方法，包括一行 CDN 集成用于快速测试，以及 NPM 安装用于生产使用。该项目承认 browser-use 是基础工作，DOM 处理组件和提示源自该优秀项目。

---

## 参考资料

- [GitHub - alibaba/page-agent](https://github.com/alibaba/page-agent)
- [Page Agent Official Demo & Documentation](https://alibaba.github.io/page-agent/)
