---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI 时代 Angular 开发者仪表板
translated: true
type: note
---

## 项目愿景：The "AI-Era Developer Dashboard"

这是一个真正令人兴奋且时机恰当的项目想法。您本质上是在构建一个 **AI 开发者的个人指挥中心** — 将社交足迹、代码活动和 LLM 消耗结合在一个可自定义的画布中。将它想象成“AI 时代的 Netvibes”。

---

## 🧠 为什么 Angular 21 是这里的一个强有力选择

Angular 21 于 2025 年底发布，带来了 Signal Forms 作为响应式表单 API、zoneless change detection 作为新默认、Vitest 作为现代测试环境、Angular Aria 用于可访问组件，以及增强的 MCP server 用于 AI 支持的开发。

直接惠及您的仪表板的 Angular 21 关键特性：

- **Signals-first reactivity** — Signal Forms 消除了手动 `valueChanges` 订阅和令人畏惧的 `takeUntil(this.destroy$)` 模式的需要，使小部件设置/配置表单干净且响应式。
- **Zoneless change detection** — Zoneless change detection 在 v20.2 中达到稳定，并在 v21 中成为默认，完全移除 zone.js，减少开销并产生更干净的堆栈跟踪 — 这对于使用 websockets 或轮询的实时仪表板至关重要。
- **Standalone components** — 每个小部件都是一个完美的自包含 standalone component，可以懒加载。
- **Angular Aria** — 新的 Angular Aria 组件库提供了 8 种 UI 模式和 13 个基于 signals 的组件，完全响应式且可访问 — 非常适合可访问的小部件容器和菜单。

---

## 📦 核心小部件构建

| 小部件 | 数据源 | API |
| --- | --- | --- |
| GitHub Activity Heatmap | GitHub REST/GraphQL | `api.github.com` |
| OpenRouter Token Usage | OpenRouter | `/api/v1/generation`, `/activity` |
| X/Twitter Followers/Following | Twitter API v2 | `api.twitter.com/2/users` |
| AI Cost Tracker | OpenRouter + Anthropic | Usage accounting APIs |
| Model Usage Chart | OpenRouter | Stats endpoint |

对于 OpenRouter 具体来说，您可以展示的关键指标包括：总令牌使用量（输入 vs 输出拆分）、随时间变化的令牌使用量、错误率、缓存利用率百分比、模型分布、按模型的成本分布，以及随时间变化的请求量。

OpenRouter 允许您在请求中包含 `usage: {include: true}` 以在响应中接收使用数据，您还可以在 Activity 部分查看您的历史记录。

---

## 🔗 可参考的类似项目

### 小部件/仪表板架构

- **[Dashy](https://dashy.to/)** — 一个开源、自托管的仪表板，捆绑了 50+ 个预构建小部件，支持状态检查、主题、图标包和 UI 编辑器。从 UI 中，您可以选择不同的布局、项目大小、显示/隐藏组件，并切换主题。这是小部件添加/移除/自定义 UX 的最近参考。
- **[ngx-admin](https://github.com/akveo/ngx-admin)** — 基于 Angular 10+ 的可自定义管理仪表板模板，MIT 许可，具有丰富的生态小部件。非常适合布局参考。
- **[ai-api-usage-monitor](https://github.com/kylnor/ai-api-usage-monitor)** — 一个多提供商 AI API 使用和成本监控系统，支持 OpenAI、Anthropic Claude、OpenRouter、Google Gemini、ElevenLabs 和 MiniMax，带有仪表板和警报。它包括对 6 大主要 AI 提供商的实时监控、准确的成本跟踪，以及通过电子邮件、Slack 和 webhooks 的智能预算警报。
- **[SigNoz OpenRouter Dashboard](https://signoz.io/docs/dashboards/dashboard-templates/openrouter-dashboard/)** — 展示 OpenRouter 统计面板指标和布局的绝佳参考。

### 网格/拖拽小部件布局

- **angular-gridster2** — Angular 拖拽可调整大小网格库的首选（在 Angular 21 的 standalone components 中工作良好）
- **@angular/cdk DragDrop** — Angular 的 CDK 提供行为原语，如 Drag and Drop，您可以将其包含在自己的自定义组件中 — 保持原生以获得更轻的依赖足迹。

---

## 🏗️ 推荐架构

```
src/
├── widgets/                    # Each widget = standalone component
│   ├── github-heatmap/
│   ├── openrouter-tokens/
│   ├── twitter-profile/
│   ├── ai-cost-chart/
│   └── widget-registry.ts      # Registry for dynamic widget loading
├── core/
│   ├── dashboard-store.ts      # Signal-based state (layout, widget config)
│   ├── api/                    # Per-service API services
│   └── widget.model.ts
├── layout/
│   ├── grid.component.ts       # CDK-based drag/drop grid
│   └── widget-shell.component.ts
└── settings/
    └── api-keys.component.ts   # Store keys in localStorage/encrypted
```

**状态管理**：使用 Angular 21 Signals + `localStorage` 持久化仪表板布局配置。不需要 NgRx — signals 足够表达力。

**小部件协议**：定义一个 `WidgetComponent` 接口，带有 `config` 输入 signal、`title` 和 `refresh()` 方法。每个小部件实现此接口。

---

## 🛠️ 建议技术栈

| 层 | 选择 | 原因 |
| --- | --- | --- |
| Framework | Angular 21 | Signals, zoneless, standalone |
| UI Components | Angular Aria + Tailwind | 可访问、无样式自由 |
| Charts | ngx-echarts or Chart.js | 两者都有 Angular 包装器 |
| Grid layout | angular-gridster2 | 成熟、Angular 原生 |
| HTTP | Angular `HttpClient` (functional) | 内置、signals 友好 |
| Auth/Keys | Angular Signal Store + encrypt-storage | 安全的本地密钥存储 |
| Testing | Vitest (Angular 21 default) | 快速、zoneless 原生 |

---

## 💡 项目名称建议

| 名称 | 风格 |
| --- | --- |
| **NexusBoard** | 所有您的 feeds 的枢纽 — 编码、AI、社交 |
| **TokenPulse** | 强调 AI/令牌时代角度 |
| **DevAura** | 您的开发者存在一目了然 |
| **SignalBoard** | 双重含义 — Angular Signals + 社交信号 |
| **AIgrid** | 基于网格、AI 优先 |
| **VibeDash** | 倾向于“vibe coding”时代，轻快有趣 |
| **StackPulse** | 您的完整开发者栈，实时 |
| **ContextPanel** | 您监控您的上下文 — 代码、AI、社交 |

**个人推荐**：**`SignalBoard`** — 它巧妙（Angular Signals + 社交信号监控）、易记且值得域名。

---

## 🚀 入门检查清单

1. `ng new signal-board --standalone` — 搭建 Angular 21 standalone 项目
2. 安装 `angular-gridster2` 用于拖拽小部件网格
3. 创建一个带有基于 signal 的活动小部件列表的 `WidgetRegistryService`
4. 先构建 GitHub 小部件（公共 API，无需认证即可用于公共资料）
5. 使用 `/api/v1/generation` 统计端点添加 OpenRouter 小部件
6. Twitter/X 小部件放最后 — API v2 需要 OAuth 2.0，提前规划
7. 添加一个 `+` 按钮打开小部件目录模态框 — 选择并添加到网格
8. 在每次拖拽/调整大小时将布局 JSON 持久化到 `localStorage`

---

## ⚠️ 潜在挑战

- **Twitter API v2** 的免费层有严格的速率限制；考虑 15 分钟+ 的轮询间隔
- **CORS**：OpenRouter 和 GitHub 是 CORS 友好的；Twitter 不是 — 您需要一个轻量级代理（Cloudflare Worker 或简单的 Node/Deno 边缘函数）
- **API 密钥安全**：切勿硬编码密钥。存储在 `sessionStorage` 或带有用户设置口令的轻量级加密存储中

参考资料：

- [OpenRouter API Reference](https://openrouter.ai/docs/api/reference/overview)
- [OpenRouter Support – Usage Tracking](https://openrouter.ai/support)
- [Dashy – Open Source Widget Dashboard](https://dashy.to/)
- [ai-api-usage-monitor on GitHub](https://github.com/kylnor/ai-api-usage-monitor)
- [Announcing Angular v21 – Official Blog](https://blog.angular.dev/announcing-angular-v21-57946c34f14b)
- [What's New in Angular 21 – Angular Architects](https://www.angulararchitects.io/blog/whats-new-in-angular-21-signal-forms-zone-less-vitest-angular-aria-cli-with-mcp-server/)
- [SigNoz OpenRouter Dashboard Template](https://signoz.io/docs/dashboards/dashboard-templates/openrouter-dashboard/)
- [ngx-admin on GitHub](https://github.com/akveo/ngx-admin)
