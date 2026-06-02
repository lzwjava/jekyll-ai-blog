---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular ChangeDetectorRef 注入与使用
translated: true
type: note
---

Question: 在 Angular 中，如果一个组件在其构造函数中注入 `ChangeDetectorRef`，Angular 是否会以不同于默认的方式初始化该组件？并且我们是否可以然后调用 `cdr.markForCheck()`？

Answer:

## 简短回答 — 不，在构造函数中注入 `ChangeDetectorRef` **不会**改变 Angular 初始化组件的方式

在构造函数中注入 `ChangeDetectorRef` (CDR) **只是标准的 Angular 依赖注入**。由于这个原因，Angular 不会以不同的方式初始化或引导你的组件。组件生命周期（`ngOnInit`、`ngOnChanges` 等）运行方式与其他组件完全相同。

你*确实*获得的是**组件变更检测器的引用**，你可以用它来手动控制变更检测行为。

---

## 什么是 `ChangeDetectorRef`？

`ChangeDetectorRef` 是一个抽象类，它提供了明确控制特定组件视图的 Angular 变更检测的方法。

抽象接口如下所示：

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

## 如何注入它

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

这是普通的 DI。Angular 的内部 Ivy 编译器将 `ChangeDetectorRef` 解析为与组件当前视图绑定的**特殊 token** — 但**组件初始化过程与其他组件完全相同**。

---

## 关键方法及其使用时机

### 1. `cdr.markForCheck()`

当视图使用 `ChangeDetectionStrategy.OnPush` 策略时，`markForCheck()` 会明确将视图标记为已更改，以便重新检查它。

调用 `markForCheck` 方法时，在底层 Angular 会从当前组件视图开始向上迭代，并为每个父组件直到根组件启用检查。

**重要细节：** `ChangeDetectorRef` 上的 `markForCheck()` **不会**立即触发变更检测 — 它会将所有 `OnPush` 祖先标记为在**当前或下一个**变更检测周期中检查一次。

**典型用例：** 与 `OnPush` 结合使用，当数据异步到达时（例如来自 observable、WebSocket 或定时器）：

```typescript
constructor(private cdr: ChangeDetectorRef) {}

ngOnInit() {
  this.data$.subscribe(newValue => {
    this.value = newValue;
    this.cdr.markForCheck(); // 告诉 Angular：“请重新检查此组件”
  });
}
```

---

### 2. `cdr.detectChanges()`

`ChangeDetectorRef` 上的 `detectChanges()` 会**立即**在该视图及其子视图上运行变更检测，尊重变更检测策略。它可以与 `detach()` 结合使用，以实现本地变更检测检查。

```typescript
this.title = 'Updated';
this.cdr.detectChanges(); // 立即同步更新视图
```

---

### 3. `cdr.detach()` 和 `cdr.reattach()`

`detach` 方法会将组件从 Angular 的变更检测树中移除。被分离的组件在重新附加之前**不会**在正常变更检测运行中被检查。

这对于性能关键的组件很有用：

```typescript
constructor(private ref: ChangeDetectorRef) {
  ref.detach(); // 停止自动变更检测
  setInterval(() => {
    this.ref.detectChanges(); // 每 5 秒手动触发一次
  }, 5000);
}
```

---

## `markForCheck()` 与 `detectChanges()` — 关键区别

| 方法 | 是否立即触发变更检测？ | 作用范围 |
|---|---|---|
| `markForCheck()` | ❌ 否 — 调度到下一个周期 | 将组件 + 所有祖先标记为脏 |
| `detectChanges()` | ✅ 是 — 同步运行 | 当前组件 + 子组件のみ |

当变更影响多个组件并且你确定后续会有变更检测运行时，通过调用 `markForCheck` 而非 `detectChanges`，你本质上减少了变更检测的调用次数，将未来的运行合并到一个周期中。

---

## 总结

- 注入 `ChangeDetectorRef` **不会**改变 Angular 初始化你的组件的方式。它是纯 DI。
- 你获得了组件内部变更检测器的句柄，可以用于手动控制。
- `cdr.markForCheck()` 最适用于 `ChangeDetectionStrategy.OnPush`，用于告诉 Angular 该组件需要在下一个周期中重新检查。
- `cdr.detectChanges()` 强制对组件子树进行立即同步检查。
- `cdr.detach()` / `cdr.reattach()` 让你完全手动控制组件是否参与变更检测。

References:

- [Angular Official Docs — ChangeDetectorRef](https://angular.dev/api/core/ChangeDetectorRef)
- [The Last Guide For Angular Change Detection — mokkapps.de](https://mokkapps.de/blog/the-last-guide-for-angular-change-detection-you-will-ever-need)
- [Running Change Detection — Manual Control — angular.love](https://angular.love/running-change-detection-manual-control/)
- [Deep dive into OnPush — Angular In Depth](https://medium.com/angular-in-depth/deep-dive-into-the-onpush-change-detection-strategy-in-angular-fab5e4da1d69)
- [ChangeDetectorRef source code — GitHub](https://github.com/angular/angular/blob/main/packages/core/src/change_detection/change_detector_ref.ts)
