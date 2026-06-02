---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular 独立迁移指南
translated: true
type: note
---

问题：如何将基于 NgModule 的 Angular 应用程序迁移到 standalone components？

回答：

## 概述

有两种方法：使用 Angular 内置 schematic 的**自动迁移**（推荐），以及**手动迁移**逐个组件进行。下面将介绍两种方法。

---

## 方法 1：自动迁移（推荐）

迁移过程分为三个步骤。您必须多次运行它，并在每个步骤后手动检查项目是否能构建并按预期运行。

### 先决条件

您的项目必须：

- 使用 **Angular 15.2.0 或更高版本**
- 无任何编译错误地构建
- 处于**干净的 Git 分支**，所有工作已保存

### 步骤 1 — 将所有 components、directives 和 pipes 转换为 standalone

```bash
ng g @angular/core:standalone
# 选择："Convert all components, directives and pipes to standalone"
```

这会自动为每个 component、directive 和 pipe 添加 `standalone: true`，并将它们的依赖移动到 `imports` 数组中。

**Before:**

```typescript
@Component({
  selector: 'app-example',
  templateUrl: './example.component.html',
  styleUrls: ['./example.component.css']
})
export class ExampleComponent {}
```

**After:**

```typescript
@Component({
  selector: 'app-example',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './example.component.html',
  styleUrls: ['./example.component.css']
})
export class ExampleComponent {}
```

✅ 验证应用仍能构建和运行，然后提交。

---

### 步骤 2 — 删除不必要的 NgModule 类

```bash
ng g @angular/core:standalone
# 选择："Remove unnecessary NgModule classes"
```

这会删除 NgModule 实例，将 components 标记为 standalone，并将现在独立的 components 移动到使用它们的其他 standalone components 的直接 imports 中。

> ⚠️ 注意：某些模块，特别是 `SharedModule`，在 schematic 执行后可能仍然存在，因为 schematic 无法判断移除它们是否安全。您可能需要手动删除这些模块。

✅ 验证应用仍能构建和运行，然后提交。

---

### 步骤 3 — 使用 standalone APIs 进行 bootstrap

```bash
ng g @angular/core:standalone
# 选择："Bootstrap the project using standalone APIs"
```

此步骤将 `bootstrapModule` 的任何用法转换为新的基于 standalone 的 `bootstrapApplication`。它还会从根 component 中删除 `standalone: false`，并删除根 NgModule。如果根模块有任何 providers 或 imports，迁移会尝试将尽可能多的配置复制到新的 bootstrap 调用中。

您的 `main.ts` 将从以下内容更改：

```typescript
// OLD — NgModule bootstrap
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule);
```

更改为：

```typescript
// NEW — Standalone bootstrap
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig);
```

✅ 验证应用，运行 lint + format 检查，然后提交。

---

## 方法 2：手动迁移（逐步进行）

如果您更喜欢逐步迁移，以下是手动为每个 component 进行迁移的方法：

### 1. 添加 `standalone: true` 并将 imports 移动到 component

```typescript
// BEFORE — component declared in a module
@Component({
  selector: 'app-user',
  templateUrl: './user.component.html'
})
export class UserComponent {}

// user.module.ts
@NgModule({
  declarations: [UserComponent],
  imports: [CommonModule, FormsModule]
})
export class UserModule {}
```

```typescript
// AFTER — standalone component
@Component({
  selector: 'app-user',
  standalone: true,
  imports: [CommonModule, FormsModule],  // moved here
  templateUrl: './user.component.html'
})
export class UserComponent {}
```

### 2. 修复服务注入

在 services 中使用 `providedIn: 'root'` 选项以确保它们全局可用。对于特定功能的 services，使用 `providers` 数组在 component 级别提供它们。

```typescript
@Injectable({
  providedIn: 'root'  // globally available, no module needed
})
export class UserService {
  getData() { return 'data'; }
}
```

### 3. 修复懒加载 — 使用 `loadComponent` 而非 `loadChildren`

```typescript
// OLD — lazy loaded module
{
  path: 'shop',
  loadChildren: () => import('./shop/shop.module').then(m => m.ShopModule)
}

// NEW — lazy loaded standalone component
{
  path: 'shop',
  loadComponent: () => import('./shop/shop.component').then(m => m.ShopComponent)
}
```

### 4. 在 `app.config.ts` 中替换 `RouterModule.forRoot()` 和 `HttpClientModule`

```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient()
  ]
};
```

---

## 关键变更总结

| 旧 NgModule 方式 | 新 Standalone 方式 |
|---|---|
| 模块中的 `declarations: [XComponent]` | component 中的 `standalone: true` |
| 模块中的 `imports: [X]` | component 中的 `imports: [X]` |
| `bootstrapModule(AppModule)` | `bootstrapApplication(AppComponent, appConfig)` |
| `RouterModule.forRoot(routes)` | `provideRouter(routes)` |
| `HttpClientModule` | `provideHttpClient()` |
| 懒加载的 `loadChildren` | 懒加载的 `loadComponent` |

---

## 迁移后 — 可选强制执行

考虑在 `tsconfig.json` 中添加 `strictStandalone` 选项，以强制未来仅编写 standalone components。

```json
// tsconfig.json
{
  "angularCompilerOptions": {
    "strictStandalone": true
  }
}
```

---

参考资料：

- [Angular Official Docs — Migrate to Standalone](https://angular.dev/reference/migrations/standalone)
- [Migrating a Large Angular App to Standalone — AngularSpace](https://www.angularspace.com/migrating-a-large-angular-application-to-standalone/)
- [Migrating a Modular Angular App to Standalone — Medium](https://medium.com/@sehban.alam/migrating-a-modular-angular-app-to-standalone-components-a-comprehensive-guide-4cbed7482731)
- [Angular Standalone Migration Schematic README — GitHub](https://github.com/angular/angular/blob/main/packages/core/schematics/ng-generate/standalone-migration/README.md)
