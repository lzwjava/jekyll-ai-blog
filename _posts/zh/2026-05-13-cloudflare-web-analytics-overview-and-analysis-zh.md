---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare 网站分析概览与解析
translated: true
type: note
---

问题：Cloudflare Web Analytics 可以做什么（例如查看访问的URL、国家等）？你能分析来自 lzwjava.github.io 的报告吗？

回答：

## Cloudflare Web Analytics 的功能

Cloudflare Web Analytics 支持在核心网页指标（Core Web Vitals）中进行交互式探索，允许你按 **URL、浏览器、操作系统、国家和元素** 筛选数据。这是一款注重隐私、无需 cookie 的工具——它通过轻量级 JavaScript 信标直接从用户浏览器收集性能数据，而不跟踪用户或存储客户端状态。

主要可查看的内容：

- **哪些 URL 被访问**——查看哪些页面获得最多流量
- **访问者来自哪些国家**
- **使用了哪些浏览器和操作系统**
- **每个页面的核心网页指标**——每个 URL 的 LCP、INP、CLS
- **调试视图**——精确定位导致性能问题的具体 DOM 元素
- **页面加载指标**——百分位细分（P50、P75、P90、P99）

---

## lzwjava.github.io 分析（2026年4月13日 – 5月13日）

### 1. 最大内容绘制（LCP）——加载速度

**结果：89% 良好 / 5% 需要改善 / 6% 较差**

良好的 LCP 分数应在 2.5 秒以内。你的网站基本达标，但异常值值得关注：

| 百分位 | 数值 | 评估 |
|---|---|---|
| P50（中位数） | 560ms | 优秀 |
| P75 | 1,404ms | 良好 |
| P90 | 2,608ms | 临界 / 需要改善 |
| P99 | 11,368ms | 非常差 |

P99 峰值 **11 秒** 表明有一小部分用户（可能网络较慢或使用移动设备）经历了非常缓慢的加载。流量最大的 URL 是 `/notes-en`、`/`（首页）、`/notes-zh.html` 和 `/index-zh.html`。

---

### 2. 与下一次绘制的交互（INP）——响应能力

**结果：98% 良好 / 2% 需要改善 / 0% 较差**

INP 通过观察所有点击、触摸和键盘交互的延迟来衡量页面整体对用户交互的响应能力。这是一个非常出色的分数。

然而，**调试视图** 显示有两个特定元素存在缓慢交互：

- `#moonIcon > path` — **312ms**（10 次）——这很可能是深色模式切换按钮
- `html.dark-mode > body` — **472ms**（10 次）——这表明深色模式切换触发了整个页面主体的缓慢重绘

良好的 INP 阈值应在 200ms 以下。这两者均高于阈值，意味着深色模式切换是你网站上主要的交互性瓶颈。

---

### 3. 累积布局偏移（CLS）——视觉稳定性

**结果：100% 良好 / 0% 需要改善 / 0% 较差**

良好的 CLS 分数应在 0.1 以下。你的网站在此项得分完美——没有出现影响用户的意外布局偏移。

不过，调试视图显示了一个值得注意的元素：

- `#content > div.language-bash.highlighter-rouge > div.highlight > pre.highlight` — CLS 分数 **0.301**（10 次）

这意味着在你的某个笔记页面中，一个 **bash 代码块** 导致了布局偏移，分数为 0.301，技术上属于“较差”范围（高于 0.1）。它仅影响 10 次页面浏览，因此并不普遍，但仍值得修复（例如，为代码块预留空间或使用 `overflow: auto`）。

---

## 总结与建议

| 指标 | 分数 | 状态 |
|---|---|---|
| LCP | 89% 良好 | ✅ 基本正常；调查 P99 峰值 |
| INP | 98% 良好 | ✅ 优秀；修复深色模式切换延迟 |
| CLS | 100% 良好 | ✅ 整体完美；修复 bash 代码块偏移 |

**主要待办事项：**

1. **深色模式切换**（`#moonIcon`）速度较慢，为 312–472ms——考虑使用防抖或优化 CSS 类切换，而不是重绘整个 body。
2. **Bash 代码块** 导致 CLS 为 0.301——添加固定尺寸或 `min-height` 以防止加载时布局偏移。
3. **P99 LCP 为 11 秒**——调查是否有大图或阻塞渲染的资源影响慢速访问者，尤其是在首页（`lzwjava.github.io/`）。

参考资料：

- [Cloudflare 核心网页指标文档](https://developers.cloudflare.com/web-analytics/data-metrics/core-web-vitals/)
- [核心网页指标说明（2026）](https://www.corewebvitals.io/core-web-vitals)
- [Cloudflare 指标探索器博客](https://blog.cloudflare.com/web-analytics-vitals-explorer/)
