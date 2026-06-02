---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AG Grid 升级指南 v20 至 30+
translated: true
type: note
---

**Question:** Compare AG Grid 20+ version and AG Grid 30+ version. If we upgrade it, then how to fix errors, how to upgrade it?

**Answer:**

AG Grid version 20（大约 2019 年初）比 version 30+（version 30 于 2023 年年中发布，2026 年的当前版本已达到 35+）要旧得多。从 v20.x 升级到 v30+ 意味着跨越了大约 10 个主版本的 **巨大跳跃**，涉及到许多新功能、性能改进、更好的 TypeScript 支持、现代 Theming（主题化）以及多个 Breaking changes。

### Key Differences (v20+ vs v30+)

- **v30+ 中的新特性 (v20 中没有):**
  - 具有自动类型推断的 Cell data types
  - 内置 Cell editors（更丰富的编辑体验）
  - 用于 Server-side row model 的 Group footer rows
  - 支持按当前的展开/折叠状态将 Row groups 导出到 Excel
  - Advanced filtering 改进（在后期的次要版本中支持布尔表达式）
  - 使用 CSS variables 的现代 Theming 系统（自 v28 左右引入）
  - 更好的 Module 注册机制（按 Grid 注册而非全局注册）
  - 改进的 React/Angular/Vue 集成和 Ivy 支持
  - 大量的性能和 Accessibility（可访问性）增强

- **Breaking Changes 和移除的内容:**
  - 移除了 v20–v29 中弃用的 API（例如：旧的 Module 系统、某些属性/方法）
  - Module 注册在 v22–v23 左右发生了剧变（转向 `@ag-grid-community/all-modules` 或 `@ag-grid-enterprise/all-modules`）
  - Theming 从旧的 Sass-based 迁移到 CSS variable-based（v28+ 左右的重大转变）
  - TypeScript 要求提高（v29+ 需要更新的 TS 版本）
  - Column 默认值更改（例如：在后续版本中 `sortable` / `resizable` 默认设为 true）
  - 一些 Component 注册和 Grid option 行为进行了更新

- **升级的好处:**
  - 处理大数据集时性能显著提升
  - 现代框架兼容性（例如：Angular 16+、React 18+）
  - 新的 Enterprise 功能（如果使用 Enterprise 版本）
  - 面向未来的代码（v20 已不再受支持）

### How to Upgrade from AG Grid v20+ to v30+

由于累积的 Breaking changes，**不建议**直接从 v20 一步升级到 v30+。请采用增量升级的方法。

1. **推荐的升级路径:**
   - v20 → v22/v23 (重大的 Module 系统变更)
   - 随后 v23 → v27/v28 (Theming 和 Angular/React 更新)
   - 随后 v28 → v29
   - 随后 v29 → v30
   - 最后升级到最新版本 (v35+)

2. **准备工作:**
   - 检查您当前的框架（React、Angular、Vue、原生 JS）及其与目标 AG Grid 版本的版本兼容性
   - 备份您的项目
   - 查看每个主版本的官方 Changelog：https://www.ag-grid.com/changelog/

3. **升级步骤 (常规):**

   - 更新 `package.json` 依赖项：
     - Community 版本：`"ag-grid-community": "^30.0.0"` (或最新版)
     - Enterprise 版本：`"ag-grid-enterprise": "^30.0.0"`
     - 框架封装库 (例如：`"ag-grid-angular": "^30.0.0"`, `"ag-grid-react": "^30.0.0"`)
   - 如果使用了 all-in-one 软件包，请移除旧的导入，如 `ag-grid` 或单个模块
   - 运行 `npm install` 或 `yarn install`
   - 修复 TypeScript 错误（如果需要，更新 `tsconfig`；v30+ 通常需要 TS 4.3+）
   - 更新 Grid 设置代码（例如：Module 注册、Theme 引入）

4. **常见错误及修复方法:**
   - **Module not found / 注册错误** —— 切换到 `import 'ag-grid-enterprise';` 或使用 `all-modules` 包。旧的全局注册方式已被移除。
   - **Theming 问题 (样式丢失/损坏)** —— 迁移到新的 CSS variable 主题（导入新的 Theme CSS，更新类名如 `ag-theme-alpine`）
   - **属性/方法未找到** —— 在 Changelog 中搜索已移除/弃用的条目；用新的等效项替换（例如：旧 API → 新 API）
   - **TypeScript 类型错误** —— 提供显式类型（例如：为 `columnDefs: ColDef[]` 指定类型）
   - **自定义 Cell renderers/editors 损坏** —— 检查 Params 是否发生变化；更新到新的接口
   - **框架相关问题** —— Angular：如果存在 `.withComponents()`，请将其移除（v28 之后）；React：检查 Functional component hooks

5. **辅助工具:**
   - AG Grid 从 v31+ 开始提供 **Codemods**（自动执行部分迁移）
   - 使用每个主版本的迁移指南（例如：upgrading-to-ag-grid-30）
   - 进行彻底测试 —— Excel 导出、Server-side model 和自定义组件等功能通常需要重点关注

**建议：** 逐步升级（一次升级一个或两个主版本），并对照每一步的官方迁移指南。如果代码库允许，可以先升级到最新的 v30.x 或直接升级到当前版本 (v35+)，但根据使用复杂度的不同，预计需要 1 到数个工作日的工作量。

**参考资料:**

- [Upgrading to AG Grid 30](https://www.ag-grid.com/javascript-data-grid/upgrading-to-ag-grid-30)
- [AG Grid Migration Guides Overview](https://www.ag-grid.com/javascript-data-grid/migration)
- [What's New in AG Grid 30](https://blog.ag-grid.com/whats-new-in-ag-grid-30/)
- [AG Grid Changelog](https://www.ag-grid.com/changelog)
