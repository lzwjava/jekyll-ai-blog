---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 深入了解 Pretext 文本布局库
translated: true
type: note
---

Question: What is the Pretext library by Cheng Lou, and how does it work?

Answer: **Pretext** 是由 Cheng Lou（React 核心贡献者及 ReasonML 创始人）开发的一个高性能 JavaScript/TypeScript 库，专为多行文本测量（measurement）和布局（layout）而设计。它解决了 Web 性能中的一个根本性瓶颈：由从 DOM 读取文本指标（metrics）引起的“布局抖动”（layout thrashing）。

传统上，计算段落高度或寻找换行位置需要浏览器执行同步布局（例如通过 `getBoundingClientRect` 或 `offsetHeight`），这在计算上非常昂贵。Pretext 通过使用两阶段架构进行数学层面的布局预测，完全绕过了 DOM。

### **Core Architecture: The Two-Phase Model**

Pretext 将工作分为“高开销”的设置阶段和“极速”的执行阶段：

1.  **`prepare()` (Measurement 阶段):**
    * **Segmentation:** 使用 `Intl.Segmenter` 将文本拆分为单词、Emojis 和特定的换行点（如 soft hyphens）。
    * **Measurement:** 使用 `canvas.measureText()` 代替 DOM。该接口直接与浏览器的 font engine 通信，而不会触发页面 reflow。
    * **Caching:** 这些分段的宽度被缓存到一个 Map 中（`Map<font, Map<segment, metrics>>`）。这是一次性开销（处理大批量文本大约需要 17-19ms）。

2.  **`layout()` (Hot Path):**
    * **Pure Arithmetic:** 一旦分段测量完成，计算文本在何处换行就变成了一个简单的数学问题：累加缓存的宽度，直到达到 `maxWidth`。
    * **Performance:** 由于在此阶段避免了所有 DOM 和 Canvas 调用，它的速度极快——在 500 条文本的批量测试中约为 **0.10ms**（比传统方法快约 200 倍）。

### **Key Features & Use Cases**

* **Virtualization & Occlusion:** 它在文本渲染前提供准确的块高度，从而实现完美的“滚动虚拟化”（scroll virtualization，仅渲染屏幕上的内容），且没有预估高度带来的“跳动”感。
* **Advanced UI Layouts:** 通过手动计算逐行宽度，实现复杂的 UI 效果，例如让容器紧贴文本宽度的“收缩包裹”（shrink-wrapping），或让文本绕流不规则形状（如图像）。
* **Internationalization:** 它为双向（BiDi）文本（如阿拉伯语/英语混排）、Emojis 以及 CJK（中文、日文、韩文）语言提供生产级的支持。
* **Cross-Platform Rendering:** 虽然它可以用于定位标准 DOM 节点，但其数学输出允许将文本渲染到 **Canvas、SVG 或 WebGL**，而这些技术传统上缺乏复杂的多行换行逻辑。

### **Usage Example**

```typescript
import { prepare, layout } from '@chenglou/pretext';

// 1. Prepare: 测量并缓存（仅执行一次）
const prepared = prepare('Hello world! 🚀', '16px Inter');

// 2. Layout: 纯数学计算（可以在每一帧或每次 resize 时安全调用）
const { height, lineCount } = layout(prepared, 300, 20);
// 返回在 300px 宽度和 20px 行高下的高度
```

### **Why It Matters**

Pretext 将文本布局的职责从浏览器不透明的 CSS 引擎转移到了“用户态”的 JavaScript 中。这让开发者在浏览器中获得了类似于桌面出版应用（如 Apple Pages 或 Keynote）的精度，开启了开发一类全新的、高度交互且文本密集型用户界面的可能性。

References:

* [chenglou/pretext - GitHub Repository](https://github.com/chenglou/pretext)
* [You're Looking at the Wrong Pretext Demo - DEV Community](https://dev.to/denodell/youre-looking-at-the-wrong-pretext-demo-4960)
* [Pretext: TypeScript library for multiline text measurement and layout - Hacker News](https://news.ycombinator.com/item?id=47556290)
