---
audio: false
generated: true
image: false
lang: en
layout: post
title: NgBootstrap Modal Z-Index Handling
translated: false
type: note
---

**Question:** What if there are two NgbModals open at the same time? How do we handle the z-index of them?

**Answer:**

NgbModal (from @ng-bootstrap) already handles multiple open modals correctly in almost all real-world cases.

### Default behavior (2024–2026 versions)

When you open a second modal while the first one is still open:

- The **newest modal** gets a higher z-index automatically
- ng-bootstrap adds incremental z-index values using this pattern:

```css
.modal:nth-of-type(n+2) {
  z-index: 1055;   /* or higher */
}
.modal-backdrop:nth-of-type(n+2) {
  z-index: 1050;   /* or higher */
}
```

Typical z-index progression:

| Modal order | Modal z-index | Backdrop z-index |
|-------------|----------------|------------------|
| 1st modal   | 1050           | 1040             |
| 2nd modal   | 1055           | 1050             |
| 3rd modal   | 1060           | 1055             |
| ...         | +5 each time   | +5 each time     |

So in the default case **you usually don't need to do anything** — the last opened modal is on top.

### When you actually get z-index problems

You need manual intervention mainly in these situations:

1. You have custom very high z-index elements (tooltips, notifications, intercom, floating action buttons, etc.)
2. You use `windowClass` or global styles that set `z-index` explicitly
3. You nest modals inside other positioned elements with `overflow: hidden` or own z-index
4. You open many modals (5+) and Bootstrap's increment becomes insufficient

### Solutions (from most recommended to more invasive)

#### 1. Best & cleanest – use `windowClass` + higher z-index only when needed

```ts
this.modalService.open(MyVeryImportantModalComponent, {
  windowClass: 'very-important-modal',
  // ... other options
});
```

```css
/* global styles or component stylesheet */
.very-important-modal {
  z-index: 1080 !important;          /* higher than normal modals */
}

.very-important-modal + .modal-backdrop {
  z-index: 1075 !important;
}
```

#### 2. Force higher base z-index for all modals (simple but global)

Add this to global `styles.scss`:

```css
.ngb-modal-window {
  z-index: 1100 !important;
}
.modal-backdrop.show {
  z-index: 1090 !important;
}
```

→ Good quick fix when your app has many overlapping high-z elements (like live-chat widgets).

#### 3. Use modal options `backdropClass` + `windowClass` together

```ts
this.modalService.open(UrgentAlertComponent, {
  windowClass: 'emergency-modal',
  backdropClass: 'emergency-backdrop',
  backdrop: 'static',
  keyboard: false
});
```

```css
.emergency-modal   { z-index: 1200 !important; }
.emergency-backdrop { z-index: 1190 !important; }
```

#### 4. Last resort – patch ng-bootstrap modal z-index logic (not recommended)

You can listen to modal events and dynamically increase z-index, but it's fragile and usually unnecessary.

```ts
// Example – avoid if possible
modalRef._windowCmptRef.instance.windowClass = 'force-top';
```

### Quick decision table

| Situation                              | Recommended fix                              |
|----------------------------------------|----------------------------------------------|
| Normal app, 2–3 modals                 | Do nothing – ng-bootstrap handles it         |
| Last modal must always be on top       | Nothing needed (already default behavior)    |
| Custom high z-index elements overlap   | Use `windowClass` with higher z-index        |
| Many nested / chained modals           | Increase global `.ngb-modal-window` z-index  |
| One special "emergency" modal          | Use dedicated `windowClass` + `backdropClass`|
| Still broken after all above           | Check parent containers for `overflow:hidden` or `z-index` |

### Summary – most common real-world pattern in 2025–2026

```ts
// Normal modal
this.modalService.open(RegularModalComponent);

// Important modal that must be above everything
this.modalService.open(AdminActionModalComponent, {
  windowClass: 'admin-critical-modal',
  backdrop: 'static',
  keyboard: false
});
```

```css
.admin-critical-modal {
  z-index: 1100 !important;
}
.admin-critical-modal ~ .modal-backdrop {
  z-index: 1095 !important;
}
```

In 95% of Angular applications using ng-bootstrap you will **never need to touch z-index** manually.

**References:**

- https://ng-bootstrap.github.io/#/components/modal/examples
- https://github.com/ng-bootstrap/ng-bootstrap/issues/2195
- https://github.com/ng-bootstrap/ng-bootstrap/issues?q=is%3Aissue+z-index+modal
