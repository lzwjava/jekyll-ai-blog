---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 每个页面上的深色/浅色模式切换
translated: true
type: note
---

完成 ✅ — 已提交为 `8cc20d2` 并推送到 `main`。

**深色/浅色模式切换**现在已应用于每个页面（首页、作品集、全部 12 个案例页面）：

- **按钮** — 导航栏中 EN/中 切换旁边的 🌙 / ☀️ 图标按钮
- **`theme.js`** — 共享的切换逻辑：
  - 将选择保存到 `localStorage`（`zhiwei-theme`）
  - 首次访问：跟随操作系统的 `prefers-color-scheme` 设置
  - `<head>` 中的一小段内联脚本会在 CSS 加载*之前*应用主题 → 无闪烁（FOUC）
- **`style.css`** — `[data-theme="dark"]` 覆盖样式：卡片/导航/统计/筛选标签/标签的深色背景，调整了英雄区和联系区的渐变，更深的缩略图占位符，`color-scheme: dark` 用于原生滚动条/输入框
- **`i18n.js`** — 切换按钮的 `aria-label` 跟随当前语言（切换到浅色/深色模式）

已使用无头 Chrome 在两个配置文件中验证：

- `data-theme` 正确应用，包括深色持久化 → 案例页面也能正确遵循
- 截图亮度确认了真实深色（平均 28/255）与浅色（平均 247/255）渲染
- 无缺失资源或损坏的引用
