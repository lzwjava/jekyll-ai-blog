---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular Upgrade Manual Testing Guide
translated: false
type: note
---

Question: If a frontend application is upgraded from Angular 9 to Angular 14, how should manual testing be performed, and what aspects of the app should we focus on?

Answer:

Upgrading from **Angular 9 → 14** spans five major versions (10, 11, 12, 13, 14), so even when automated migrations (ng update) run successfully, many subtle and visual/behavioral regressions can appear. Manual exploratory testing becomes very important.

### Recommended Manual Testing Approach

1. **Smoke test the entire application** after the upgrade is stable (builds, starts, no console errors).
2. **Follow main user journeys** end-to-end (happy paths + common error paths).
3. **Compare behavior side-by-side** (old Angular 9 version vs new Angular 14 version) whenever possible.
4. **Use different browsers** (Chrome, Firefox, Edge, Safari) — especially check mobile viewports / responsive design.
5. **Test with real data** (staging environment, production-like data) — synthetic data often hides issues.
6. **Pay special attention to slow / data-heavy / animation-heavy screens**.
7. **Record short screencasts** of critical flows before & after upgrade — makes regression spotting much easier.
8. **Involve domain / business users** in final UAT phase — developers often miss "feels wrong" issues.

### Key Areas to Focus On During Manual Testing

| Priority | Area                          | What Exactly to Check / Common Breakage Points (9→14)                                                                 | Why It Breaks Frequently |
|--------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------|
| ★★★★★  | **Routing & Navigation**      | • Deep linking<br>• Back/forward browser buttons<br>• Lazy-loaded modules load correctly?<br>• Guards / resolvers<br>• Auxiliary routes (if used) | pathMatch defaults became stricter, resolver behavior changed, many router lifecycle tweaks |
| ★★★★★  | **Forms (Template-driven + Reactive)** | • Validation messages appear at correct time<br>• Disabled / readonly state<br>• Custom validators / async validators<br>• Form value / status changes propagate correctly<br>• Dirty / touched / pristine flags | Angular 14 introduced much stricter typing → subtle coercion bugs surface |
| ★★★★☆  | **Change Detection & Performance** | • UI does **not** flicker / re-render unnecessarily<br>• Infinite change detection loops (console warning)<br>• Slow lists / large tables still usable?<br>• Components inside *ngIf / ngSwitch update correctly | Ivy + stricter change detection + new zone.js behaviors |
| ★★★★☆  | **Templates & Directives**    | • Structural directives (*ngIf,*ngFor, *ngSwitch)<br>• Custom structural / attribute directives<br>• @Input / @Output bindings<br>• Two-way bindings [(ngModel)] | New template type checking is stricter, some old patterns are now warned / broken |
| ★★★★☆  | **HTTP / Interceptors / API calls** | • All HTTP calls still work<br>• Interceptors modify / catch errors correctly<br>• Loading spinners / disabled states during requests<br>• Error handling UI (toast, modal, inline) | HttpClient changes + RxJS updates (v6 → v7) |
| ★★★★☆  | **Third-party libraries & Components** | • Angular Material → check theme, typography, density<br>• Charts (ng2-charts, highcharts-angular…)<br>• Tables (ag-grid, prime-ng, material table)<br>• Modals / dialogs / overlays<br>• Date pickers / file upload components | Many libs had major version jumps + breaking changes |
| ★★★☆☆  | **Animations & Transitions**  | • Enter / leave animations<br>• Route animations<br>• @.disabled / :increment / :decrement | Animation DSL had fixes & deprecations |
| ★★★☆☆  | **Internationalization (i18n)** | • Translations still load<br>• Plural / gender rules correct<br>• RTL languages (if supported) | i18n tooling & extraction improved → old extraction can break |
| ★★★☆☆  | **Accessibility (a11y)**      | • Screen reader behavior<br>• Focus management (modals, menus)<br>• Keyboard navigation<br>• ARIA attributes | Some old patterns are now flagged by extended diagnostics |
| ★★★☆☆  | **Browser Console & Warnings** | • No red errors<br>• No yellow deprecation / Ivy / zone.js warnings<br>• No "ExpressionChangedAfterItHasBeenCheckedError" | Many old patterns now produce warnings |
| ★★☆☆☆  | **Build & Bundle Size**       | • Application still loads reasonably fast<br>• No huge regressions in bundle size | Ivy + differential loading changes + tree-shaking improvements |
| ★★☆☆☆  | **Edge Cases**                | • Empty states<br>• Very long content / overflow<br>• Very large forms / lists<br>• Offline mode (if implemented)<br>• Copy-paste / drag-drop features | Often not covered by unit tests |

### Quick Checklist Summary for Testers

- [ ] Login / authentication flows (including social login if any)
- [ ] Main navigation + sidebar / topbar
- [ ] CRUD operations on main entities
- [ ] Search / filtering / sorting
- [ ] Form submission + validation
- [ ] File upload / download (if exists)
- [ ] Any real-time / polling / websocket features
- [ ] Export to Excel/PDF
- [ ] Responsive design on phone/tablet/desktop
- [ ] Browser back/forward/refresh behavior

Follow the official **Angular Update Guide** (<https://angular.dev/update-guide>) and read release notes / breaking changes summaries for versions 10–14.

Careful manual testing + good before/after comparison is usually the difference between "it works on my machine" and "production is broken".

References:

- [Angular Update Guide](https://angular.dev/update-guide)
- [Angular 14 Release Notes & Breaking Changes Discussion](https://github.com/angular/angular/blob/main/CHANGELOG.md) (look for v10 to v14 sections)
