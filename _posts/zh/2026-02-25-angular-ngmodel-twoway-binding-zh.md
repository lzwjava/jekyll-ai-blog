---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular ngModel 双向绑定指南
translated: true
type: note
---

**问题：** Angular 的 ngModel 如何工作？

**答案：**

`ngModel` 是来自 `@angular/forms` 的一个 **directive**，它在 HTML 表单控件（如 `<input>`、`<select>`、`<textarea>`）和 Angular 组件中的属性之间启用 **two-way data binding**。

它是 **template-driven forms** 中使用的关键机制。

### ngModel 的核心目的

- 自动创建和管理 `FormControl` 实例（幕后操作）
- 保持 **input value** ↔ **component property** 同步
- 提供内置的 **validation state** 跟踪（valid/invalid, touched/dirty, errors…）
- 将控件注册到父表单（如果在带有 `ngForm` 的 `<form>` 内）

### 最常见的语法（双向绑定 – “Banana in a Box”）

```html
<input [(ngModel)]="username" name="username" required>

<!-- 等效的展开形式 -->
<input [ngModel]="username" (ngModelChange)="username = $event" name="username">
```

- `[(ngModel)]` 是语法糖
- 左侧部分 → 属性绑定 (`[ngModel]`)
- 右侧部分 → 事件绑定 (`(ngModelChange)`)

### 内部工作原理（简化流程）

1. Angular 看到 `[(ngModel)]="username"`
2. `NgModel` directive 在 `<input>` 上激活
3. 它创建一个 `FormControl` 实例
4. 它从组件读取初始值（`username`）并设置到 input 上（model → view）
5. 它附加一个 **value accessor**（通常是 native input 的 `DefaultValueAccessor`）
6. 用户输入时 → 浏览器分发 `input` / `change` 事件
7. `NgModel` 捕获它 → 更新 `FormControl` 值
8. `FormControl` 发出值变化
9. `NgModel` 调用 setter → 更新组件属性（`username`）
10. 变更检测运行 → 如需要更新视图

### 重要要求

你 **必须** 导入 `FormsModule`：

```ts
// app.module.ts 或 standalone imports
import { FormsModule } from '@angular/forms';

@NgModule({
  imports: [
    FormsModule,
    // ...
  ]
})
```

或在 standalone 组件中：

```ts
@Component({
  standalone: true,
  imports: [FormsModule],
  // ...
})
```

### 单向绑定变体

```html
<!-- 仅 model → view -->
<input [ngModel]="username">

<!-- 仅 view → model（很少单独使用） -->
<input (ngModelChange)="username = $event">
```

### Template-driven 表单示例

```html
<form #f="ngForm" (ngSubmit)="onSubmit(f.value)">
  <input
    type="email"
    name="email"
    [(ngModel)]="user.email"
    required
    email
    #emailCtrl="ngModel">

  <div *ngIf="emailCtrl.invalid && emailCtrl.touched">
    请输一个有效的邮箱
  </div>

  <button type="submit" [disabled]="f.invalid">注册</button>
</form>
```

### 现代替代方案（Angular 17+）

- **Signal inputs + `model()`**（许多新组件中首选）

```ts
email = model<string>('');           // 双向
emailInput = model<string | null>(); // 可空双向
```

```html
<input [model]="emailInput()" />
```

- **Reactive Forms** (`FormControl`、`FormGroup`) — 通常推荐用于复杂表单

### 快速总结表格

| 语法                        | 方向               | 使用场景                              |
|-----------------------------|--------------------|---------------------------------------|
| `[(ngModel)]="prop"`        | 双向               | 经典 template-driven forms            |
| `[ngModel]="prop"`          | Model → View       | 仅显示或单向                          |
| `(ngModelChange)="…"`       | View → Model       | 自定义变更处理                        |
| `model()` + signal          | 双向（现代）       | 基于 Signal 的组件（17+）             |
| `formControlName`           | —                  | Reactive forms（无 `ngModel`）        |

`ngModel` 仍然被广泛使用，尤其是在简单表单和遗留代码中，但许多新 Angular 应用倾向于使用 **reactive forms** 或 **signal + model()** 以获得更好的类型安全性和可测试性。

**参考资料：**

- [NgModel - Official Angular Documentation](https://angular.dev/api/forms/NgModel)
- [Two-way binding syntax explanation](https://angular.dev/guide/templates/two-way-binding)
- [Template-driven forms guide](https://angular.dev/guide/forms)
