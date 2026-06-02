---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 NgBootstrap 20 分页导入
translated: true
type: note
---

**问题：** 如何修复在使用 ng-bootstrap 20 与 Angular 21 一起时出现的 “cannot find module '@ng-bootstrap/ng-bootstrap/pagination' or its corresponding type declarations” 问题？

**答案：**

这个错误通常是因为 **ng-bootstrap v20** 引入了 **component entry points**（一种导入单个组件的新方式），而许多代码库仍然使用旧的导入风格或错误地混合两种方式。

在 **ng-bootstrap v19 及更早版本**中，人们通常这样导入：

```ts
import { NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';
```

或者直接：

```ts
import { NgbPagination } from '@ng-bootstrap/ng-bootstrap';
```

从 **ng-bootstrap v20**（支持 Angular 21）开始，该库添加了 **secondary entry points**，以实现更好的 tree-shaking 和更快的构建。对于 standalone components（Angular 17+ 推荐）的正确现代导入风格是：

```ts
import { NgbPagination } from '@ng-bootstrap/ng-bootstrap/pagination';
```

### 如何修复

1. **更改分页相关组件的导入**：

   将以下替换：

   ```ts
   import { NgbPagination } from '@ng-bootstrap/ng-bootstrap';
   // 或
   import { NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';
   ```

   替换为：

   ```ts
   import {
     NgbPagination,
     NgbPaginationEllipsis,
     NgbPaginationFirst,
     NgbPaginationLast,
     NgbPaginationNext,
     NgbPaginationNumber,
     NgbPaginationPrevious,
     NgbPaginationPages
   } from '@ng-bootstrap/ng-bootstrap/pagination';
   ```

2. **更新您的组件 / standalone imports 数组**（Angular 17+ 中最常见的情况）：

   ```ts
   @Component({
     standalone: true,
     imports: [
       NgbPagination,           // ← 只添加您实际使用的组件
       // NgbPaginationFirst,
       // NgbPaginationNext,
       // 等。
     ],
     template: `
       <ngb-pagination
         [collectionSize]="totalItems"
         [(page)]="currentPage"
         [pageSize]="pageSize">
       </ngb-pagination>
     `
   })
   export class PaginationExampleComponent {
     // ...
   }
   ```

3. **如果您仍然使用基于 NgModule 的架构**（在 2025–2026 年较少见）：

   您可以继续导入完整模块：

   ```ts
   import { NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';
   ```

   ```ts
   @NgModule({
     imports: [NgbPaginationModule, /* ... */],
     // ...
   })
   export class FeatureModule {}
   ```

   但现在 **推荐** 的方式是 standalone + secondary entry points。

### 快速兼容性检查

- `@ng-bootstrap/ng-bootstrap@20.x` → 专为 **Angular ^21.0.0** 设计
- 确保您的 `package.json` 中有：

  ```json
  "@ng-bootstrap/ng-bootstrap": "^20.0.0",
  "@angular/core": "^21.0.0"
  ```

- 在更改版本/导入后，再次运行 `npm install` 或 `pnpm install`。

### 总结 – 最可能的修复方法（选择一种）

- 使用 `from '@ng-bootstrap/ng-bootstrap'` 的旧代码 → 更改为 `from '@ng-bootstrap/ng-bootstrap/pagination'`
- 使用完整的 `NgbModule` 导入 → 替换为单个 standalone 导入（最佳实践）
- 路径拼写错误或混合两种风格 → 标准化为 secondary entry points

应用正确的导入路径后，如果错误仍然存在，请清理缓存（`npm cache clean --force`），删除 `node_modules`，并重新安装依赖。

**参考资料：**

- [https://ng-bootstrap.github.io/#/getting-started](https://ng-bootstrap.github.io/#/getting-started)
- [https://github.com/ng-bootstrap/ng-bootstrap/releases](https://github.com/ng-bootstrap/ng-bootstrap/releases)
- [https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md](https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md)
- [https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap](https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap)
