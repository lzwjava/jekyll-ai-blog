---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 详解 Angular 独立组件
translated: true
type: note
---

**Question: 如何理解 Angular 中的 standalone components？**

**Answer:**

Standalone components 是现代 Angular 中最重要的变化之一（在 Angular 14 作为开发者预览版引入，在 Angular 15 达到生产可用状态，并从 Angular 16+ 开始成为推荐的默认组件编写方式）。

### “Standalone” 的实际含义

一个 **standalone component** 是指：

- **不**属于任何 NgModule
- 直接声明其自身的 **dependencies**（其他 components、directives、pipes、services…）
- 可以**直接**用于 routing、在另一个 component 的 template 中使用，或作为入口点

简而言之：它在大多数情况下消除了对经典 NgModule 样板代码的需求。

### 经典（基于 NgModule）的方式 – standalone 之前

```ts
// classic.component.ts
@Component({
  selector: 'app-classic',
  template: `<h1>Hello</h1>`,
  standalone: false   // ← 默认值 / 不需要
})
export class ClassicComponent {}

// 你必须在一个 module 中声明它
@NgModule({
  declarations: [ClassicComponent],
  imports: [CommonModule, FormsModule],
  exports: [ClassicComponent]
})
export class SomeModule {}
```

### Standalone 方式 – 现代 Angular (2023–2026 风格)

```ts
// modern.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { HighlightDirective } from './highlight.directive';

@Component({
  selector: 'app-modern',
  standalone: true,                           // ← 这是关键行
  imports: [                                  // ← 列出此组件需要的所有内容
    CommonModule,
    FormsModule,
    MatButtonModule,
    HighlightDirective,                       // ← 可以导入其他 standalone components/directives
    // 如果需要，也可以导入整个 NgModules（过渡期）
  ],
  template: `
    <h1>Hello from standalone!</h1>
    <input type="text" [(ngModel)]="name">
    <button mat-button>Click</button>
  `
})
export class ModernComponent {
  name = 'Angular';
}
```

### 如何使用 Standalone Components（无需 NgModule）

1. **在 router 中**（目前最常见的用例）

```ts
const routes: Routes = [
  { path: 'home', component: HomeComponent },           // ← standalone component
  { path: 'profile', component: ProfileComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' }
];
```

2. **在另一个组件的 template 内部**

```html
<!-- parent.component.html -->
<app-modern></app-modern>
<app-user-card [user]="currentUser"></app-user-card>
```

3. **作为根组件** (bootstrapApplication)

```ts
// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { AppComponent } from './app.component';
import { routes } from './app.routes';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes)
  ]
});
```

### 快速对比表 – NgModule vs Standalone

| 特性 | 基于 NgModule (经典) | Standalone (现代) |
| :--- | :--- | :--- |
| 需要 NgModule 吗？ | 是，始终需要 | 否 |
| 在哪里列出 imports？ | 在 NgModule 中 | 直接在 `@Component({ imports: […] })` 中 |
| 可重用性 | 需要从 module 中 export | 可以直接在任何地方 import |
| 样板代码 | 多 (module + declarations + exports) | 非常少 |
| Tree-shaking | 较差 | 更好（尤其是配合 lazy-loading） |
| 学习曲线 (新开发者) | 陡峭（因为有 modules） | 容易得多 – 感觉像 React/Vue/Solid |
| 2025–2026 年推荐？ | 仅针对遗留系统或超大型 monorepos | 是 – 新项目的默认选择 |

### 心智模型 – 像这样理解 Standalone

> 一个 standalone component 就像一个小型、自包含的微型应用：
>
> - 它声明：“我需要这些部分才能工作”
> - Angular 的 compiler 正好打包这些部分
> - 不再需要中央“模块注册表”

这非常接近 React、Vue、Svelte 等组件的工作方式。

### 实践中开始理解的最佳方式 (2026)

1. 创建一个使用 standalone 的新项目（自 Angular 17 起为默认设置）：

```bash
ng new my-app --standalone
```

2. 将组件生成为 standalone（现在的默认行为）：

```bash
ng g component user-card    # → 自动创建 standalone: true
```

3. 观察生成的代码 → 你几乎再也看不到 `declarations: []` 或 NgModules 了。

这是“感受” standalone 含义的最快方法。

Standalone 不仅仅是一种语法——它是 Angular 向更简单、更现代的组件模型的转变，该模型去除了大部分模块仪式感，同时保留了所有强大功能（dependency injection、lazy-loading 等）。

**References:**

- <https://angular.dev/guide/standalone-components>
- <https://blog.angular.dev/introducing-standalone-components-58a418173aa3>
- <https://blog.angular.dev/angular-v17-is-now-available-8c4c0d8d3169>
- <https://angular.love/standalone-components-in-angular>
