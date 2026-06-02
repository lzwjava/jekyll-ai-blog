---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Angular 无限递归错误
translated: true
type: note
---

**问题：** 为什么在从 Angular 14 迁移到 Angular 21 时，main.ts 和 polyfills.ts 的模块构建会在 @ngtools/webpack/src/ivy/index.js 中失败，报错 "Error: Maximum call stack size exceeded"，如何修复？

**回答：**

这个错误几乎总是表示 **Angular compiler (via Ivy in @ngtools/webpack)** 在分析或元数据处理阶段进入了无限递归 / 循环。

它会在非常早的阶段出现——通常在 **main.ts** 和 **polyfills.ts** 上——因为这些入口文件会拉入整个应用图谱，而编译器在尝试处理循环或深度递归导入时崩溃。

### 大型迁移（14 → 17/18/19/20/21）期间最常见原因

- 循环导入 / 循环模块依赖（在主要版本跳跃后非常常见）
- 一个模块意外导入了**自身**（直接或通过 barrel files 间接）
- 非常旧的 barrel files（`index.ts` 重新导出一切），在更严格的 Ivy / esbuild-based 编译规则下创建巨大的导入循环
- 不正确的懒加载设置或形成循环的 NgModule 导入
- 非常罕见：极深的组件嵌套 / 递归模板（但这通常在运行时崩溃，而不是构建时）
- 第三方库带有损坏的元数据 / 非常旧的代码，新编译器无法处理

### 如何修复（逐步指南）

1. **首先清理一切**（消除许多假阳性）

   ```bash
   rm -rf node_modules
   rm -rf dist
   npm cache clean --force
   npm install
   ```

2. **查找循环依赖**

   安装一个有用的工具：

   ```bash
   npm install -g madge
   ```

   然后运行（如果需要调整入口点）：

   ```bash
   madge --circular --extensions ts src/
   madge --circular src/main.ts
   ```

   修复每个报告的循环——这能解决 ~70–80% 的此类错误。

3. **检查自导入模块**

   在代码库中搜索类似模式：

   ```ts
   // in src/app/feature/feature.module.ts
   import { FeatureModule } from './feature.module';
   ```

   或 barrel files 这样做的：

   ```ts
   // src/app/shared/index.ts
   export * from './shared.module';
   ```

   → 删除或重构此类 barrel files。

4. **尝试关闭增量编译**（有时有助于识别真正的问题文件）

   ```bash
   ng build --no-progress --verbose
   ```

   或临时添加到 angular.json：

   ```json
   "architect": {
     "build": {
       "options": {
         "progress": false
       }
     }
   }
   ```

5. **如果可能，逐步迁移**

   直接从 14 跳到 21 非常激进（15、16、17 有许多破坏性变更——standalone components、esbuild、新的控制流等）。

   推荐路径：

   14 → 15 → 16 → 17 → 18 → 19 → 20 → 21

   每次使用官方更新指南：

   <https://update.angular.dev/>

   在每个步骤运行 `ng update @angular/cli@next @angular/core@next`，并一次修复一个版本。

6. **快速变通方法来缩小问题范围**（非永久修复）

   - 临时在 **app.module.ts** 中注释掉几乎所有导入 → 查看是否能构建
   - 转换为 **standalone bootstrap**（Angular 17+）——移除 NgModule 图谱复杂性

     ```ts
     // main.ts
     import { bootstrapApplication } from '@angular/platform-browser';
     import { AppComponent } from './app/app.component';
     bootstrapApplication(AppComponent);
     ```

   - 从 AppModule 中逐个移除第三方模块

7. **如果已在 Angular 17+ 且仍看到 @ngtools/webpack**

   在现代 Angular 版本中应该看到 **esbuild** 而非此。

   强制使用现代 builder：

   ```bash
   ng build --esbuild
   ```

   或更新 angular.json 以使用 `@angular-devkit/build-angular:application`（v17+ 新增）。

### 总结 – 快速行动计划

- 运行 **madge** → 修复所有循环依赖
- 删除 / 重构不良 barrel files
- 逐版本迁移（不要直接从 14 → 21 跳跃）
- 清理 node_modules 并重新安装
- 如果卡住 → 创建最小复现 → 在 GitHub / Stack Overflow 上分享

这个错误**几乎从来不是 Angular 的 bug**——是您的项目导入图谱不再被更严格/更快的编译器容忍。

**参考：**

- <https://stackoverflow.com/questions/73197135/angular-14-ng-serve-error-ngtools-webpack-src-ivy-index-js-error-maximum>
- <https://github.com/angular/angular-cli/issues/26969>
- <https://github.com/angular/angular-cli/issues/23597>
- <https://github.com/angular/angular-cli/issues/23814>
