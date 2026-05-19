---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular 21 Fix Pagination Update Issue
translated: false
type: note
---

Question: In Angular 21, a worklist (parent) updates data in a pagination (child) component, but the pagination's total items and other UI don't visually update until the user clicks on it — how do I fix this change detection timing issue?

Answer:

## Root Cause

Angular v21's zoneless change detection removes Zone.js, requiring manual or signal-based triggering of change detection. Angular no longer automatically runs global checks — the UI only updates when explicitly prompted. This is why Angular 14 felt more forgiving: Zone.js would catch nearly any async update and re-run change detection for the whole tree. In Angular 21 with stricter scheduling, OnPush components are only checked on input reference changes, events in that component, `async` pipe emissions, and signal writes. Your pagination component just sits idle until you click it (which fires a DOM event, triggering its own check).

---

## Fix Options (Best to Fallback)

### ✅ Option 1 — Use Angular Signals (Recommended / Modern Way)

This is the cleanest fix. Convert your shared state (total items, current page, etc.) to signals.

**In a shared service (e.g., `worklist.service.ts`):**
```typescript
import { signal, computed } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class WorklistService {
  totalItems = signal<number>(0);
  currentPage = signal<number>(1);
  pageSize = signal<number>(10);
}
```

**In the worklist (parent) component:**
```typescript
constructor(private worklistService: WorklistService) {}

loadData() {
  this.apiService.getItems().subscribe(result => {
    this.worklistService.totalItems.set(result.total); // signal write
  });
}
```

**In the pagination (child) component template:**
{% raw %}
```html
<p>Total: {{ worklistService.totalItems() }}</p>
```
{% endraw %}

Reading a signal in a template links it to the view; writing to that signal schedules the right view to update — this makes change detection more targeted and pairs naturally with OnPush or even zoneless.

---

### ✅ Option 2 — Use `input()` Signal API (Angular 17+)

Replace `@Input()` with the new signal-based `input()` function on the pagination component:

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

**Parent passes it normally:**
```html
<app-pagination [totalItems]="total" [pageSize]="pageSize" />
```

You can use `input()` or `output()` signal APIs instead of `@Input()` or `@Output()`, eliminating the need to manually trigger change detection.

---

### ✅ Option 3 — Use `Observable` + `async` Pipe

If you prefer RxJS, use an observable in the service and subscribe via `async` pipe in the template.

**Service:**
```typescript
private totalItemsSubject = new BehaviorSubject<number>(0);
totalItems$ = this.totalItemsSubject.asObservable();

updateTotal(n: number) { this.totalItemsSubject.next(n); }
```

**Pagination template:**
{% raw %}
```html
<p>Total: {{ worklistService.totalItems$ | async }}</p>
```
{% endraw %}

The `AsyncPipe` automatically calls `markForCheck` when a new value arrives, so Angular knows to re-check that component.

---

### ⚠️ Option 4 — Manual `markForCheck()` (Fallback / Legacy)

Use this when you can't refactor to signals or observables yet:

```typescript
// pagination.component.ts
constructor(private cdr: ChangeDetectorRef) {}

ngOnChanges() {
  this.cdr.markForCheck(); // tell Angular: re-check this component
}
```

Or call it directly after receiving data from the parent:
```typescript
updatePagination(total: number) {
  this.totalItems = total;
  this.cdr.markForCheck();
}
```

Components can use the Default strategy as long as they notify Angular when change detection needs to run (calling `markForCheck`, using signals, `AsyncPipe`, etc.).

---

## Summary Table

| Approach | Angular 21 Friendly | Effort |
|---|---|---|
| Signals (`signal()`, `input()`) | ✅ Best | Low–Medium |
| Observable + `async` pipe | ✅ Good | Low |
| `markForCheck()` manually | ⚠️ Works but legacy | Low |
| Mutate `@Input()` object directly | ❌ Broken | — |

The key principle: if you are passing objects and arrays via `@Input()` and change the data in the parent component, change detection will not happen — the object data will be changed, but detection won't trigger. Always pass new object references or use signals/observables to guarantee the child re-renders.

References:

- [Angular Zoneless Guide](https://angular.dev/guide/zoneless)
- [Zoneless Change Detection in Angular v21](https://www.zignuts.com/question-and-answer/how-does-zoneless-change-detection-work-in-angular-v21)
- [Change Detection Strategies: Zones and Signals](https://blog.lunatech.com/posts/2025-11-05-change-detection-strategies-in-angular-zones-and-signals)
- [Angular OnPush Change Detection – Avoid Common Pitfalls](https://blog.angular-university.io/onpush-change-detection-how-it-works/)
- [Angular Change Detection with Zoneless – DEV Community](https://dev.to/soumayaerradi/angular-change-detection-with-zoneless-413f)