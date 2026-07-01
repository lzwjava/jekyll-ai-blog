---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular ChangeDetectorRef Injection and Usage
translated: false
type: note
---

Question: In Angular, if a component injects `ChangeDetectorRef` in its constructor, does Angular initialize the component differently than the default? And can we then call `cdr.markForCheck()`?

Answer:

## Short Answer — No, Injecting `ChangeDetectorRef` Does NOT Change How Angular Initializes the Component

Injecting `ChangeDetectorRef` (CDR) in the constructor is **just standard Angular Dependency Injection**. Angular does not initialize or bootstrap your component differently because of it. The component lifecycle (`ngOnInit`, `ngOnChanges`, etc.) runs exactly the same way as any other component.

What you *do* get is a **reference to the component's change detector**, which you can then use to manually control change detection behavior.

---

## What is `ChangeDetectorRef`?

`ChangeDetectorRef` is an abstract class that provides methods to explicitly control Angular's change detection for a specific component view.

The abstract interface looks like this:

```typescript
abstract class ChangeDetectorRef {
  abstract markForCheck(): void;
  abstract detach(): void;
  abstract detectChanges(): void;
  abstract checkNoChanges(): void;
  abstract reattach(): void;
}
```

---

## How to Inject It

{% raw %}

```typescript
@Component({
  selector: 'app-my',
  template: `{{ value }}`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MyComponent {
  value = 0;

  constructor(private cdr: ChangeDetectorRef) {}
}
```

{% endraw %}

This is plain DI. Angular's internal Ivy compiler resolves `ChangeDetectorRef` as a **special token** tied to the component's current view — but the **component initialization process is identical** to any other component.

---

## The Key Methods and When to Use Them

### 1. `cdr.markForCheck()`

When a view uses the `ChangeDetectionStrategy.OnPush` strategy, `markForCheck()` explicitly marks the view as changed so that it can be checked again.

When the `markForCheck` method is called, under the hood Angular simply iterates upwards starting from the current component view and enables checks for every parent component up to the root component.

**Important nuance:** `markForCheck()` on `ChangeDetectorRef` does **not** trigger change detection immediately — it marks all `OnPush` ancestors as to be checked once, either as part of the **current or next** change detection cycle.

**Typical use case:** Used with `OnPush` when data arrives asynchronously (e.g., from an observable, WebSocket, or timer):

```typescript
constructor(private cdr: ChangeDetectorRef) {}

ngOnInit() {
  this.data$.subscribe(newValue => {
    this.value = newValue;
    this.cdr.markForCheck(); // Tell Angular: "please re-check this component"
  });
}
```

---

### 2. `cdr.detectChanges()`

`detectChanges()` on `ChangeDetectorRef` runs change detection **immediately** on this view and its children, respecting the change detection strategy. It can be used in combination with `detach()` to implement local change detection checks.

```typescript
this.title = 'Updated';
this.cdr.detectChanges(); // Synchronously updates the view right now
```

---

### 3. `cdr.detach()` and `cdr.reattach()`

The `detach` method removes the component from Angular's change detection tree. A detached component is **not checked** during normal change detection runs until it is reattached.

This is useful for performance-critical components:

```typescript
constructor(private ref: ChangeDetectorRef) {
  ref.detach(); // Stop automatic change detection
  setInterval(() => {
    this.ref.detectChanges(); // Manually trigger every 5 seconds
  }, 5000);
}
```

---

## `markForCheck()` vs `detectChanges()` — Key Difference

| Method | Triggers CD immediately? | Scope |
| --- | --- | --- |
| `markForCheck()` | ❌ No — schedules for next cycle | Marks component + all ancestors dirty |
| `detectChanges()` | ✅ Yes — runs synchronously | Current component + children only |

When changes affect multiple components and you're sure the change detection run will follow, by calling `markForCheck` instead of `detectChanges` you're essentially reducing the number of times change detection will be called by coalescing future runs into one cycle.

---

## Summary

- Injecting `ChangeDetectorRef` **does NOT** change how Angular initializes your component. It is pure DI.
- You get a handle to the component's internal change detector, which you can use for manual control.
- `cdr.markForCheck()` is most useful with `ChangeDetectionStrategy.OnPush` to tell Angular the component needs to be re-checked on the next cycle.
- `cdr.detectChanges()` forces an immediate synchronous check on the component subtree.
- `cdr.detach()` / `cdr.reattach()` gives you full manual control over whether the component participates in change detection at all.

References:

- [Angular Official Docs — ChangeDetectorRef](https://angular.dev/api/core/ChangeDetectorRef)
- [The Last Guide For Angular Change Detection — mokkapps.de](https://mokkapps.de/blog/the-last-guide-for-angular-change-detection-you-will-ever-need)
- [Running Change Detection — Manual Control — angular.love](https://angular.love/running-change-detection-manual-control/)
- [Deep dive into OnPush — Angular In Depth](https://medium.com/angular-in-depth/deep-dive-into-the-onpush-change-detection-strategy-in-angular-fab5e4da1d69)
- [ChangeDetectorRef source code — GitHub](https://github.com/angular/angular/blob/main/packages/core/src/change_detection/change_detector_ref.ts)
