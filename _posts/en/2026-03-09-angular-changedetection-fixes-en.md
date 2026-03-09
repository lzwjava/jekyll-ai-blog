---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular Change Detection Fixes Guide
translated: false
type: note
---

Question: In Angular (modern versions with stricter change detection), a worklist component updates data in a pagination child component, but the pagination UI (e.g., `totalItems`) only renders/updates after the user physically clicks the pagination component. How do you fix this timing/change detection issue?

Answer:

## Root Cause

This is a classic **change detection timing problem**. When the parent (worklist) sets data on the pagination child:

- The data arrives **outside Angular's normal change detection flow** (e.g., from an async call, setTimeout, or an event that runs after the current CD pass)
- The pagination child uses `OnPush` or relies on `@Input()` reference checks, so it waits for the *next* CD cycle
- A user click happens to *incidentally trigger* CD, which is why clicking "fixes" it — the click event forces Angular to run change detection

---

## Fix Strategy: Choose the Right Approach

### ✅ Option 1 — Use Angular Signals (Recommended for Angular 17+/21)

This is the **modern, idiomatic fix**. Signals are reactive by nature and bypass the lifecycle timing problem entirely.

**In the worklist (parent):**
```typescript
import { signal, computed } from '@angular/core';

export class WorklistComponent {
  totalItems = signal(0);
  items = signal<MyItem[]>([]);

  loadData() {
    this.myService.getItems().subscribe(result => {
      this.items.set(result.data);
      this.totalItems.set(result.total);  // signal update is immediate + reactive
    });
  }
}
```

**In the pagination child:**
```typescript
import { input } from '@angular/core'; // Angular 17+ input signal

export class PaginationComponent {
  totalItems = input.required<number>();  // reactive signal input
}
```

**Template (parent):**
```html
<app-pagination [totalItems]="totalItems()" />
```

With `OnPush` strategy, Angular only triggers change detection if a new reference is passed as an `@Input()` value — but with Signals, updates are tracked reactively and schedule re-renders automatically without waiting for the next CD pass.

---

### ✅ Option 2 — Use `ChangeDetectorRef.detectChanges()` in the Child

If you cannot refactor to Signals, inject `ChangeDetectorRef` into the **pagination component** and call `detectChanges()` when the input is received.

**In pagination component:**
```typescript
import { Component, Input, OnChanges, SimpleChanges, ChangeDetectorRef } from '@angular/core';

export class PaginationComponent implements OnChanges {
  @Input() totalItems = 0;
  
  constructor(private cdr: ChangeDetectorRef) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['totalItems']) {
      this.cdr.detectChanges(); // force this component + children to re-render now
    }
  }
}
```

`ChangeDetectorRef.detectChanges()` forces change detection on the current view and its children, which solves the issue when the parent's async operation completes but the child view hasn't been updated yet.

---

### ✅ Option 3 — Use `markForCheck()` in the Parent After Setting Data

If the **worklist** owns the change, mark the view after updating:

```typescript
import { ChangeDetectorRef } from '@angular/core';

export class WorklistComponent {
  @ViewChild(PaginationComponent) pagination!: PaginationComponent;

  constructor(private cdr: ChangeDetectorRef) {}

  loadData() {
    this.myService.getItems().subscribe(result => {
      this.totalItems = result.total;
      this.cdr.markForCheck(); // schedules the OnPush tree to be checked
    });
  }
}
```

`markForCheck()` does not trigger change detection immediately, but marks all `OnPush` ancestors as needing to be checked — either in the current or next change detection cycle.

---

### ✅ Option 4 — Shared Reactive Service with BehaviorSubject / Observable

Use a **shared service** so the pagination component can independently subscribe and react without relying on `@Input()` timing at all.

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

```typescript
// worklist.component.ts
this.paginationState.setTotalItems(result.total);

// pagination.component.ts
totalItems$ = this.paginationState.totalItems;
// template: {{ totalItems$ | async }}
```

Using a shared service with observables is especially useful for deeply nested components, avoiding the need to bubble data and events up and down the component tree via `@Input`/`@Output` chains.

---

## Summary — Which Option to Pick?

| Situation | Best Fix |
|---|---|
| Angular 17+ / 21 modern project | **Signals + `input()`** |
| Existing `@Input()` pattern, can't refactor | **`ChangeDetectorRef.detectChanges()` in child** |
| Parent controls the update | **`markForCheck()` in parent** |
| Deeply nested or shared state | **Shared BehaviorSubject service** |

The core principle: **never rely on a user interaction to accidentally trigger change detection**. Either use reactive primitives (Signals, Observables) or explicitly schedule a CD check after async data arrives.

References:

- [Angular OnPush Change Detection Pitfalls](https://blog.angular-university.io/onpush-change-detection-how-it-works/)
- [The Last Guide For Angular Change Detection](https://mokkapps.de/blog/the-last-guide-for-angular-change-detection-you-will-ever-need)
- [Angular Parent-Child ChangeDetectorRef Fix](https://www.w3tutorials.net/blog/call-child-component-method-from-parent-class-angular/)
- [NgRx SignalStore Pagination Example](https://ngrx.io/guide/signals/signal-store)