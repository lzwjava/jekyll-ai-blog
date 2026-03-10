---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bootstrap 5 Key Upgrades Explained
translated: false
type: note
---

**Question:** What are the differences between Bootstrap 4 and Bootstrap 5?

**Answer:**

## Bootstrap 4 vs Bootstrap 5 — Comprehensive Comparison

---

### 1. Release & Status

| | Bootstrap 4 | Bootstrap 5 |
|---|---|---|
| **Released** | January 2018 | May 2021 |
| **End of Life** | January 1, 2023 | Actively maintained |
| **Status** | No new features; security patches only | Current stable version |

---

### 2. jQuery Dependency

One of the most significant changes. Bootstrap 4 relies on jQuery for certain components and functionalities, while Bootstrap 5 has removed the jQuery dependency, aiming for a more modern and lightweight approach. Bootstrap 5 uses **Vanilla JavaScript** instead, resulting in a smaller, faster bundle.

---

### 3. Grid System

Bootstrap 4 has a 5-tier grid system. In Bootstrap 5, the grid system was enhanced to provide easier customization and upgraded to 6 tiers by introducing the new `xxl` breakpoint to support 1400px and up.

| Breakpoint | Bootstrap 4 | Bootstrap 5 |
|---|---|---|
| xs | < 576px | < 576px |
| sm | ≥ 576px | ≥ 576px |
| md | ≥ 768px | ≥ 768px |
| lg | ≥ 992px | ≥ 992px |
| xl | ≥ 1200px | ≥ 1200px |
| **xxl** | ❌ Not available | ✅ ≥ 1400px |

Also, in Bootstrap 5, columns **no longer have a default relative position**.

---

### 4. Form Controls

Bootstrap 5 includes custom-designed form controls. In Bootstrap 4, form controls used whatever defaults each browser provided. In Bootstrap 5, the form controls offer a much more consistent look and feel across all browsers due to their custom design, built on completely semantic and standard form controls.

Bootstrap 5 also introduces **floating labels** for form inputs.

---

### 5. Utility Classes

Bootstrap 5 introduces more utility classes, making it easier to apply styles directly in HTML without the need for custom CSS. New utilities were added for gaps, overflow, positioning, sizing, and more. Bootstrap 5 also includes a powerful **Utility API** so developers can create their own custom utility classes.

---

### 6. Color System

Bootstrap 5 has expanded its color palette to explore different shades for projects, including more shades such as `$blue-200`, `$blue-100`, `$blue-300`, and so on up to `$blue-900`. Bootstrap 4 had a much more limited set of color variables.

Additionally, Bootstrap 5 introduces built-in dark mode and support for custom color palettes, allowing for greater branding flexibility.

---

### 7. New Components in Bootstrap 5

Bootstrap 5 introduces new floating forms and components like Accordions, Alerts with icons, and Offcanvas, while also updating existing components like Buttons, Dropdowns, Navbars, and Popovers to load faster.

Key new components include:
- **Offcanvas** — a flexible sidebar/drawer panel
- **Accordion** — redesigned collapsible sections
- **Floating labels** — animated label inputs
- **Updated Navbar and Dropdowns**

---

### 8. Data Attributes Naming Convention

Bootstrap 4 relied on `data-*` attribute naming for classes. Bootstrap 5 introduces a new `data-bs-*` naming convention for improved consistency and separation from native HTML attributes.

Example:
- Bootstrap 4: `data-toggle="modal"`
- Bootstrap 5: `data-bs-toggle="modal"`

---

### 9. Browser Support

Bootstrap 5 has dropped support for old browser versions such as Internet Explorer 10 and 11, Microsoft Edge < 16, Firefox < 60, Chrome < 60, and Safari < 12.

Bootstrap 4 still supported IE 10/11, which added overhead. Dropping IE support allowed Bootstrap 5 to use modern CSS features like CSS custom properties (variables).

---

### 10. CSS Custom Properties (Variables)

Bootstrap 5 makes extensive use of **CSS custom properties** (`--bs-primary`, `--bs-font-size-base`, etc.), making runtime theming possible without recompiling Sass. Bootstrap 4 had this capability only via Sass variables at compile time.

---

### 11. JavaScript Plugins

Bootstrap 5 is faster and lighter as it no longer uses jQuery; instead, it adapts to Vanilla JavaScript. Its enhanced customization of components, layout, and design provides robust flexibility in theme creation due to its CSS custom properties.

---

### 12. Documentation & Icons

Bootstrap 5's documentation has been improved, providing clearer explanations and examples. It also switches from Glyphicons to SVG icons, providing better scalability. Bootstrap Icons is now an official, standalone icon library maintained by the Bootstrap team.

---

### Summary Table

| Feature | Bootstrap 4 | Bootstrap 5 |
|---|---|---|
| Released | 2018 | 2021 |
| jQuery | ✅ Required | ❌ Removed |
| Grid Tiers | 5 | 6 (adds `xxl`) |
| Form Controls | Browser-default | Custom-designed |
| Dark Mode | ❌ | ✅ Built-in |
| Offcanvas | ❌ | ✅ |
| CSS Variables | Limited | ✅ Extensive |
| Data attributes | `data-*` | `data-bs-*` |
| IE 10/11 Support | ✅ | ❌ Dropped |
| Utility API | ❌ | ✅ |
| End of Life | Jan 2023 | Actively maintained |

---

### Which Should You Use?

- **New projects** → Always choose **Bootstrap 5**. It is actively maintained, modern, lighter, and more feature-rich.
- **Existing Bootstrap 4 projects** → Consider migrating to Bootstrap 5, especially since Bootstrap 4 reached its official end of life in January 2023 and no longer receives meaningful updates.

---

**References:**

- [LoginRadius — Bootstrap 4 vs Bootstrap 5](https://www.loginradius.com/blog/engineering/guest-post/bootstrap4-vs-bootstrap5)
- [TemplateToaster — Bootstrap 5 vs Bootstrap 4 Comparison](https://blog.templatetoaster.com/bootstrap-5-vs-bootstrap-4/)
- [Super Dev Resources — Bootstrap 5 vs Bootstrap 4](https://superdevresources.com/bootstrap5-vs-bootstrap4-whats-new/)
- [Tutlane — Bootstrap 4 vs Bootstrap 5 Differences](https://www.tutlane.com/article/bootstrap/bootstrap-4-vs-bootstrap-5-differences)
- [Vskills — Bootstrap 5 vs Bootstrap 4](https://www.vskills.in/certification/blog/bootstrap-5-vs-bootstrap-4-whats-new-and-should-you-upgrade/)
- [LinkedIn — Compare Bootstrap 4 and Bootstrap 5](https://www.linkedin.com/pulse/compare-bootstrap-4-5-which-one-good-your-project-cuong-le-zjz6c)