---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Android Drawable 资源的存储位置
translated: true
type: note
---

Question: 图像等 drawable 资源应该放置在哪个文件夹中？  
A) res/values  
B) res/layout  
C) res/drawable  
D) res/menu

Answer: 

正确答案是 **C) res/drawable**。

在 Android 项目中，drawable 资源（如 PNG, JPEG, SVG 等图像）、vector drawables 以及其他可以绘制在屏幕上的图形资源，都应放在 `res/drawable` 文件夹（或其特定密度的变体，如 `drawable-hdpi`, `drawable-mdpi` 等）中。

### 各选项简要说明：

- **A) res/values**: 该文件夹用于存放定义简单值的 XML 文件，如 strings, dimensions, colors, styles 和 arrays，不用于存放图像或 drawable。
- **B) res/layout**: 该文件夹包含定义 activities, fragments 等 UI 结构的 XML layout 文件。
- **C) res/drawable**: 存放 bitmap 文件、vector drawables、shapes、selectors 以及其他 drawable 资源的正确文件夹。
- **D) res/menu**: 该文件夹用于存放定义 menus（如 options menus, context menus）的 XML 文件。

将图像存放在正确的 `res/drawable` 文件夹中，可以确保它们能在代码或 XML 中被正确引用（例如 `@drawable/my_image`），并支持自动的 density 处理。