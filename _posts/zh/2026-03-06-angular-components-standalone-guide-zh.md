---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular 组件、模块与独立组件详解
translated: true
type: note
---

**问题：** 在 Angular 21 中，什么是 Components 和 Modules，“standalone” 是什么意思？

---

**答案：**

## 1. Angular 中的 Component 是什么？

**Component** 是 Angular 应用程序的基本构建块。它控制 UI 的一个部分（一个“视图”），并由三个部分组成：

- **TypeScript class** — 包含逻辑和数据
- **HTML template** — 定义渲染的内容
- **CSS styles** — 定义外观样式

每个 Angular 应用程序都是组件的树状结构。你可以使用 `@Component` 装饰器来定义一个：

```typescript
@Component({
  selector: 'app-hello',
  template: `<h1>Hello World</h1>`,
  standalone: true
})
export class HelloComponent {}
```

---

## 2. Angular 中的 Module (NgModule) 是什么？

**Module** (`NgModule`) 是传统的将相关 components、directives、pipes 和 services 分组和组织的方式。在 standalone components 出现之前，**每个 component 都必须在 NgModule 中声明** 才能使用。

```typescript
// 旧方式 — 基于 NgModule
@NgModule({
  declarations: [UserComponent],
  imports: [CommonModule],
  exports: [UserComponent]
})
export class UserModule {}
```

Angular 中的模块概念似乎多余，并且让初学者从零开始学习 Angular 变得更难 — 它是一个额外的概念，而且不清楚为什么需要它。

---

## 3. “Standalone” 是什么意思？

Standalone components 是自包含的 Angular components，不需要 NgModule 即可运行。在此功能之前，每个 component 都必须在 NgModule 中声明，这增加了复杂性和依赖性。

使用 standalone component 时，你可以将依赖项**直接在 component 本身中声明**，使用 `imports` 数组：

```typescript
// Angular 21 方式 — Standalone
@Component({
  selector: 'app-user',
  standalone: true,           // <-- 这使其成为 standalone
  imports: [CommonModule],    // <-- 依赖项放在这里
  template: `<h2>User Works!</h2>`
})
export class UserComponent {}
```

---

## 4. 时间线：Standalone 如何成为默认

| Angular 版本 | 发生了什么变化 |
|---|---|
| v14 | 将 standalone 引入为开发者预览 |
| v15–v18 | Standalone 稳定下来，被 Angular 团队推荐 |
| **v19** | 从 Angular v19 开始，components、directives 和 pipes **默认是 standalone**。 |
| **v21** | Angular 21 专注于 **standalone-first 架构**、简化、性能提升以及现代响应式模式。 |

---

## 5. 在 Angular 21 中：你还需要写 `standalone: true` 吗？

默认情况下，Angular components 是 standalone 的，这意味着你可以直接将它们添加到其他 components 的 `imports` 数组中。使用早期 Angular 版本创建的 components 可能在其 `@Component` 装饰器中指定 `standalone: false`。

因此在 Angular 21 中：
- 你 **不再需要写** `standalone: true` — 它是默认的
- 只有当你想要旧的 NgModule 行为时，才写 `standalone: false`
- NgModules **并未弃用**，但不再推荐用于新代码

---

## 6. Standalone 的优势（对比 NgModule）

Standalone components 通过消除 NgModule 样板代码、实现更清晰的依赖管理、通过更好的 tree-shaking 提升性能、简化项目结构，并提升模块化、可重用性和可测试性，从而彻底改变了开发工作流程。

总结：

| 特性 | NgModule（旧版） | Standalone（Angular 21） |
|---|---|---|
| 声明 component | 必须在 NgModule 中 | 不需要 |
| 导入依赖项 | 在模块中 | 直接在 component 中 |
| 懒加载 | 模块级别 | Component 级别（更简单） |
| 样板代码 | 高 | 最小 |
| 测试 | 需要模块设置 | 更简单，无需模块 |

---

## 参考资料

- [Angular Official Docs — Standalone Components](https://angular.dev/reference/migrations/standalone)
- [Angular Official Docs — Anatomy of Components](https://angular.dev/guide/components)
- [Angular Blog — The Future is Standalone](https://blog.angular.dev/the-future-is-standalone-475d7edbc706)
- [Angular 21 — What's New, What's Changed](https://dev.to/mridudixit15/angular-21-whats-new-whats-changed-3fl3)
- [GeeksforGeeks — Standalone Components in Angular](https://www.geeksforgeeks.org/angular-js/standalone-components-in-angular/)