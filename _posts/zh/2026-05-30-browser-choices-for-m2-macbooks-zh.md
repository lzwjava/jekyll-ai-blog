---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M2 MacBook的浏览器选择
translated: true
type: note
---

**问题：** 在 macOS（MacBook Air M2）上我应该使用什么浏览器？

**答案：**

在 M2 Mac 上，引擎的选择更为重要，因为 Apple Silicon 优化。

## Safari — 实际上这里最适合的默认选择

尽管它是闭源的，但在 M2 Mac 上，**Safari 确实是大多数浏览场景的正确选择**：

- **电池续航**：Safari 在 Apple Silicon 上的能耗比 Chrome/Brave 低约 30-50%。WebKit 与 M2 的效率核心和 GPU 深度集成。
- **JavaScriptCore 是 ARM 原生**：JSC 已针对 Apple Silicon 进行调优——基准测试分数与 V8 不相上下。
- **WebKit 是开源的**：因此你并非完全处于黑盒引擎中。你可以阅读渲染代码、提交错误报告甚至贡献代码。
- **内存**：Safari 使用的 RAM 远少于基于 Chromium 的浏览器——这对你的 Air 仅有 16 GB 内存来说尤为重要。

## Brave — 最佳开源日常驱动

如果你想要完全开源和 Chromium 兼容性（对于 Web 开发工作很重要，因为大多数公司内部工具都针对 Chrome）：

```bash
brew install --cask brave-browser
```

Brave 在 M2 上是为 Apple Silicon 原生编译的，因此性能良好。但仍比 Safari 更耗电。

## Firefox — 值得拥有以实现引擎多样性

```bash
brew install --cask firefox
```

Gecko 在 M2 上表现不错。Firefox 是测试非 WebKit、非 Blink 渲染的唯一方式——如果你做前端工作，这很重要。

## 我为你的工作流推荐的设置

| 浏览器 | 使用场景 |
| --- | --- |
| **Safari** | 默认浏览、阅读、电池续航 |
| **Brave** | Web 开发、测试、需要 Chrome 兼容性的网站 |
| **Firefox** | 跨浏览器 QA、用于 CSS 调试的 DevTools |

## 对于自动化 / AI 工作

由于你构建 CLI 代理和爬虫——在 macOS 上，Playwright 对 M2 的支持很好：

```bash
pip install playwright
playwright install chromium  # or webkit, firefox
```

通过 Playwright 使用 WebKit 是 M2 上最轻量的选项，并使用 Safari 的引擎——适合在不使用模拟器的情况下测试 iOS 等效行为。

**总结：** 在 M2 上使用 Safari 作为主要浏览器——电池和内存优势是实实在在的，并且在工作日内累积。保留 Brave 用于开发工作。“开源浏览器”这个问题在 Mac 上不那么重要，因为最重要的组件（WebKit/JSC）已经是开源的，而且 Safari 就是基于它运行的。
