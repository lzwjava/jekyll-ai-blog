---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare 核心网页指标详解
translated: true
type: note
---

**问题：** Cloudflare 控制面板中的 LCP、INP 和 CLS（Core Web Vitals）是什么意思？

**回答：**

这些是 Google 的 Core Web Vitals — 三个从真实访客浏览器中测量的用户体验指标（RUM，真实用户监控）。Cloudflare 通过在 **Web Analytics**（以及 Observatory）中注入一个小型信标脚本，报告实际用户的体验，然后聚合每个指标的第 75 百分位数。

各指标含义：

**LCP — Largest Contentful Paint（最大内容绘制）**（加载速度）
从导航开始到最大可视元素（主图、大标题 `<h1>`、视频海报）完成渲染的时间。

- 良好：≤ 2.5s | 需要改进：2.5–4s | 较差：> 4s
- 主要影响因素：TTFB、阻塞渲染的 CSS/JS、图片大小、服务器位置。Cloudflare 的杠杆：边缘缓存、Polish/图片缩放、Early Hints、HTTP/3。

**INP — Interaction to Next Paint（交互到下一次绘制）**（响应性）
用户交互（点击、触摸、按键）到下一次帧绘制之间的最差延迟。2024 年 3 月取代了 FID，因为 FID 只测量了首次输入的延迟；INP 采样整个会话中的所有交互。

- 良好：≤ 200ms | 需要改进：200–500ms | 较差：> 500ms
- 主要影响因素：长时间的主线程 JS 任务、繁重的事件处理程序、水合成本。这几乎完全取决于你的客户端 JS — Cloudflare 无法为你修复（不过通过 Zaraz 延迟第三方脚本有所帮助）。

**CLS — Cumulative Layout Shift（累积布局偏移）**（视觉稳定性）
无单位分数，累计加载过程中可见内容意外跳动的总量（缺少 `width`/`height` 的图片、后期注入的广告、字体切换）。

- 良好：≤ 0.1 | 需要改进：0.1–0.25 | 较差：> 0.25

在信任控制面板数据之前，可以用以下命令在本地快速检查：

```bash
npx lighthouse https://lzwjava.github.io --only-categories=performance --view
```

或者使用 Cloudflare 信标所用的相同库在浏览器控制台中测量：

```js
import {onLCP, onINP, onCLS} from 'https://unpkg.com/web-vitals@4?module';
onLCP(console.log); onINP(console.log); onCLS(console.log);
```

关于 Cloudflare 数据的注意事项：它们来自实际流量的现场数据，因此会不同于 Lighthouse 实验室运行结果（实验室使用限速的合成设备）。如果 Cloudflare 显示 LCP 较差但 Lighthouse 看起来正常，那么你的真实用户很可能离源站较远或处于慢速网络 — 这正是边缘缓存可以解决的问题。对于像你这样的 GitHub Pages 博客，LCP 和 CLS 是值得关注的；INP 在 JS 极少的静态站点上很少成为问题。
