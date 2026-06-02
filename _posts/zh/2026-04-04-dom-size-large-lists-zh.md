---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大列表的DOM尺寸限制
translated: true
type: note
---

**问题**：浏览器中最多能渲染多少个这样的 li 项？我现在有 7000 多个项，可行吗？20000 个呢？

**答案**：

现代浏览器（Chrome、Firefox、Edge、Safari）对于 `<ul>` 或类似容器（如 Bootstrap `.list-group`）中可以放置的 `<li>` 元素数量**没有硬性的技术限制**。浏览器在技术上可以处理数万个 DOM 元素。

然而，**真正的限制在于性能**，而非严格的上限。以下是基于当前 Web 性能指南（截至 2026 年）的清晰说明：

### DOM 规模的性能指南

- 页面总 DOM 节点数 **少于 1,500** → 理想状态（Lighthouse/Chrome 推荐）。
- 在 **1,500 至 5,000 个节点**之间 → 在许多情况下可接受，但可能会开始注意到交互变慢。
- **超过 10,000 个节点** → 出现问题的风险较高（初始渲染慢、滚动卡顿、内存使用增加、点击或悬停等用户交互延迟）。

你单个 `<li class="list-group-item">` 元素包含：

- `<li>` 本身
- 一个 `<a>` 标签
- 几个 `<span>` 元素（日期、类型、标题）

这意味着**一个列表项 ≈ 5–6 个 DOM 节点**（加上 Bootstrap 添加的任何类或伪元素）。

- **7,000 个项** → 仅列表部分大约 **35,000 – 42,000 个 DOM 节点**（加上页面其余部分）。
  这在许多设备上**很可能会感觉卡顿**，尤其是在滚动、搜索或浏览器重新计算布局/样式时。初始页面加载和 JavaScript 操作也会变慢。

- **20,000 个项** → 大约 **100,000+ 个 DOM 节点**。
  这**通常不推荐**用于良好的用户体验。你可能会观察到：
  - 页面加载缓慢
  - 滚动卡顿或延迟
  - CPU/内存使用率升高
  - 在 Lighthouse 等工具中得分不佳（DOM 规模过大警告/错误）
  - 在低端设备或移动浏览器上可能无响应

### 为何大型列表会导致问题

浏览器必须：

- 构建庞大的 DOM 树
- 为每个元素（包括屏幕外的元素）计算样式和布局
- 当任何内容发生变化时处理重绘和重排
- 将所有元素保留在内存中

即使列表渲染出来了，**滚动浏览 7000 多个或 20000 个项**也会在不优化的情况下变得不流畅。

### 推荐解决方案

对于如此庞大的列表，**切勿**一次性渲染所有项。使用以下方法之一：

1. **虚拟滚动 / 视窗化**（最适合 7k–20k+ 项）
   仅渲染当前视口中可见的项（通常一次 10–30 个项）。随着用户滚动，新项被添加到 DOM，旧项被移除。
   常用库：
   - React：`react-window` 或 `react-virtualized`
   - Vue：`vue-virtual-scroller`
   - Angular：Angular CDK Virtual Scrolling
   - 原生 JavaScript：`Clusterize.js` 或自定义 Intersection Observer 实现

2. **分页**
   每页显示 50–200 个项，并提供“加载更多”或页码。

3. **无限滚动**（配合虚拟化）
   在用户滚动时加载更多项，但 DOM 中仍只保留有限数量。

4. **在服务器端或客户端进行过滤/搜索**
   让用户先搜索或过滤，以减少显示的项目数量。

5. **如果必须保留所有项，可进行简单优化**
   - 使用 `will-change: transform;` 或 CSS containment
   - 避免在列表项上使用复杂的 CSS（复杂选择器、阴影等）
   - 在 JavaScript 中构建列表时使用 `document.createDocumentFragment()`
   - 对于极端情况，可考虑使用固定布局的 `<table>` 或基于 canvas 的列表

### 快速测试建议

尝试在隐身窗口中渲染你的 7000 个项，并检查：

- Chrome DevTools → Performance 标签（记录一次滚动过程）
- Lighthouse 审计中的“Avoid excessive DOM size”项目
- 在中端笔记本电脑和手机上的滚动流畅度

如果你在 7000 个项时注意到卡顿，那么在增加到 20000 个项之前就应该实施虚拟化。

**总结**：

- 7000 个项处于**临界状态**——可能能用，但不是最优的。
- 20000 个项对于简单渲染的列表来说**太多了**，很可能会降低用户体验。

采用虚拟滚动可以让你流畅地处理 20k、50k 甚至 100k+ 的项。

**参考链接**：

- <https://developer.chrome.com/docs/lighthouse/performance/dom-size>
- <https://web.dev/articles/dom-size-and-interactivity>
- <https://www.debugbear.com/blog/excessive-dom-size>
