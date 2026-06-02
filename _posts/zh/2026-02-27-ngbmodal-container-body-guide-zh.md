---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NgbModal 容器与主体详解
translated: true
type: note
---

**问题：** 在 ngb-modal 中，“container body” 是什么意思？

**答案：**

在 **ng-bootstrap**（Angular 对 Bootstrap 组件的封装）中，`NgbModal` **没有名为 "container body" 的选项或属性**。

您最可能看到（或听说）的是一组经常一起使用的两个独立概念：

- `NgbModalOptions` 中的 **`container`** 选项
- 模态框 HTML 结构中的 **`.modal-body`** 类

### 1. `container` 选项

当您使用 `NgbModal.open(...)` 打开模态框时，可以传递选项：

```ts
this.modalService.open(content, {
  container: 'body',          // ← 这是最常见的值
  // 或：container: '#some-div'
});
```

- **`container: 'body'`**（大多数情况下的默认值）
  → 模态框对话框**直接追加到 `<body>` 元素**（portal / 从组件树中的原始位置分离）。
  这是推荐且最常见的设置。

- **`container: '#my-app-root'`** 或任何其他选择器
  → 模态框追加到指定的特定元素中，而不是 `<body>`。

此设置在以下情况下很重要：

- 您的元素有 `overflow: hidden`
- 您使用 fixed/sticky 定位
- 您有 z-index 堆叠上下文问题
- 您在深度嵌套的组件中打开模态框

### 2. `.modal-body` 部分

这**不是**一个选项——它是您在模态框模板中编写的 **HTML 结构** 的一部分：

```html
<ng-template #content let-modal>
  <div class="modal-header">...</div>
  <div class="modal-body">           <!-- ← 这是 .modal-body -->
    这是带有内边距的实际内容区域。
  </div>
  <div class="modal-footer">...</div>
</ng-template>
```

`.modal-body` 是一个 **Bootstrap CSS 类**，它添加了：

- `padding`
- 适当的间距
- 内容较长时的滚动行为

因此，在 ngb-modal 讨论中，当人们说 “container body” 时，几乎总是指：

> 在模态框 **选项** 中使用 `container: 'body'`
> 并将主要内容放入模板中的 `<div class="modal-body">` 内。

### 快速总结表格

| Term              | 含义                                 | 出现位置                           | 典型值 / 用法                      |
|-------------------|--------------------------------------|------------------------------------|-------------------------------------|
| `container`       | 选项 – 模态框追加的位置              | `NgbModal.open(..., { container })` | `'body'`（最常见）                 |
| `.modal-body`     | CSS 类 – 带内边距的内容区域          | 您的模态框模板内部                 | `<div class="modal-body">...</div>`|

**最常见 / 推荐模式：**

```ts
this.modalService.open(content, { container: 'body', centered: true });
```

```html
<div class="modal-body">
  您的表单、文本、表格等内容放在这里
</div>
```

参考资料：

- [https://ng-bootstrap.github.io/#/components/modal/api](https://ng-bootstrap.github.io/#/components/modal/api)
- [https://ng-bootstrap.github.io/#/components/modal/examples](https://ng-bootstrap.github.io/#/components/modal/examples)
