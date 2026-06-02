---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: AG Grid Version Guide for Angular Upgrades
translated: false
type: note
---

Question: How have the ag-grid packages developed in terms of versions? Especially, if we upgrade Angular from 9 to Angular 14 or 17, how should we choose the version of ag-grid?

Answer:

AG Grid (including `ag-grid-community` and `ag-grid-angular`) follows a regular release cycle with major versions every ~6 months and minor/patch releases more frequently. As of early 2026, the latest versions are around **35.x** (e.g., 35.0.1 or 35.1.0), which include many performance improvements, new features (like better date/time grouping, tool panel enhancements, and charting updates), and ongoing support for modern Angular versions.

The **ag-grid-angular** package has evolved significantly:

- Older versions (≈ v23–v27) were used with Angular 9–11.
- Major breaking changes occurred around v28 (Ivy support improvements, removal of legacy wrappers).
- From v30 onward, legacy support for very old Angular versions was dropped.
- Newer versions gradually raised the minimum Angular requirement (e.g., v32 requires Angular 16+, v33 requires Angular 17+).

### AG Grid & Angular Compatibility (based on official chart, early 2026)

| Angular Version | Compatible AG Grid Versions          | Recommended / Latest Possible |
|-----------------|--------------------------------------|-------------------------------|
| 9               | 23 – 27                              | ~27.x (last good match)       |
| 10–11           | 24 – 27                              | ~27.x                         |
| 12–13           | 25 – 30                              | ~30.x                         |
| 14–15           | 25 – 31                              | ~31.x                         |
| 16              | 28 – 32                              | ~32.x                         |
| 17              | 28 – 34                              | ~34.x                         |
| 18              | 28 – 35                              | ~35.x                         |
| 19–21           | 28 – 35+                             | 35.x (latest)                 |

### Recommendations when upgrading Angular

- **Angular 9 → Angular 14**
  You can (and should) upgrade AG Grid significantly — from ~23–27.x → **31.x** (or at least 30.x).
  This jump gives access to many new features, better tree data, server-side row model improvements, modern TypeScript support, and performance gains.
  Avoid staying on very old AG Grid versions (≤27) — they miss years of bug fixes and optimizations.

- **Angular 9 → Angular 17**
  Upgrade AG Grid to **34.x** (or the latest 35.x if you go to Angular 18+ later).
  Versions ≥33 typically require Angular 17+, so target **34.x** for the best balance of new features and stability with Angular 17.

### Practical steps for choosing / upgrading ag-grid version

1. First upgrade Angular (follow official Angular Update Guide step-by-step: 9→10→11→…).
2. After each Angular major version, update `ag-grid-angular` + `ag-grid-community` to a compatible version from the table above.
3. Use the highest patch/minor version within the compatible range (e.g., for Angular 17 → prefer 34.2.x or 34.3.x over 28.x).
4. Check the [changelog](https://www.ag-grid.com/changelog) and specific "Upgrading to AG Grid XX" guides (especially for 28, 30, 32, 33) for breaking changes.
5. Test custom cell renderers / editors — many old patterns (e.g., `AgGridModule.withComponents()`) were removed around v28.

**Summary** — When moving from Angular 9 to 14, choose AG Grid **~31.x**; to Angular 17, choose **~34.x** (or latest 35.x if you can also update to newer Angular). This gives you modern features and long-term maintainability.

References:

- [AG Grid Angular Version Compatibility Chart](https://www.ag-grid.com/angular-data-grid/compatibility)
- [AG Grid Changelog](https://www.ag-grid.com/changelog)
- [ag-grid-angular on npm](https://www.npmjs.com/package/ag-grid-angular)
