---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 AI 快速修复构建错误
translated: true
type: note
---

## AI 编码助手的单次错误修复策略

您描述了一种非常有效的提示工程技术。以下是其工作原理以及系统应用方法的全面分解。

---

### 为什么此策略有效

当您一次性粘贴所有 20 个错误并要求 AI“修复它们所有”时，AI 必须**猜测**模式。但是当您：

1. 手动**修复一个错误**（或让 AI 只修复一个）
2. 将**该修复作为示例展示给 AI**
3. 然后粘贴**所有剩余的类似错误**

……您就给了 AI 一个**具体模板**——这被称为**one-shot prompting**，它能显著提高准确性，因为模型不再需要推断意图。

---

### 逐步工作流程

```
步骤 1: 运行构建
  mvn compile  OR  npm run build
  → 获取 20 个错误

步骤 2: 按 TYPE/FAMILY 分组错误
  - Type A: NullPointerException 模式 (8 个错误)
  - Type B: 缺少 import (7 个错误)
  - Type C: 类型不匹配 (5 个错误)

步骤 3: 手动或使用 AI 帮助修复 Type A 中的一个错误
  → 这将成为您的“示例”

步骤 4: 提示 AI：
  "这里是一个错误及其修复的示例：
   [ERROR SAMPLE] → [FIXED CODE SAMPLE]

   现在这里有来自同一构建的 8 个类似错误。
   对每个错误应用相同的修复模式：
   [粘贴所有 8 个错误]"

步骤 5: 对 Type B 和 Type C 系列重复执行
```

---

### 可重用的提示模板

```
我有多个相同类型的构建错误。

这里是一个示例错误以及我如何修复它：

--- 修复前 ---
[paste original broken code snippet]

--- 错误消息 ---
[paste the specific error]

--- 修复后 ---
[paste corrected code snippet]

现在这里是我构建输出中的所有类似错误。
请对每个错误应用相同的修复模式：

[paste all similar error messages with file:line references]
```

---

### 为什么“错误家族”很重要

| Approach | AI Accuracy | Why |
| --- | --- | --- |
| 一次性抛出所有 20 个错误 | ~50–60% | AI 猜测模式 |
| 使用 one-shot 按错误家族修复 | ~85–95% | AI 有具体参考 |
| 逐个错误修复 | 准确但缓慢 | 无并行性 |

按家族分组意味着**具有相同根本原因**的错误将获得相同处理，避免不一致的修复。

---

### 最大化准确性的提示

- **包含文件名 + 行号**在您的粘贴中，以便 AI 推理范围
- **按错误代码分组**（例如 TS2345、NullPointerException、cannot find symbol）——相同代码 = 同一家族
- AI 生成修复后，**立即重新运行构建**——在验证前不要批量处理太多家族
- 如果一个家族有**变体**，提供**2 个示例**（two-shot）而不是一个
- 对于 `mvn` Java 错误，复制 `[ERROR]` 前缀行最有用——跳过 `[INFO]` 噪声

---

### 示例：TypeScript / npm run build

```
Family: TS2345 - Argument of type 'string' is not assignable to parameter of type 'number'

您提供的示例修复：
  BEFORE: doSomething(userId)   // userId is string
  AFTER:  doSomething(Number(userId))

然后粘贴所有 12 个 TS2345 错误 → AI 一致应用 Number() 转换
```

---

### 总结

> **修复 1 个 → 向 AI 展示修复 → 给 AI 所有类似错误 → 让它批量应用模式**

这本质上是**通过示例教导 AI**，这与 LLM 表现最佳的方式一致。单次示例消除了歧义，并将模型的行为锚定到您的特定代码库风格和修复约定。
