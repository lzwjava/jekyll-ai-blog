---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Angular 升级中的 AG Grid 版本指南
translated: true
type: note
---

Question: AG Grid 的版本是如何演进的？特别是如果我们将 Angular 从 9 升级到 Angular 14 或 17，应该如何选择 AG Grid 的版本？

Answer:

AG Grid（包括 `ag-grid-community` 和 `ag-grid-angular`）遵循定期的发布周期，大约每 6 个月发布一个 Major 版本，并频繁发布 Minor/Patch 版本。截至 2026 年初，最新版本约为 **35.x**（例如 35.0.1 或 35.1.0），其中包括许多性能优化、新功能（如更好的 date/time 分组、tool panel 增强和 charting 更新）以及对现代 Angular 版本的持续支持。

**ag-grid-angular** 包经历了显著的演变：

- 较旧版本（≈ v23–v27）用于 Angular 9–11。
- v28 前后发生了重大 Breaking changes（改进了 Ivy 支持，移除了旧版 wrappers）。
- 从 v30 开始，停止了对极旧 Angular 版本的遗留支持。
- 较新版本逐渐提高了对 Angular 的最低要求（例如，v32 需要 Angular 16+，v33 需要 Angular 17+）。

### AG Grid 与 Angular 兼容性表（基于 2026 年初官方图表）

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

### 升级 Angular 时的建议

- **Angular 9 → Angular 14**
  你可以（并且应该）显著升级 AG Grid —— 从 ~23–27.x 升级到 **31.x**（或至少是 30.x）。
  这次跳跃可以让你获得许多新功能、更好的 tree data、server-side row model 改进、现代 TypeScript 支持以及性能提升。
  避免停留在非常旧的 AG Grid 版本（≤27），因为这些版本缺失了多年的 Bug 修复和优化。

- **Angular 9 → Angular 17**
  将 AG Grid 升级到 **34.x**（如果你以后会升级到 Angular 18+，则选择最新的 35.x）。
  版本 ≥33 通常需要 Angular 17+，因此目标定在 **34.x** 是在 Angular 17 环境下平衡新功能与稳定性的最佳选择。

### 选择/升级 AG Grid 版本的实际步骤

1. 首先升级 Angular（按照 Angular 官方 Update Guide 逐步进行：9→10→11→...）。
2. 在每个 Angular Major 版本升级后，根据上表将 `ag-grid-angular` + `ag-grid-community` 更新到兼容的版本。
3. 在兼容范围内使用最高的 Patch/Minor 版本（例如，对于 Angular 17，优先选择 34.2.x 或 34.3.x，而不是 28.x）。
4. 查看 [changelog](https://www.ag-grid.com/changelog) 和特定的 "Upgrading to AG Grid XX" 指南（特别是针对 28、30、32、33 版本），了解 Breaking changes。
5. 测试自定义 cell renderers / editors —— 许多旧模式（例如 `AgGridModule.withComponents()`）在 v28 左右已被移除。

**总结** —— 从 Angular 9 迁移到 14 时，选择 AG Grid **~31.x**；迁移到 Angular 17 时，选择 **~34.x**（如果你还能更新到更新的 Angular，则选最新的 35.x）。这将为你提供现代化的功能和长期的可维护性。

参考资料：

- [AG Grid Angular Version Compatibility Chart](https://www.ag-grid.com/angular-data-grid/compatibility)
- [AG Grid Changelog](https://www.ag-grid.com/changelog)
- [ag-grid-angular on npm](https://www.npmjs.com/package/ag-grid-angular)
