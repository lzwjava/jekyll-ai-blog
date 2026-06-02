---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular 21 修复分页更新问题
translated: true
type: note
---

Question: 在 Angular 21 中，worklist（父组件）更新 pagination（子组件）中的数据，但 pagination 的 total items 和其他 UI 不会视觉更新，直到用户点击它——如何修复这个 change detection timing 问题？

Answer:

## 根本原因

Angular v21 的 zoneless change detection 移除了 Zone.js，需要手动或基于 signal 的触发 change detection。Angular 不再自动运行全局检查——UI 仅在明确提示时更新。这就是为什么 Angular 14 感觉更宽容：Zone.js 会捕获几乎任何 async 更新并为整个树重新运行 change detection。在 Angular 21 的更严格调度中，OnPush 组件仅在 input 引用变化、该组件中的事件、`async` pipe 发出值以及 signal 写入时检查。您的 pagination 组件只是闲置，直到您点击它（这会触发 DOM 事件，引发其自身检查）。

---

## 修复选项（最佳到备选）

### ✅ 选项 1 — 使用 Angular Signals（推荐 / 现代方式）

这是最干净的修复。将共享状态（total items、current page 等）转换为 signals。

**在共享服务中（例如 `worklist.service.ts`）：**

```typescript
import { signal, computed } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class WorklistService {
  totalItems = signal<number>(0);
  currentPage = signal<number>(1);
  pageSize = signal<number>(10);
}
```

**在 worklist（父组件）中：**

```typescript
constructor(private worklistService: WorklistService) {}

loadData() {
  this.apiService.getItems().subscribe(result => {
    this.worklistService.totalItems.set(result.total); // signal write
  });
}
```

**在 pagination（子组件）模板中：**
{% raw %}

```html
<p>Total: {{ worklistService.totalItems() }}</p>
```

{% endraw %}

在模板中读取 signal 会将其链接到视图；写入该 signal 会调度正确的视图更新——这使 change detection 更具针对性，并与 OnPush 或甚至 zoneless 自然搭配。

---

### ✅ 选项 2 — 使用 `input()` Signal API（Angular 17+）

用新的基于 signal 的 `input()` 函数替换 `@Input()`，在 pagination 组件上：

```typescript
// pagination.component.ts
import { input } from '@angular/core';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  ...
})
export class PaginationComponent {
  totalItems = input<number>(0);  // signal input
  pageSize = input<number>(10);
}
```

**父组件正常传递：**

```html
<app-pagination [totalItems]="total" [pageSize]="pageSize" />
```

您可以使用 `input()` 或 `output()` signal API 代替 `@Input()` 或 `@Output()`，从而消除手动触发 change detection 的需要。

---

### ✅ 选项 3 — 使用 `Observable` + `async` Pipe

如果您更喜欢 RxJS，在服务中使用 observable，并在模板中通过 `async` pipe 订阅。

**服务：**

```typescript
private totalItemsSubject = new BehaviorSubject<number>(0);
totalItems$ = this.totalItemsSubject.asObservable();

updateTotal(n: number) { this.totalItemsSubject.next(n); }
```

**Pagination 模板：**
{% raw %}

```html
<p>Total: {{ worklistService.totalItems$ | async }}</p>
```

{% endraw %}

`AsyncPipe` 在新值到达时自动调用 `markForCheck`，因此 Angular 知道要重新检查该组件。

---

### ⚠️ 选项 4 — 手动 `markForCheck()`（备选 / 遗留方式）

当您还无法重构为 signals 或 observables 时使用此方法：

```typescript
// pagination.component.ts
constructor(private cdr: ChangeDetectorRef) {}

ngOnChanges() {
  this.cdr.markForCheck(); // 告诉 Angular：重新检查此组件
}
```

或在从父组件接收数据后直接调用：

```typescript
updatePagination(total: number) {
  this.totalItems = total;
  this.cdr.markForCheck();
}
```

组件可以使用 Default 策略，只要它们在 change detection 需要运行时通知 Angular（调用 `markForCheck`、使用 signals、`AsyncPipe` 等）。

---

## 总结表格

| 方法 | Angular 21 友好 | 复杂度 |
|---|---|---|
| Signals (`signal()`、`input()`) | ✅ 最佳 | 低–中 |
| Observable + `async` pipe | ✅ 良好 | 低 |
| 手动 `markForCheck()` | ⚠️ 有效但遗留 | 低 |
| 直接修改 `@Input()` 对象 | ❌ 失效 | — |

关键原则：如果您通过 `@Input()` 传递对象和数组，并在父组件中更改数据，change detection 不会发生——对象数据会被更改，但检测不会触发。始终传递新对象引用，或使用 signals/observables 来保证子组件重新渲染。

References:

- [Angular Zoneless Guide](https://angular.dev/guide/zoneless)
- [Zoneless Change Detection in Angular v21](https://www.zignuts.com/question-and-answer/how-does-zoneless-change-detection-work-in-angular-v21)
- [Change Detection Strategies: Zones and Signals](https://blog.lunatech.com/posts/2025-11-05-change-detection-strategies-in-angular-zones-and-signals)
- [Angular OnPush Change Detection – Avoid Common Pitfalls](https://blog.angular-university.io/onpush-change-detection-how-it-works/)
- [Angular Change Detection with Zoneless – DEV Community](https://dev.to/soumayaerradi/angular-change-detection-with-zoneless-413f)
