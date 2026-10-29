---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 3Blue1Brown如何制作视频
translated: true
type: note
---

**问题：** 3Blue1Brown 是如何制作视频的，他使用了哪些工具/项目？

**回答：**

Grant Sanderson（3Blue1Brown）最常被问到的问题是他用什么来制作视频动画。简短的回答是，他编写了一个**名为 Manim 的自定义 Python 库**——它完全是程序化的，而且非常定制化。

### 🔧 核心工具 —— Manim

**Manim** 代表 **Mathematical Animation Engine**（数学动画引擎），由 Grant Sanderson 创建，用于制作高精度的数学动画视频。

它与标准动画软件的不同之处在于，**一切都是脚本化的**——你编写 Python 代码来描述形状、位置和变换，Manim 会将帧渲染成视频。

### 🚀 它是如何开始的

Grant 最初用一段简陋的 Python 代码制作了他频道上的第一个视频，随着他制作更多视频，工具也不断改进——而工具改进后又让他能制作更多视频，如此循环往复。他一直把自己为视频编写的所有代码公开发布在 GitHub 上，同时也将底层工具 Manim 开源。

### 📦 Manim 的两个版本

一个是他个人的版本，另有一个社区——人们希望它成为更强大的工具，于是分叉了该仓库并创建了一个更关注 issues 和 pull requests、拥有更好测试和文档的版本——它被称为 **Manim Community** 版。

### 🎬 完整工作流程

Manim 只是用来制作单个片段以供后期剪辑的工具。他建议尽可能多地使用**传统视频编辑软件**。

他还使用 **MathPix**，这是一个 OCR 工具，可以将方程截图直接转换为 LaTeX 代码。工作流程变成：在论文中看到方程 → 截图 → 将 LaTeX 粘贴到 Manim 中 → 制作动画。

### 📁 GitHub 上的代码

GitHub 仓库 `3b1b/videos` 包含用于生成 3Blue1Brown 上所有解释性数学视频的代码，按年份从 2015 年起整理。

---

**工具总结：**

| 工具 | 用途 |
|------|---------|
| **Manim**（Python 库） | 核心动画引擎 |
| **LaTeX** | 数学公式渲染 |
| **MathPix** | 将方程转换为 LaTeX |
| **视频编辑软件**（如 Premiere） | 最终视频剪辑和旁白同步 |
| **GitHub** | 开源代码分享 |

**参考链接：**
- [3Blue1Brown 常见问题（官方）](https://www.3blue1brown.com/faq/)
- [How I animate 3Blue1Brown — Manim demo](https://recapio.com/digest/how-i-animate-3blue1brown-a-manim-demo-with-ben-sparks-by-3blue1brown)
- [Manim 在维基百科上](https://www.wikiwand.com/en/articles/Manim)
- [3b1b/manim 在 GitHub 上](https://github.com/3b1b/manim)
- [3b1b/videos（场景代码）在 GitHub 上](https://github.com/3b1b/videos)