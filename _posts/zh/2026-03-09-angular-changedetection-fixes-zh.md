---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular 变更检测修复指南
translated: true
type: note
---

问题：在 Angular（现代版本，具有更严格的变更检测）中，worklist 组件向 pagination 子组件更新数据，但 pagination UI（例如 `totalItems`）仅在使用户实际点击 pagination 组件后才渲染/更新。您如何修复此时序/变更检测问题？

答案：

## 根本原因

这是一个典型的 **change detection timing problem**。当父组件（worklist）向 pagination 子组件设置数据时：

- 数据以 **超出 Angular 正常变更检测流程** 的方式到达（例如，来自异步调用、setTimeout 或当前 CD 周期后运行的事件）
- pagination 子组件使用 `OnPush` 或依赖 `@Input()` 引用检查，因此它会等待*下一个* CD 周期
- 用户点击恰好*偶然触发* CD，这就是为什么点击能“修复”它——点击事件强制 Angular 运行变更检测

---

## 修复策略：选择正确的方法

### ✅ 选项 1 — 使用 Angular Signals（推荐用于 Angular 17+/21）

这是**现代、惯用的修复方法**。Signals 本质上是响应式的，完全绕过了生命周期时序问题。

**在 worklist（父组件）中：**
```typescript
import { signal, computed } from '@angular/core';

export class WorklistComponent {
  totalItems = signal(0);
  items = signal<MyItem[]>([]);

  loadData() {
    this.myService.getItems().subscribe(result => {
      this.items.set(result.data);
      this.totalItems.set(result.total);  // signal 更新是即时的 + 响应式的
    });
  }
}
```

**在 pagination 子组件中：**
```typescript
import { input } from '@angular/core'; // Angular 17+ input signal

export class PaginationComponent {
  totalItems = input.required<number>();  // 响应式 signal 输入
}
```

**模板（父组件）：**
```html
<app-pagination [totalItems]="totalItems()" />
```

使用 `OnPush` 策略时，Angular 仅在传递新的 `@Input()` 值引用时才触发变更检测——但使用 Signals 时，更新会被响应式跟踪，并自动调度重新渲染，而无需等待下一个 CD 周期。

---

### ✅ 选项 2 — 在子组件中使用 `ChangeDetectorRef.detectChanges()`

如果无法重构为 Signals，请将 `ChangeDetectorRef` 注入到 **pagination 组件** 中，并在接收输入时调用 `detectChanges()`。

**在 pagination 组件中：**
```typescript
import { Component, Input, OnChanges, SimpleChanges, ChangeDetectorRef } from '@angular/core';

export class PaginationComponent implements OnChanges {
  @Input() totalItems = 0;
  
  constructor(private cdr: ChangeDetectorRef) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['totalItems']) {
      this.cdr.detectChanges(); // 强制当前组件 + 子组件立即重新渲染
    }
  }
}
```

`ChangeDetectorRef.detectChanges()` 强制当前视图及其子视图进行变更检测，从而解决父组件异步操作完成但子视图尚未更新的问题。

---

### ✅ 选项 3 — 在设置数据后在父组件中使用 `markForCheck()`

如果 **worklist** 控制变更，请在更新后标记视图：

```typescript
import { ChangeDetectorRef } from '@angular/core';

export class WorklistComponent {
  @ViewChild(PaginationComponent) pagination!: PaginationComponent;

  constructor(private cdr: ChangeDetectorRef) {}

  loadData() {
    this.myService.getItems().subscribe(result => {
      this.totalItems = result.total;
      this.cdr.markForCheck(); // 调度 OnPush 树进行检查
    });
  }
}
```

`markForCheck()` 不会立即触发变更检测，但会标记所有 `OnPush` 祖先组件需要在当前或下一个变更检测周期中被检查。

---

### ✅ 选项 4 — 使用共享的响应式服务（BehaviorSubject / Observable）

使用**共享服务**，使 pagination 组件可以独立订阅并响应，而不依赖 `@Input()` 时序。

```typescript
// pagination-state.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PaginationStateService {
  private totalItems$ = new BehaviorSubject<number>(0);
  totalItems = this.totalItems$.asObservable();

  setTotalItems(total: number) {
    this.totalItems$.next(total);
  }
}
```

{% raw %}
```typescript
// worklist.component.ts
this.paginationState.setTotalItems(result.total);

// pagination.component.ts
totalItems$ = this.paginationState.totalItems;
// template: {{ totalItems$ | async }}
```
{% endraw %}

使用带有 observables 的共享服务特别适用于深度嵌套组件，避免通过 `@Input`/`@Output` 链在组件树中上下冒泡数据和事件。

---

## 总结 — 选择哪个选项？




| 情况 | 最佳修复 |
|---|---|
| Angular 17+ / 21 现代项目 | **Signals + `input()`** |
| 现有的 `@Input()` 模式，无法重构 | **子组件中的 `ChangeDetectorRef.detectChanges()`** |
| 父组件控制更新 | **父组件中的 `markForCheck()`** |
| 深度嵌套或共享状态 | **共享 BehaviorSubject 服务** |

核心原则：**切勿依赖用户交互来偶然触发变更检测**。要么使用响应式原语（Signals、Observables），要么在异步数据到达后显式调度 CD 检查。

参考资料：

- [Angular OnPush Change Detection Pitfalls](https://blog.angular-university.io/onpush-change-detection-how-it-works/)
- [The Last Guide For Angular Change Detection](https://mokkapps.de/blog/the-last-guide-for-angular-change-detection-you-will-ever-need)
- [Angular Parent-Child ChangeDetectorRef Fix](https://www.w3tutorials.net/blog/call-child-component-method-from-parent-class-angular/)
- [NgRx SignalStore Pagination Example](https://ngrx.io/guide/signals/signal-store)