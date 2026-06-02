---
audio: false
generated: true
image: false
lang: en
layout: post
title: NgbModal Container and Body Explained
translated: false
type: note
---

**Question:** What does "container body" mean in ngb-modal?

**Answer:**

In **ng-bootstrap** (the Angular wrapper for Bootstrap components), there is **no option or property called "container body"** in `NgbModal`.

What you are most likely seeing (or hearing about) is the combination of two separate concepts that are frequently used together:

- **`container`** option in `NgbModalOptions`
- **`.modal-body`** class in the modal's HTML structure

### 1. The `container` option

When you open a modal with `NgbModal.open(...)`, you can pass options:

```ts
this.modalService.open(content, {
  container: 'body',          // ← this is the most common value
  // or: container: '#some-div'
});
```

- **`container: 'body'`** (default in most cases)
  → The modal dialog is **appended directly to the `<body>`** element (portal / detached from its original place in the component tree).
  This is the recommended and most common setting.

- **`container: '#my-app-root'`** or any other selector
  → The modal is appended inside that specific element instead of `<body>`.

This setting is important when:

- You have elements with `overflow: hidden`
- You use fixed/sticky positioning
- You have z-index stacking context problems
- You open modals inside deeply nested components

### 2. The `.modal-body` part

This is **not** an option — it's part of the **HTML structure** you write inside your modal template:

```html
<ng-template #content let-modal>
  <div class="modal-header">...</div>
  <div class="modal-body">           <!-- ← this is .modal-body -->
    This is the actual content area with padding.
  </div>
  <div class="modal-footer">...</div>
</ng-template>
```

`.modal-body` is a **Bootstrap CSS class** that adds:

- `padding`
- Proper spacing
- Scroll behavior when content is long

So when people say "container body" in ngb-modal conversations, they almost always mean:

> Use `container: 'body'` in the modal **options**
> and put your main content inside `<div class="modal-body">` in the template.

### Quick summary table

| Term              | What it is                           | Where it appears                  | Typical value / usage              |
|-------------------|--------------------------------------|------------------------------------|-------------------------------------|
| `container`       | Option – where to append the modal   | `NgbModal.open(..., { container })` | `'body'` (most common)             |
| `.modal-body`     | CSS class – content area with padding| Inside your modal template         | `<div class="modal-body">...</div>`|

**Most common / recommended pattern:**

```ts
this.modalService.open(content, { container: 'body', centered: true });
```

```html
<div class="modal-body">
  Your form, text, table, etc. goes here
</div>
```

References:

- [https://ng-bootstrap.github.io/#/components/modal/api](https://ng-bootstrap.github.io/#/components/modal/api)
- [https://ng-bootstrap.github.io/#/components/modal/examples](https://ng-bootstrap.github.io/#/components/modal/examples)
