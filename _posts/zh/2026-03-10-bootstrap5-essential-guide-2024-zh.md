---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Bootstrap 5 精要指南 2024
translated: true
type: note
---

问题：什么是 Bootstrap 5 的全面介绍？

回答：

## 什么是 Bootstrap 5？

Bootstrap 5 是一个前端框架，帮助开发者快速高效地创建响应式且视觉吸引人的网站。它是最受欢迎的用于创建响应式、移动优先网站的 HTML、CSS 和 JavaScript 框架。

Bootstrap 是一个免费开源的 CSS 和 JavaScript 代码集合，用于创建动态网站布局和 Web 应用程序。Bootstrap 5 于 2020 年 6 月 16 日正式发布，经过数月对功能的重新定义。

---

## 从 Bootstrap 4 到 Bootstrap 5 的主要变化

Bootstrap 5 最重要的一项变化是它不再需要 jQuery。Bootstrap 已完全转向 **Vanilla JavaScript**，使其更轻量且更现代化。它还放弃了对 Internet Explorer 10 和 11 的支持，因为 IE 不再兼容现代 JavaScript 标准。

Bootstrap 5 还引入了通过 RFS（Responsive Font Sizes）引擎实现的 **Responsive Fonts**，它会根据视口大小自动调整排版元素大小，并能调整 margin、padding、border-radius 和 box-shadow 等 CSS 属性。

Bootstrap 5 还进一步利用 **CSS variables** 来更好地支持全局主题样式、单个组件和实用类。颜色、字体样式等的数十个变量可在 `:root` 级别使用，可在任何地方应用。

---

## 入门 — 安装

在项目中包含 Bootstrap 5 有两种主要方式：

**通过 CDN（最快方法）**

您可以通过 CDN 包含 Bootstrap 的生产就绪 CSS 和 JavaScript，无需任何构建步骤。您需要包含 `<meta name="viewport">` 标签以确保移动设备上的正确响应式行为，将 CSS `<link>` 置于 `<head>` 中，并在关闭 `</body>` 标签前放置 JavaScript 捆绑包的 `<script>` 标签（包括用于 dropdowns、popovers 和 tooltips 的 Popper）。

一个最小的 Bootstrap 5 HTML 模板如下所示：

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bootstrap 5 Demo</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <h1>Hello, Bootstrap 5!</h1>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**通过包管理器**

```bash
npm install bootstrap
```

然后在您的 Sass 中导入：
```scss
@import "../node_modules/bootstrap/scss/bootstrap";
```

---

## 网格系统

网格系统是 Bootstrap 布局的核心支柱。

Bootstrap 5 的网格系统是一个强大的工具，用于创建响应式布局。它采用 **12 列系统**，可适应各种屏幕尺寸。关键概念包括：Containers（最外层元素）、Rows（列的水平组）、Columns（基本构建块）和 Breakpoints（布局根据屏幕尺寸调整的点）。

**基本网格结构：**
```html
<div class="container">
  <div class="row">
    <div class="col-md-6">Left Column</div>
    <div class="col-md-6">Right Column</div>
  </div>
</div>
```

**容器类型：**

Bootstrap 提供 `.container` 用于响应式像素宽度，`.container-fluid` 用于所有视口和设备的 100% 宽度，或如 `.container-md` 这样的响应式容器，用于流体和固定宽度的组合。

---

## Breakpoints

Bootstrap 包含六个默认 Breakpoints，有时称为网格层级，用于构建响应式布局。这些 Breakpoints 可通过 `_variables.scss` 样式表中的 Sass 进行自定义。

| Breakpoint | Prefix | Min Width |
|---|---|---|
| Extra small | *(none / xs)* | < 576px |
| Small | `sm` | ≥ 576px |
| Medium | `md` | ≥ 768px |
| Large | `lg` | ≥ 992px |
| Extra large | `xl` | ≥ 1200px |
| Extra extra large | `xxl` | ≥ 1400px |

由于 Bootstrap 是采用移动优先方式开发的，它会应用最少的样式以使布局在最小 Breakpoint 上正常工作，然后叠加样式以调整设计适应更大设备。这优化了 CSS，提高了渲染时间，并为访客提供出色的体验。

**响应式列示例：**
```html
<div class="row">
  <div class="col-12 col-md-6 col-lg-4">Responsive Column</div>
  <div class="col-12 col-md-6 col-lg-8">Responsive Column</div>
</div>
```
这表示：在移动设备上全宽，在平板上半宽（md），在桌面上一分为四/八（lg）。

---

## 核心组件

Bootstrap 提供丰富的预构建组件，简化常见网站元素。以下是最重要的组件：

### 1. Navbar
一个响应式导航栏，在小屏幕上会折叠。
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">MyApp</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item"><a class="nav-link" href="#">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="#">About</a></li>
      </ul>
    </div>
  </div>
</nav>
```

### 2. Buttons
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-outline-success">Outline</button>
```

### 3. Cards
灵活的内容容器。
```html
<div class="card" style="width: 18rem;">
  <img src="image.jpg" class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card Title</h5>
    <p class="card-text">Some content here.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
```

### 4. Modal
```html
<!-- Trigger -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
  Open Modal
</button>

<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Modal Title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">Content here...</div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
```

### 5. Alerts
```html
<div class="alert alert-success" role="alert">Success! Operation completed.</div>
<div class="alert alert-warning alert-dismissible fade show" role="alert">
  Warning! Check your input.
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

### 6. Forms
Bootstrap 5 重新设计了表单系统：
```html
<form>
  <div class="mb-3">
    <label for="email" class="form-label">Email address</label>
    <input type="email" class="form-control" id="email" placeholder="name@example.com">
  </div>
  <div class="mb-3">
    <label for="password" class="form-label">Password</label>
    <input type="password" class="form-control" id="password">
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### 7. 其他关键组件
- **Carousel** — 使用 `data-bs-ride="carousel"` 的图像/内容幻灯片
- **Accordion** — 可折叠内容面板
- **Tabs / Pills** — 导航标签
- **Badges** — 小型计数和标签指示器：`<span class="badge bg-danger">5</span>`
- **Progress Bars** — `<div class="progress-bar" style="width: 70%"></div>`
- **Spinners** — `<div class="spinner-border text-primary"></div>`
- **Toasts** — 轻量级通知弹出窗口
- **Offcanvas** — 移动友好导航的侧边抽屉

---

## Utility Classes

Bootstrap 5 提供以实用类为主的类，用于间距、颜色、对齐、阴影、边框和响应式可见性，而无需编写自定义 CSS。

**Spacing** — 使用模式 `{property}{side}-{size}`，其中 size 为 0–5 或 `auto`：
```html
<div class="mt-3 mb-2 px-4 py-2">Spaced element</div>
<!-- mt = margin-top, px = padding x-axis, etc. -->
```

**Typography：**
```html
<p class="text-center text-primary fw-bold fs-4">Styled Text</p>
```

**Display：**
```html
<div class="d-none d-md-block">Visible only on md and up</div>
<div class="d-flex justify-content-between align-items-center">Flexbox row</div>
```

**Colors：**
```html
<p class="text-success bg-light p-2">Green text on light background</p>
```

**Borders & Shadows：**
```html
<div class="border border-primary rounded shadow-sm p-3">Styled box</div>
```

---

## Flexbox & Layout Utilities

Bootstrap 5 基于 Flexbox，并通过类直接暴露它：

```html
<div class="d-flex flex-wrap gap-3 justify-content-center align-items-start">
  <div class="p-2 bg-primary text-white">Item 1</div>
  <div class="p-2 bg-secondary text-white">Item 2</div>
  <div class="p-2 bg-success text-white">Item 3</div>
</div>
```

---

## 使用 Sass 进行自定义

Bootstrap 使用 Sass 实现模块化和可自定义的架构。您可以仅导入所需的组件，启用如渐变和阴影等全局选项，并使用 Bootstrap 的变量、映射、函数和混入编写自己的 CSS。

```scss
// 在导入 Bootstrap 之前覆盖变量
$primary: #e63946;
$font-size-base: 1rem;
$enable-shadows: true;

// 然后导入 Bootstrap
@import "../node_modules/bootstrap/scss/bootstrap";
```

---

## 总结 — 为什么使用 Bootstrap 5？

| Feature | Details |
|---|---|
| No jQuery | Pure Vanilla JS，轻量且更快 |
| Mobile-first | 先为小屏幕设计 |
| 12-column Grid | 灵活的响应式布局 |
| Rich Components | Navbar、modals、cards、forms 等 |
| Utility Classes | 数百个间距、颜色、flex 助手类 |
| Sass Support | 完全自定义变量和主题 |
| CSS Variables | 轻松运行时主题化 |
| IE Dropped | 仅关注现代浏览器 |
| Free & Open Source | 活跃社区和文档 |

Bootstrap 5 是构建专业响应式网站的最快方式，无需从零开始。它适合学习 Web 开发的初学者，也同样强大，适用于需要快速原型设计和一致设计系统的经验开发者。

参考资料：

- [Bootstrap 5 Official Docs — Getting Started](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Bootstrap 5 Grid System — Official](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Bootstrap 5 Breakpoints — Official](https://getbootstrap.com/docs/5.3/layout/breakpoints/)
- [Bootstrap 5 Introduction — GeeksforGeeks](https://www.geeksforgeeks.org/bootstrap-5-introduction/)
- [Bootstrap 5 Grid All Breakpoints — GeeksforGeeks](https://www.geeksforgeeks.org/bootstrap/bootstarp-5-grid-system-all-breakpoints/)
- [Bootstrap 5 Grid Tutorial — MDBootstrap](https://mdbootstrap.com/docs/standard/layout/grid/)
- [Bootstrap Breakpoints & Media Queries — BrowserStack](https://www.browserstack.com/guide/bootstrap-breakpoints-and-media-queries)
