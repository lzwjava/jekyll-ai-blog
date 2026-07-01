---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bootstrap 5 Essential Guide 2024
translated: false
type: note
---

Question: What is a comprehensive introduction to Bootstrap 5?

Answer:

## What is Bootstrap 5?

Bootstrap 5 is a front-end framework that helps developers create responsive and visually appealing websites quickly and efficiently. It is the most popular HTML, CSS, and JavaScript framework for creating responsive, mobile-first websites.

Bootstrap is a free and open-source collection of CSS and JavaScript code used for creating dynamic website layouts and web applications. Bootstrap 5 was officially released on 16 June 2020 after several months of redefining its features.

---

## Key Changes from Bootstrap 4 to Bootstrap 5

The most important change in Bootstrap 5 is that it no longer requires jQuery. Bootstrap has moved completely to **Vanilla JavaScript**, which makes it lighter weight and more modern. It also dropped support for Internet Explorer 10 and 11, since IE is no longer compatible with modern JavaScript standards.

Bootstrap 5 also introduced **Responsive Fonts** via the RFS (Responsive Font Sizes) engine, which automatically resizes typography elements according to the viewport size and can also resize CSS properties like margin, padding, border-radius, and box-shadow.

Bootstrap 5 has also evolved to better utilize **CSS variables** for global theme styles, individual components, and utilities. Dozens of variables for colors, font styles, and more are available at a `:root` level for use anywhere.

---

## Getting Started — Installation

There are two main ways to include Bootstrap 5 in a project:

**Via CDN (quickest method)**

You can get started by including Bootstrap's production-ready CSS and JavaScript via CDN without the need for any build steps. You need to include the `<meta name="viewport">` tag for proper responsive behavior on mobile devices, place the CSS `<link>` in the `<head>`, and the `<script>` tag for the JavaScript bundle (including Popper for dropdowns, popovers, and tooltips) before the closing `</body>` tag.

A minimal Bootstrap 5 HTML template looks like this:

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

**Via Package Manager**

```bash
npm install bootstrap
```

Then import in your Sass:

```scss
@import "../node_modules/bootstrap/scss/bootstrap";
```

---

## The Grid System

The grid system is the backbone of Bootstrap layout.

Bootstrap 5's grid system is a powerful tool for creating responsive layouts. It utilizes a **12-column system** that adapts to various screen sizes. The key concepts are: Containers (the outermost element), Rows (horizontal groups of columns), Columns (the basic building blocks), and Breakpoints (points at which the layout adjusts based on screen size).

**Basic grid structure:**

```html
<div class="container">
  <div class="row">
    <div class="col-md-6">Left Column</div>
    <div class="col-md-6">Right Column</div>
  </div>
</div>
```

**Container types:**

Bootstrap provides `.container` for a responsive pixel width, `.container-fluid` for 100% width across all viewports and devices, or a responsive container such as `.container-md` for a combination of fluid and fixed widths.

---

## Breakpoints

Bootstrap includes six default breakpoints, sometimes referred to as grid tiers, for building responsively. These breakpoints can be customized via Sass in the `_variables.scss` stylesheet.

| Breakpoint | Prefix | Min Width |
| --- | --- | --- |
| Extra small | *(none / xs)* | < 576px |
| Small | `sm` | ≥ 576px |
| Medium | `md` | ≥ 768px |
| Large | `lg` | ≥ 992px |
| Extra large | `xl` | ≥ 1200px |
| Extra extra large | `xxl` | ≥ 1400px |

Since Bootstrap is developed mobile-first, it applies the bare minimum of styles to make a layout work at the smallest breakpoint, and then layers on styles to adjust that design for larger devices. This optimizes CSS, improves rendering time, and provides a great experience for visitors.

**Responsive column example:**

```html
<div class="row">
  <div class="col-12 col-md-6 col-lg-4">Responsive Column</div>
  <div class="col-12 col-md-6 col-lg-8">Responsive Column</div>
</div>
```

This means: full-width on mobile, half-width on tablet (md), and 4/8 split on desktop (lg).

---

## Core Components

Bootstrap provides a rich set of pre-built components that simplify common website elements. Here are the most important ones:

### 1. Navbar

A responsive navigation bar that collapses on small screens.

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

Flexible content containers.

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

Bootstrap 5 has a revamped forms system:

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

### 7. Other Key Components

- **Carousel** — image/content slideshow with `data-bs-ride="carousel"`
- **Accordion** — collapsible content panels
- **Tabs / Pills** — navigation tabs
- **Badges** — small count and labeling indicators: `<span class="badge bg-danger">5</span>`
- **Progress Bars** — `<div class="progress-bar" style="width: 70%"></div>`
- **Spinners** — `<div class="spinner-border text-primary"></div>`
- **Toasts** — lightweight notification pop-ups
- **Offcanvas** — a sidebar drawer for mobile-friendly navigation

---

## Utility Classes

Bootstrap 5 provides utility-first classes for spacing, colors, alignment, shadows, borders, and responsive visibility without writing custom CSS.

**Spacing** — uses the pattern `{property}{side}-{size}` where size is 0–5 or `auto`:

```html
<div class="mt-3 mb-2 px-4 py-2">Spaced element</div>
<!-- mt = margin-top, px = padding x-axis, etc. -->
```

**Typography:**

```html
<p class="text-center text-primary fw-bold fs-4">Styled Text</p>
```

**Display:**

```html
<div class="d-none d-md-block">Visible only on md and up</div>
<div class="d-flex justify-content-between align-items-center">Flexbox row</div>
```

**Colors:**

```html
<p class="text-success bg-light p-2">Green text on light background</p>
```

**Borders & Shadows:**

```html
<div class="border border-primary rounded shadow-sm p-3">Styled box</div>
```

---

## Flexbox & Layout Utilities

Bootstrap 5 is built on Flexbox and exposes it directly via classes:

```html
<div class="d-flex flex-wrap gap-3 justify-content-center align-items-start">
  <div class="p-2 bg-primary text-white">Item 1</div>
  <div class="p-2 bg-secondary text-white">Item 2</div>
  <div class="p-2 bg-success text-white">Item 3</div>
</div>
```

---

## Customization with Sass

Bootstrap uses Sass for a modular and customizable architecture. You can import only the components you need, enable global options like gradients and shadows, and write your own CSS with Bootstrap's variables, maps, functions, and mixins.

```scss
// Override variables BEFORE importing Bootstrap
$primary: #e63946;
$font-size-base: 1rem;
$enable-shadows: true;

// Then import Bootstrap
@import "../node_modules/bootstrap/scss/bootstrap";
```

---

## Summary — Why Use Bootstrap 5?

| Feature | Details |
| --- | --- |
| No jQuery | Pure Vanilla JS, lighter & faster |
| Mobile-first | Designed for small screens first |
| 12-column Grid | Flexible, responsive layouts |
| Rich Components | Navbars, modals, cards, forms, etc. |
| Utility Classes | Hundreds of helpers for spacing, color, flex |
| Sass Support | Full customization of variables & themes |
| CSS Variables | Easy runtime theming |
| IE Dropped | Focuses on modern browsers only |
| Free & Open Source | Active community & documentation |

Bootstrap 5 is the fastest way to build professional, responsive websites without starting from scratch. It is ideal for beginners learning web development, and equally powerful for experienced developers who need rapid prototyping and consistent design systems.

References:

- [Bootstrap 5 Official Docs — Getting Started](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Bootstrap 5 Grid System — Official](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Bootstrap 5 Breakpoints — Official](https://getbootstrap.com/docs/5.3/layout/breakpoints/)
- [Bootstrap 5 Introduction — GeeksforGeeks](https://www.geeksforgeeks.org/bootstrap-5-introduction/)
- [Bootstrap 5 Grid All Breakpoints — GeeksforGeeks](https://www.geeksforgeeks.org/bootstrap/bootstarp-5-grid-system-all-breakpoints/)
- [Bootstrap 5 Grid Tutorial — MDBootstrap](https://mdbootstrap.com/docs/standard/layout/grid/)
- [Bootstrap Breakpoints & Media Queries — BrowserStack](https://www.browserstack.com/guide/bootstrap-breakpoints-and-media-queries)
