---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 HTML 上下文的精确修复
translated: true
type: note
---

问题：为什么在升级 Angular/Bootstrap 时，向 Copilot/Claude 等 AI 工具提供（前后）HTML 元素是一个有效策略，这种方法如何帮助解决像 `form-group` 等被移除的类的问题？

回答：

## 为什么为 Angular/Bootstrap 升级提供前后 HTML 上下文如此有效

### “仅自然语言”提示的核心问题

当你只是说：
> *“Bootstrap 升级后表单看起来不对”*

AI 没有任何**具体证据**——它只能猜测。但当你提供实际 HTML 时，它就有了**真实依据**。

---

### “前后 HTML”策略

#### ✅ 给 AI 提供什么

```
BEFORE (Bootstrap 4):
<div class="form-group">
  <label for="email">Email</label>
  <input type="email" class="form-control" id="email">
  <small class="form-text text-muted">Help text</small>
</div>

AFTER UPGRADE (Bootstrap 5 - broken now):
<div class="form-group">   <!-- ❌ form-group removed in BS5 -->
  <label for="email">Email</label>
  <input type="email" class="form-control" id="email">
  <small class="form-text text-muted">Help text</small>
</div>

PROBLEM: Spacing between fields is gone, layout collapsed
```

现在 Claude/Copilot **立即知道**：
- 确切哪个类错了（`form-group`）
- 结构是什么样的
- 预期的视觉行为是什么

---

### 为什么 HTML 元素比自然语言更好

| 方法 | AI 理解 | 修复质量 |
|---|---|---|
| “表单看起来坏了” | 模糊，猜测 | 通用答案 |
| “form-group 不起作用” | 部分 | 可能修复错的东西 |
| **粘贴完整的 before/after HTML** | **精确，无歧义** | **针对性，正确修复** |

---

### Bootstrap 4 → 5 常见破坏性变更（此策略最有效的地方）

```html
<!-- ❌ BS4: form-group REMOVED in BS5 -->
<div class="form-group"> → <div class="mb-3">

<!-- ❌ BS4: text-left REMOVED in BS5 -->
<p class="text-left"> → <p class="text-start">

<!-- ❌ BS4: float-left REMOVED -->
<div class="float-left"> → <div class="float-start">

<!-- ❌ BS4: ml-* mr-* REMOVED (replaced with ms-* me-*) -->
<div class="ml-2 mr-3"> → <div class="ms-2 me-3">

<!-- ❌ BS4: badge-primary changed -->
<span class="badge badge-primary"> → <span class="badge bg-primary">
```

当你粘贴**实际损坏的 HTML** 时，Claude 可以一次性发现所有这些问题——不仅仅是你注意到的一个。

---

### Angular 特定：还要包含组件上下文

对于 Angular 升级，添加**组件选择器 + 模板片段**：

```html
<!-- Tell AI: This is Angular 15 → 17, standalone component -->

<!-- BEFORE (worked in ng15): -->
<mat-form-field appearance="legacy">  <!-- ❌ legacy removed in Angular Material 15+ -->
  <input matInput placeholder="Name">
</mat-form-field>

<!-- What error shows: No provider for MAT_FORM_FIELD_DEFAULT_OPTIONS -->
```

这告诉 AI：版本上下文 + 损坏元素 + 错误消息——一个**完整画面**。

---

### 理想提示模板

```
Upgrading from [Bootstrap 4 / Angular X] to [Bootstrap 5 / Angular Y].

This HTML worked before:
--- BEFORE ---
[paste old HTML]
--- END ---

After upgrade it now looks/behaves like:
--- AFTER ---
[paste current broken HTML]
--- END ---

Problem: [one sentence — e.g., "spacing is gone between form fields" 
          or "button alignment shifted right"]

Please fix the AFTER HTML to match the BEFORE behavior.
```

---

### 为什么这是你描述的“轻松胜利”

- AI 工具无需**想象**你的布局——它们**看到**它
- 它们可以在脑海中对前后进行**diff**
- 它们能一次性捕捉**多个问题**，不仅仅是你描述的那个
- 修复是**复制粘贴即用**的，而不是抽象建议
- 减少来回对话，更快迭代

> HTML 元素**就是**规范。自然语言描述意图；HTML 显示**现实**。