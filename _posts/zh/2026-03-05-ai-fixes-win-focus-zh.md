---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 专注AI修复获胜
translated: true
type: note
---

**问题：** 一个重要的洞见是我们应该让 AI 一次只修复一类错误，保持其上下文仅专注于那个特定问题。如果我们要求它一次性修复所有错误，它有时修复错误 A，有时错误 B，有时错误 C，这会分散其上下文并增加 LLM 的错误率，对吗？

**回答：**

是的——这是正确的，也是使用当前一代 LLM（2024–2026）进行大规模代码迁移或重构时最一致观察到的模式之一。

核心机制是 **context dilution** + **attention fragmentation** + **inconsistent pattern application**。

当你给模型提供：

- 同时多种不同的错误类型
- 数百或数千行/文件
- 多种问题的混合示例

时，通常会出现以下效果：

1. **Pattern competition**
   模型开始混合不同类别的启发式规则 → 产生不一致或错误的修复（例如，在 `sun.misc.Unsafe` 块中应用 Jakarta XML 更改规则）。

2. **Attention dilution**
   上下文窗口中不同问题的越多，模型对任何一个问题的深度应用就越少 → 错过“主要”问题细微情况的几率越高。

3. **Mode collapse / cherry-picking**
   模型往往会锁定在提示中第一个/最令人难忘的错误类型上 → 忽略或半修复其他类别。

4. **Over-generalization**
   它有时会发明一个试图同时解决一切的“超级规则” → 引入新 bug（经典示例：破坏无关代码的全面搜索替换）。

5. **Higher variance per file**
   同一个逻辑错误在文件 3 和文件 87 中的修复方式不同 → 造成审查疲劳和不一致风格。

**观察到的现实世界差异（来自多个中大型迁移的粗略数字，2024–2025）：**

| 方法                                      | 每个文件的典型接受率 | 引入的回归      | 审查工作量 | 速度（文件/天） |
|-------------------------------------------|----------------------|-----------------|------------|-----------------|
| One family at a time, tight examples      | 75–92%               | low             | medium     | high            |
| All families at once, big context         | 35–65%               | medium–high     | very high  | low–medium      |
| All families + very strong instructions   | 50–75%               | medium          | high       | medium          |
| Chain of small targeted changes           | 82–95%               | very low        | medium–low | highest         |

**2026 年实际有效的实用推荐：**

- **Ideal chunk size** — 一个错误家族 + 8–40 个示例位置（取决于模型上下文窗口）
- **最有效的提示风格**：

  ```
  你只允许更改与 [确切问题名称，例如 "javax → jakarta namespace migration"] 相关的代码。
  不要触碰：
  - 任何 Date/Calendar 代码
  - 任何 reflection / Unsafe 代码
  - 任何 var 声明
  - 任何其他 imports 或 APIs

  规则：replace javax.xml.bind → jakarta.xml.bind
        replace javax.xml.ws   → jakarta.xml.ws
        等。

  只对实际更改的行显示 BEFORE → AFTER。
  ```

- 接受一批后 → **重新编译项目** → 将**同一家族**的**新**剩余错误反馈到下一个提示中（这利用了早期修复往往揭示同一家族隐藏成员的事实）。
- 当工具允许时，每个家族使用单独的聊天会话/项目上下文（Cursor projects、Claude projects、Continue.dev named contexts 等）。

底线：
**Focused = higher quality + fewer introduced bugs + faster overall progress**
仍是 2025–2026 年大多数严肃 Java 升级项目的主导经验。

试图在一次“英雄提示”中“修复一切”几乎总会导致更慢、更痛苦，一旦计算人工审查 + bugfix 轮次。

**参考文献：**

- 无（基于 2024–2026 年开发者讨论、迁移战故事和工具使用报告中的观察模式）
