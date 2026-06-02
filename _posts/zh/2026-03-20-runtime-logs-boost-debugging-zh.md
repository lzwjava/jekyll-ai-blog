---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 运行时日志助力 AI 调试
translated: true
type: note
---

## 是的 — 运行时日志是 AI 调试的强大信号

您识别出了一个许多开发者忽略的真正重要的调试策略。

---

### 核心洞见：仅代码往往不够

当您将代码 + 提示粘贴到 Copilot 或 Claude 时，AI 是在**猜测**运行时发生什么。但是 Angular lifecycle hooks、tab switching 和 form state 是**时机和序列问题**——它们仅通过实际执行顺序才能显现。

```
Code + Prompt = Static snapshot
Code + Prompt + Runtime Logs = What actually happened
```

---

### “Separator Log” 技术 — 为什么有效

您使用 `console.log("=== hi ===")` 作为视觉分隔符的想法是一种**合法的调试模式**。它本质上是一种手动**日志边界标记**。

```typescript
// Before triggering the tab switch
console.log("========== TAB SWITCH START ==========");

// After
console.log("========== TAB SWITCH END ==========");
```

当您复制该代码块并提供给 Copilot 时，AI 立即知道：

- **边界内触发了哪些 lifecycle events**
- **它们的触发顺序**
- **边界之间 field values 是否发生变化**

没有分隔符，200 行日志墙就变得模糊——AI 不知道哪些日志属于哪种用户操作。

---

### Angular 的更好分隔符策略

与其只用 `"hi"`，您可以让分隔符携带更多信息：

```typescript
// 1. Action-labeled separators
console.log(`%c▶ USER ACTION: Switched to Tab 2`, 'color: orange; font-weight: bold');

// 2. Timestamped separators
console.log(`===== TAB_SWITCH @ ${Date.now()} =====`);

// 3. State snapshot at boundary
console.log("===== BEFORE TAB SWITCH =====", {
  formValue: this.myForm.value,
  activeTab: this.activeTab,
  componentState: this.someState
});
```

这样，当您将日志粘贴到 AI 时，它就能获得**上下文 + 时机 + 状态**，全部在一个块中。

---

### 为什么这对 Angular 特别重要

Angular 有许多无声的 lifecycle events，会导致如 field value loss 等 bug：

| Lifecycle / Event | Common Bug |
|---|---|
| `ngOnDestroy` + `ngOnInit` | Form reset when tab re-creates component |
| `ngOnChanges` | Input binding overwrites user-typed value |
| `ChangeDetectionStrategy.OnPush` | UI not updating, looks like value lost |
| Router navigation | Component destroyed, state gone |

没有显示**哪些事件触发以及何时触发**的日志，即使 AI 也无法诊断根本原因。

---

### 实际工作流程

```
1. 添加 lifecycle logs + separator logs
2. 复现 bug（tab switch → field value lost）
3. 复制边界日志块（从分隔符到分隔符）
4. 粘贴到 Copilot/Claude，并附上：
   "Here are the logs between tab switch start and end —
    why did the field value disappear?"
```

这为 AI 提供了**可重现的证据链**，而非仅是假设。

---

### 总结

| Approach | AI Effectiveness |
|---|---|
| Code only | Low — AI guesses runtime behavior |
| Code + description | Medium — still missing execution order |
| Code + full raw logs | Medium — hard to isolate the relevant section |
| Code + **bounded, separated logs** | **High** — AI sees exactly what happened when |

您的直觉是对的：**对于前端时机 bug，带有清晰边界的运行时日志往往比任何代码或描述单独使用更有价值。**
