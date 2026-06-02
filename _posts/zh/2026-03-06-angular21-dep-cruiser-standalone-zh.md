---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular 21 独立模式的依赖巡航器
translated: true
type: note
---

**问题：** 在 Angular 项目中使用 dependency-cruiser 的更多细节。它支持 Angular 21 的 standalone components（module-less architecture）吗？

**回答：**

**Dependency-cruiser** 是 Angular 项目中依赖分析的绝佳选择——包括现代 Angular 版本（截至 2026 年的 Angular 21）——因为它在 **static source code level** 工作并理解 **TypeScript imports**。

### 相对于 Madge 等工具的关键优势

- 功能更强大的 **custom rules**（forbidden dependencies、layer violations、无循环、无 feature → core 导入等）
- 出色的 **circular dependency** 检测（显示完整的循环路径）
- 多种 **report formats**（err、json、html、dot/graphviz、svg、mermaid、d3、csv 等）
- CI 友好的 `--output-type err` + 违规时退出码 ≠ 0
- 非常好的 **TypeScript** 支持（包括 `tsconfig.json` 中的 path aliases）

### 它支持 Angular 21 + Standalone Components 吗？

**是的——它工作得非常完美。**

Angular 21（类似于 ~19 之后的版本）默认使用 **standalone: true** 并消除了大多数 NgModules。
Dependency-cruiser 不关心 Angular 的运行时模块系统或 `@Component({ standalone: true, imports: […] })`——它仅跟踪 TypeScript 文件中的 **static import / export graph**。

因此它能正确检测：

- 常规的 `import { Something } from './something.component';`
- Barrel re-exports（`export * from './comp';`）
- Path aliases（`@app/shared`、`@core` 等）
- Standalone components 之间的循环依赖（在递归树、对话框等中非常常见）

**关于 standalone components 中循环依赖的重要说明**

Angular 本身有时需要在 `imports: []` 数组中使用 `forwardRef(() => OtherComponent)` 来打破循环 *runtime* 引用。
**Dependency-cruiser 忽略 forwardRef**——它仍会看到静态的 `import` 语句并报告循环。

这在大多数团队中实际上是 **理想** 的行为：

- 即使 Angular 可以通过 `forwardRef` 技术处理，您通常仍想了解 **architectural cycles**
- 许多团队完全禁止循环（或许除了像递归组件这样的特定情况）

如果您想允许某些循环（例如，递归 UI 模式），可以编写规则来 **禁止大多数循环但允许特定文件夹或命名例外**。

### Angular 21 项目的推荐设置

```bash
# 安装
npm install --save-dev dependency-cruiser

# 创建默认配置（非常好的起点）
npx depcruise --init
```

这会创建 `.dependency-cruiser.js`——编辑它以添加 Angular 友好的规则：

```javascript
// .dependency-cruiser.js（示例片段）
module.exports = {
  forbidden: [
    // 经典：完全不允许循环依赖
    {
      name: "no-circular",
      comment: "Don't allow circular dependencies",
      severity: "error",
      from: {},
      to: {
        circular: true
      }
    },

    // 可选：feature components 不导入 core/domain
    {
      name: "no-feature-to-core",
      comment: "Features shouldn't import core/domain logic",
      severity: "warn",
      from: { path: "^src/app/features" },
      to:   { path: "^src/app/core|^src/app/domain" }
    },

    // 可选：强制执行 clean architecture 层
    {
      name: "no-presentation-to-infrastructure",
      severity: "error",
      from: { path: "^src/app/(components|pages|features)" },
      to:   { path: "^src/app/infrastructure" }
    }
  ],

  options: {
    // 对 Angular path aliases 很重要
    doNotFollow: {
      path: "node_modules"
    },

    tsPreCompilationDeps: true,          // 理解 type-only imports
    tsConfig: { fileName: "tsconfig.json" }, // 读取 paths/aliases

    // CI 中更美观的输出
    reporterOptions: {
      dot: { collapsePattern: "^src/app/[^/]+" }
    }
  }
};
```

运行它：

```bash
# 快速检查（违规时失败 CI）
npx depcruise src --validate

# 仅循环，紧凑输出
npx depcruise src --include-only "^src" --output-type err --ruleset .dependency-cruiser.js

# 精美的交互式图表（在浏览器中打开）
npx depcruise src --output-type d3 --output-to dependency-graph.html

# CI 示例（违规时退出 ≠0）
npx depcruise src --validate || exit 1
```

许多大型 Angular monorepos（Nx、自定义设置）在 CI 中成功使用 dependency-cruiser 来强制执行“no circular dependencies”和分层架构——即使是 100% standalone components。

**参考资料：**

- [dependency-cruiser GitHub](https://github.com/sverweij/dependency-cruiser)
- [dependency-cruiser rules reference](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md)
- [dependency-cruiser npm page](https://www.npmjs.com/package/dependency-cruiser)
