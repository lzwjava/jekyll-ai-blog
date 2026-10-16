---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双语切换与品牌重命名
translated: true
type: note
---

一切正常。最终总结：

## 变更

**品牌更名：智维 Software → 智维软件**
- `index.html` — `<title>`、meta description、导航品牌、Hero 副标题、页脚
- `style.css` — 头部注释
- `README.md` — 标题（另加一条关于新的双语支持的说明）
- 品牌 智维软件 在两种语言中有意保持原样。

**完整的 zh / en 语言切换**
- **`index.html`** — 在导航栏中添加了语言切换按钮（`#langToggle`）；加载新的 `i18n.js`
- **`i18n.js`**（新增）— 包含：
  - 一个包含 123 个条目的字典，将页面上每一个确切的中文字符串（导航、Hero、服务、全部 23 个案例研究、筛选器、客户、团队、流程、联系、页脚）映射到英文 — 采用最长键优先匹配，这样像 `开发` 这样的短标签就不会覆盖完整句子。
  - 针对每种语言的英文 `<title>` 和 meta description
  - 切换逻辑：就地替换所有文本节点和 `aria-label`，更新 `<html lang>`；切换回中文时恢复原始中文快照；将选择持久化到 `localStorage`；并根据浏览器语言决定默认语言（zh 浏览器 → 中文，其他 → English）
  - 按钮在中文模式下显示 **EN**，在英文模式下显示 **中**
- **`style.css`** — `.lang-toggle` 胶囊按钮样式（在移动端可见，其他导航链接隐藏），以及在英文 meta 标签后添加一个空格（`Role Design & development`）

## 使用 Playwright（真实 Chromium）验证

- ✅ 字典覆盖了全部 123 个中文文本节点 — 英文模式下没有未翻译的残留（按设计只有品牌名保留）
- ✅ 切换可以在 zh → en → zh 之间往返，并完整恢复；语言选择在重新加载后仍然保留
- ✅ `<title>`、meta description 和 `aria-label` 也会切换；无 JS 错误
- ✅ 案例研究的平台筛选器在英文下仍可正常工作；截图确认桌面端和移动端的两种布局均能良好渲染