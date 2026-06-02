---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快速调试 Angular 循环依赖
translated: true
type: note
---

**问题：** 如何在 Angular 21 中找出哪个组件或模块存在导入或 standalone 组件的循环问题？

**答案：**

在 Angular 21（以及自 ~v14–v17 的 Ivy + standalone 推动以来），循环导入通常会导致：

- build-time stack overflow in `@ngtools/webpack` / esbuild
- NG0919: Circular Dependency Detected
- NG0200: Circular Dependency in DI
- ReferenceError / Cannot access before initialization（尤其是使用 standalone 时）

以下是在 2026 年 Angular 项目中定位确切导致循环依赖的文件的最有效方法。

### 1. 使用 `madge` – 仍是 #1 推荐工具（官方 Angular 文档建议使用它）

```bash
# Install once (recommended as dev dep)
npm install --save-dev madge

# Quick check
npx madge --circular --extensions ts src/

# More precise (start from entry point)
npx madge --circular src/main.ts

# Show warning level too (barrels, side-effects, etc.)
npx madge --circular --warning src/

# Generate visual graph (very helpful!)
npx madge --circular --extensions ts --image deps.svg src/
# then open deps.svg in browser
```

- 输出示例：
  ```
  ✖ Found 3 circular dependencies!
  1) src/app/featureA.component.ts → src/app/shared/utils.service.ts → src/app/featureA.component.ts
  2) src/app/dashboard/dashboard.component.ts → src/app/core/auth.service.ts → src/app/dashboard/data.service.ts → src/app/dashboard/dashboard.component.ts
  ```

### 2. 使用 `dependency-cruiser`（更强大的规则和报告功能）

```bash
npm install --save-dev dependency-cruiser

# Initialize default config
npx depcruise --init

# Run (detects circular by default)
npx depcruise src --validate .dependency-cruiser.js

# Or focused on circular only
npx depcruise src --include-only "^src" --output-type err --ruleset .dependency-cruiser.js
```

许多团队在大型 monorepo 中更喜欢它而不是 madge，因为可以在 CI 中强制执行“无循环依赖”。

### 3. Angular CLI + build flags（快速缩小范围）

```bash
# Very verbose output → often shows file just before crash
ng build --verbose

# Or with higher stack trace
NODE_OPTIONS="--stack-trace-limit=400" ng build --verbose

# Disable incremental → sometimes reveals clearer file name
ng build --no-progress --aot
```

### 4. Standalone 特有的循环依赖（在 Angular 17–21 中非常常见）

典型模式：递归 / 父 ↔ 子 standalone 组件

```ts
// parent.component.ts
imports: [ChildComponent]

// child.component.ts
imports: [ParentComponent]   ← direct cycle
```

使用 `forwardRef` 修复模式：

```ts
// child.component.ts
import { forwardRef } from '@angular/core';
imports: [forwardRef(() => ParentComponent)]
```

但要**找出**它们：

- madge 仍然能捕获它们（它遵循 ES imports）
- 临时注释 `app.config.ts` / root bootstrap 中的 imports → 逐个添加回来
- 搜索代码库中的互导：

  ```bash
  # rough grep (adjust paths)
  grep -r "imports.*Component" src/app | grep -B1 -A1 "Component"
  ```

### 快速行动检查清单（2026 最佳实践）

1. `npx madge --circular --extensions ts src/ > circular.txt`
2. 打开 `circular.txt` — 先修复最短的循环
3. 常见罪魁祸首：
   - Barrel 文件（`index.ts` 重新导出模块/组件）
   - Shared utils/service 被 feature 反向导入
   - 未使用 `forwardRef` 的递归 standalone 组件
   - 旧 NgModule → standalone 迁移遗留问题
4. 修复后 → 运行 `ng build --prod` 确认
5. 添加到 `package.json` scripts：

   ```json
   "check-circular": "madge --circular --extensions ts src/"
   ```

   → 在提交前 / CI 中运行

即使在 Angular 21 中，madge 仍是 Angular 社区最快且最推荐的工具。

**参考：**

- https://angular.dev/errors/NG0919
- https://medium.com/@vkrntteotia/how-to-automatically-detect-circular-dependencies-in-your-angular-project-using-a-tool-called-madge-9c2f8ab77b4f
- https://timdeschryver.dev/blog/fixing-angular-standalone-components-that-have-a-circular-dependency
- https://www.npmjs.com/package/madge
- https://github.com/sverweij/dependency-cruiser
