---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Era Developer Dashboard In Angular
translated: false
type: note
---

Question: How should I think about building an AI-era personal dashboard (showing GitHub activity, OpenRouter token usage, X/Twitter followers/following) in Angular 21, with drag-and-drop widgets? What similar projects can I reference? What should I name it?

Answer:

## Project Vision: The "AI-Era Developer Dashboard"

This is a genuinely exciting and well-timed project idea. You're essentially building a **personal command center for the AI developer** — combining social footprint, code activity, and LLM consumption in one customizable canvas. Think of it as a "Netvibes for the AI age."

---

## 🧠 Why Angular 21 is a Strong Choice Here

Angular 21, released at the end of 2025, brings Signal Forms as a reactive form API, zoneless change detection as the new default, Vitest as the modern test environment, Angular Aria for accessible components, and an enhanced MCP server for AI-supported development.

Key Angular 21 features that directly benefit your dashboard:

- **Signals-first reactivity** — Signal Forms eliminate the need for manual `valueChanges` subscriptions and the dreaded `takeUntil(this.destroy$)` pattern, making widget settings/config forms clean and reactive.
- **Zoneless change detection** — Zoneless change detection, which reached stability in v20.2 and is now the default in v21, removes zone.js entirely, reducing overhead and producing cleaner stack traces — this is huge for real-time dashboards with websockets or polling.
- **Standalone components** — each widget is a perfectly self-contained standalone component that can be lazily loaded.
- **Angular Aria** — the new Angular Aria component library provides 8 UI patterns and 13 components that are signals-based, fully responsive, and accessible — ideal for accessible widget containers and menus.

---

## 📦 Core Widgets to Build

| Widget | Data Source | API |
| --- | --- | --- |
| GitHub Activity Heatmap | GitHub REST/GraphQL | `api.github.com` |
| OpenRouter Token Usage | OpenRouter | `/api/v1/generation`, `/activity` |
| X/Twitter Followers/Following | Twitter API v2 | `api.twitter.com/2/users` |
| AI Cost Tracker | OpenRouter + Anthropic | Usage accounting APIs |
| Model Usage Chart | OpenRouter | Stats endpoint |

For OpenRouter specifically, key metrics you can surface include: total token usage (input vs output split), token usage over time, error rate, cache utilization percentage, model distribution, cost distribution by model, and request volume over time.

OpenRouter lets you include `usage: {include: true}` in requests to receive usage data in the response, and you can also review your history in the Activity section.

---

## 🔗 Similar Projects to Reference

### For Widget/Dashboard Architecture

- **[Dashy](https://dashy.to/)** — an open-source, self-hosted dashboard that comes bundled with 50+ pre-built widgets, supports status checks, themes, icon packs, and a UI editor. From the UI you can choose between different layouts, item sizes, show/hide components, and switch themes. This is your closest reference for the widget add/remove/customize UX.
- **[ngx-admin](https://github.com/akveo/ngx-admin)** — a customizable admin dashboard template based on Angular 10+, MIT licensed, with a rich widget ecosystem. Great for layout reference.
- **[ai-api-usage-monitor](https://github.com/kylnor/ai-api-usage-monitor)** — a multi-provider AI API usage and cost monitoring system for OpenAI, Anthropic Claude, OpenRouter, Google Gemini, ElevenLabs, and MiniMax with a dashboard and alerts. It includes real-time monitoring across 6 major AI providers, accurate cost tracking, and smart budget alerts via email, Slack, and webhooks.
- **[SigNoz OpenRouter Dashboard](https://signoz.io/docs/dashboards/dashboard-templates/openrouter-dashboard/)** — great reference for what metrics to show and how to lay out OpenRouter stats panels.

### For Grid/Drag-Drop Widget Layout

- **angular-gridster2** — the go-to Angular drag-and-drop resizable grid library (works well in Angular 21 with standalone components)
- **@angular/cdk DragDrop** — Angular's CDK offers behavior primitives such as Drag and Drop that you can include in your own custom-built components — keep it native for a lighter dependency footprint.

---

## 🏗️ Recommended Architecture

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

**State management**: Use Angular 21 Signals + `localStorage` persistence for dashboard layout config. No NgRx needed — signals are expressive enough.

**Widget protocol**: Define a `WidgetComponent` interface with a `config` input signal, a `title`, and a `refresh()` method. Every widget implements this interface.

---

## 🛠️ Suggested Tech Stack

| Layer | Choice | Reason |
| --- | --- | --- |
| Framework | Angular 21 | Signals, zoneless, standalone |
| UI Components | Angular Aria + Tailwind | Accessible, unstyled freedom |
| Charts | ngx-echarts or Chart.js | Both have Angular wrappers |
| Grid layout | angular-gridster2 | Mature, Angular-native |
| HTTP | Angular `HttpClient` (functional) | Built-in, signals-friendly |
| Auth/Keys | Angular Signal Store + encrypt-storage | Secure local key storage |
| Testing | Vitest (Angular 21 default) | Fast, zoneless-native |

---

## 💡 Project Name Suggestions

| Name | Vibe |
| --- | --- |
| **NexusBoard** | Hub of all your feeds — coding, AI, social |
| **TokenPulse** | Emphasizes the AI/token-era angle |
| **DevAura** | Your developer presence at a glance |
| **SignalBoard** | Double meaning — Angular Signals + social signals |
| **AIgrid** | Grid-based, AI-first |
| **VibeDash** | Leans into the "vibe coding" era, light and fun |
| **StackPulse** | Your full developer stack, live |
| **ContextPanel** | You monitor your context — code, AI, social |

**Personal pick**: **`SignalBoard`** — it's clever (Angular Signals + social signal monitoring), memorable, and domain-worthy.

---

## 🚀 Getting Started Checklist

1. `ng new signal-board --standalone` — scaffolds Angular 21 standalone project
2. Install `angular-gridster2` for drag/drop widget grid
3. Create a `WidgetRegistryService` with a signal-based list of active widgets
4. Build GitHub widget first (public API, no auth needed for public profiles)
5. Add OpenRouter widget using the `/api/v1/generation` stats endpoint
6. Twitter/X widget last — API v2 requires OAuth 2.0, plan ahead
7. Add a `+` button to open a widget catalog modal — pick and add to grid
8. Persist layout JSON to `localStorage` on every drag/resize

---

## ⚠️ Potential Challenges

- **Twitter API v2** has strict rate limits on the free tier; consider polling intervals of 15 min+
- **CORS**: OpenRouter and GitHub are CORS-friendly; Twitter is not — you'll need a lightweight proxy (Cloudflare Worker or simple Node/Deno edge function)
- **API key security**: Never hardcode keys. Store in `sessionStorage` or a lightweight encrypted store with a user-set passphrase

References:

- [OpenRouter API Reference](https://openrouter.ai/docs/api/reference/overview)
- [OpenRouter Support – Usage Tracking](https://openrouter.ai/support)
- [Dashy – Open Source Widget Dashboard](https://dashy.to/)
- [ai-api-usage-monitor on GitHub](https://github.com/kylnor/ai-api-usage-monitor)
- [Announcing Angular v21 – Official Blog](https://blog.angular.dev/announcing-angular-v21-57946c34f14b)
- [What's New in Angular 21 – Angular Architects](https://www.angulararchitects.io/blog/whats-new-in-angular-21-signal-forms-zone-less-vitest-angular-aria-cli-with-mcp-server/)
- [SigNoz OpenRouter Dashboard Template](https://signoz.io/docs/dashboards/dashboard-templates/openrouter-dashboard/)
- [ngx-admin on GitHub](https://github.com/akveo/ngx-admin)
