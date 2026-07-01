---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Bootstrap 5 主要升级详解
translated: true
type: note
---

**问题：** Bootstrap 4 和 Bootstrap 5 之间的区别是什么？

**答案：**

## Bootstrap 4 与 Bootstrap 5 — 全面比较

---

### 1. 发布与状态

|

| Bootstrap 4 | Bootstrap 5 |
|---|---|---|
| **发布日期** | 2018 年 1 月 | 2021 年 5 月 |
| **生命周期结束** | 2023 年 1 月 1 日 | 持续维护 |
| **状态** | 无新功能；仅安全补丁 | 当前稳定版本 |

---

### 2. jQuery 依赖

最显著的变化之一。Bootstrap 4 依赖 jQuery 来实现某些组件和功能，而 Bootstrap 5 移除了 jQuery 依赖，旨在采用更现代和轻量级的方法。Bootstrap 5 使用 **Vanilla JavaScript** 代替，从而产生更小、更快的捆绑包。

---

### 3. 栅格系统

Bootstrap 4 具有 5 级栅格系统。在 Bootstrap 5 中，栅格系统得到增强，提供更容易的自定义，并升级为 6 级，通过引入新的 `xxl` 断点来支持 1400px 及以上。

| Breakpoint | Bootstrap 4 | Bootstrap 5 |
| --- | --- | --- |
| xs | < 576px | < 576px |
| sm | ≥ 576px | ≥ 576px |
| md | ≥ 768px | ≥ 768px |
| lg | ≥ 992px | ≥ 992px |
| xl | ≥ 1200px | ≥ 1200px |
| **xxl** | ❌ 不可用 | ✅ ≥ 1400px |

此外，在 Bootstrap 5 中，列 **不再具有默认的相对位置**。

---

### 4. 表单控件

Bootstrap 5 包含自定义设计的表单控件。在 Bootstrap 4 中，表单控件使用浏览器提供的默认设置。在 Bootstrap 5 中，由于其自定义设计，表单控件在所有浏览器中提供更一致的外观和感觉，这些设计基于完全语义化和标准的表单控件。

Bootstrap 5 还引入了表单输入的 **浮动标签**。

---

### 5. 实用类

Bootstrap 5 引入了更多实用类，使其更容易直接在 HTML 中应用样式，而无需自定义 CSS。新增了用于间隙、溢出、定位、尺寸等的实用类。Bootstrap 5 还包含强大的 **Utility API**，允许开发者创建自己的自定义实用类。

---

### 6. 颜色系统

Bootstrap 5 扩展了其颜色调色板，以探索项目的不同色调，包括更多色调，如 `$blue-200`、`$blue-100`、`$blue-300` 等，直至 `$blue-900`。Bootstrap 4 的颜色变量集非常有限。

此外，Bootstrap 5 引入了内置深色模式和对自定义颜色调色板的支持，从而提供更大的品牌灵活性。

---

### 7. Bootstrap 5 中的新组件

Bootstrap 5 引入了新的浮动表单和组件，如折叠面板（Accordions）、带图标的警告（Alerts）和 Offcanvas，同时更新了现有组件，如 Buttons、Dropdowns、Navbars 和 Popovers，以实现更快的加载。

关键新组件包括：

- **Offcanvas** — 灵活的侧边栏/抽屉面板
- **Accordion** — 重新设计的可折叠部分
- **Floating labels** — 动画标签输入
- **更新的 Navbar 和 Dropdowns**

---

### 8. 数据属性命名约定

Bootstrap 4 依赖 `data-*` 属性命名来处理类。Bootstrap 5 引入了新的 `data-bs-*` 命名约定，以提高一致性和与原生 HTML 属性的分离。

示例：

- Bootstrap 4: `data-toggle="modal"`
- Bootstrap 5: `data-bs-toggle="modal"`

---

### 9. 浏览器支持

Bootstrap 5 放弃了对旧浏览器版本的支持，如 Internet Explorer 10 和 11、Microsoft Edge < 16、Firefox < 60、Chrome < 60 和 Safari < 12。

Bootstrap 4 仍支持 IE 10/11，这增加了开销。放弃 IE 支持使 Bootstrap 5 能够使用现代 CSS 功能，如 CSS 自定义属性（变量）。

---

### 10. CSS 自定义属性（变量）

Bootstrap 5 大量使用 **CSS 自定义属性**（`--bs-primary`、`--bs-font-size-base` 等），使运行时主题化成为可能，而无需重新编译 Sass。Bootstrap 4 仅通过编译时的 Sass 变量提供此功能。

---

### 11. JavaScript 插件

Bootstrap 5 更快、更轻量，因为它不再使用 jQuery；相反，它适应 Vanilla JavaScript。其对组件、布局和设计的增强自定义提供了强大的主题创建灵活性，这得益于其 CSS 自定义属性。

---

### 12. 文档与图标

Bootstrap 5 的文档得到改进，提供更清晰的解释和示例。它还从 Glyphicons 切换到 SVG 图标，提供更好的可缩放性。Bootstrap Icons 现在是 Bootstrap 团队维护的官方独立图标库。

---

### 总结表格

| 特性 | Bootstrap 4 | Bootstrap 5 |
| --- | --- | --- |
| 发布日期 | 2018 | 2021 |
| jQuery | ✅ 必需 | ❌ 已移除 |
| 栅格层级 | 5 | 6（添加 `xxl`） |
| 表单控件 | 浏览器默认 | 自定义设计 |
| 深色模式 | ❌ | ✅ 内置 |
| Offcanvas | ❌ | ✅ |
| CSS 变量 | 有限 | ✅ 大量使用 |
| 数据属性 | `data-*` | `data-bs-*` |
| IE 10/11 支持 | ✅ | ❌ 已放弃 |
| Utility API | ❌ | ✅ |
| 生命周期结束 | 2023 年 1 月 | 持续维护 |

---

### 您应该使用哪个？

- **新项目** → 始终选择 **Bootstrap 5**。它正在积极维护、更现代、更轻量且功能更丰富。
- **现有 Bootstrap 4 项目** → 考虑迁移到 Bootstrap 5，特别是因为 Bootstrap 4 已于 2023 年 1 月达到官方生命周期结束，不再接收有意义的更新。

---

**参考资料：**

- [LoginRadius — Bootstrap 4 vs Bootstrap 5](https://www.loginradius.com/blog/engineering/guest-post/bootstrap4-vs-bootstrap5)
- [TemplateToaster — Bootstrap 5 vs Bootstrap 4 Comparison](https://blog.templatetoaster.com/bootstrap-5-vs-bootstrap-4/)
- [Super Dev Resources — Bootstrap 5 vs Bootstrap 4](https://superdevresources.com/bootstrap5-vs-bootstrap4-whats-new/)
- [Tutlane — Bootstrap 4 vs Bootstrap 5 Differences](https://www.tutlane.com/article/bootstrap/bootstrap-4-vs-bootstrap-5-differences)
- [Vskills — Bootstrap 5 vs Bootstrap 4](https://www.vskills.in/certification/blog/bootstrap-5-vs-bootstrap-4-whats-new-and-should-you-upgrade/)
- [LinkedIn — Compare Bootstrap 4 and Bootstrap 5](https://www.linkedin.com/pulse/compare-bootstrap-4-5-which-one-good-your-project-cuong-le-zjz6c)
