---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular深色模式组件清单
translated: true
type: note
---

在 Angular 前端实现深色模式时，通常你会从 `body`、`select` 和 `option` 开始，但还有许多其他常见的 HTML 元素需要重新设计样式，以确保主题风格统一。以下是一份实用清单：

### 页面级与容器

* `html`、`body` → 背景与文字颜色
* `div`、`section`、`article`、`aside`、`header`、`footer`、`main`、`nav` → 设置背景与文字颜色（特别是默认白色背景的元素）

### 文本与标题

* `h1-h6` → 确保文字在深色背景下清晰可见
* `p`、`span`、`a` → 调整文字颜色、链接悬停色彩及已访问链接状态

### 表单与输入框

* `input[type="text"]`、`input[type="password"]`、`input[type="email"]`、`textarea` → 背景、文字颜色与边框
* `input[type="checkbox"]`、`input[type="radio"]` → 有时需要特殊处理以确保可见性
* `select`、`option` → 如你所提及，需设置背景与文字颜色
* `button` → 背景、边框、文字颜色及悬停/激活状态
* `label` → 确保文字与深色背景形成对比
* `fieldset`、`legend` → 背景与边框

### 列表与表格

* `ul`、`ol`、`li` → 文字颜色
* `table` → 背景、边框颜色与文字颜色
* `thead`、`tbody`、`tr`、`th`、`td` → 单独调整背景与边框

### 交互元素

* `details`、`summary` → 背景与文字
* `dialog` → 背景与文字
* `mark` → 高亮色需适配深色模式（默认黄色可能过亮）

### 媒体与杂项

* `hr` → 边框颜色（默认样式在深色背景下常显过亮）
* `code`、`pre` → 背景与文字颜色以确保可读性
* `blockquote` → 背景与边框颜色
* `progress`、`meter` → 轨道与数值颜色

---

💡 **最佳实践**：与其大量使用 `!important`，不如定义颜色相关的 CSS 变量（如 `--bg-color`、`--text-color` 等），并在启用深色模式时切换这些变量（例如为 `body` 添加 `.dark-mode` 类）。这样 Angular 组件和自定义元素也能更优雅地接入主题系统。

需要我为你准备一份可直接嵌入 Angular 项目的**深色模式基础 CSS 代码片段**（含变量定义）作为开发起点吗？
