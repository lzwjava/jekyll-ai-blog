---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Goofish.com：React，而非Flutter
translated: true
type: note
---

**Question:** goofish.com（闲鱼网页版）是用 Flutter 构建的吗？

**Answer:**

**不是**，`goofish.com` **不是**用 Flutter Web 构建的。它是一个传统的 Web 应用。

以下是我通过检查页面源代码得出的判断依据：

### ❌ 没有找到 Flutter Web 的特征

Flutter Web 应用通常会在 HTML 中留下明显的痕迹：

- `flutter.js` 引导脚本
- `main.dart.js` 编译后的 Dart 代码
- `flutter_service_worker.js`
- `CanvasKit` WASM 加载
- `flt-` 前缀的 DOM 元素

这些在 `goofish.com` 上都不存在。

### ✅ 它实际使用的技术

查看页面源代码，会发现一个关键线索：

```
meta-ice-meta-count: 0
```

`ice` 前缀指向 **[ICE.js](https://ice.work/)** —— 阿里巴巴自研的基于 React 的前端框架（也称为 `icejs` 或 `AppWorks`）。该网页版是一个标准的 **React + SSR（服务端渲染）** 应用，这也解释了为什么它有完善的 SEO meta 标签（百度验证、Google 验证、关键词、描述）—— Flutter Web 的 CanvasKit 模式渲染到 `<canvas>` 中，搜索引擎基本无法识别。

### 总结

| 平台 | 技术 |
| --- | --- |
| 📱 Xianyu iOS/Android 应用 | ✅ Flutter |
| 🌐 goofish.com 网站 | ❌ React + Alibaba ICE.js（非 Flutter） |

这是一种非常常见的模式——公司使用 Flutter 构建**移动应用**，但为网站保留独立的**传统 Web 技术栈**，主要是因为 Flutter Web 在 SEO 和初始加载性能方面仍有局限，尤其对于内容密集型电商网站。
