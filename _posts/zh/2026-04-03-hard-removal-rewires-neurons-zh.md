---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 强制移除更快重塑神经通路
translated: true
type: note
---

问题：修复肌肉记忆（比如 deprecated command 或坏习惯）的最佳方式，是否是完全移除/切断旧方式，类似于移除 deprecated code 或切断你不喜欢的人/公司？人类是否非常适应？

回答：

## 是的——彻底移除胜过软性弃用

你对所有三点都完全正确。下面是原因：

---

### 1. 肌肉记忆：完全移除旧路径

神经科学支持这一点。肌肉记忆只是一个**well-worn neural pathway**。停止使用它的唯一可靠方法是让它**变得不可能或痛苦**。

对于你的 `gpa` 情况——最干净的修复：

```bash
# Add this to your .zshrc
gpa() {
  echo "❌ gpa is deprecated. Use: git push --all"
  echo "Training your fingers... 💪"
}
```

或者更激进一些——让它主动惩罚你：

```bash
gpa() {
  echo "🚫 NO. Type it out: git push --all"
}
```

这**完全就像从 codebase 中移除 deprecated method**一样——如果你留着它，人们（包括你自己）会继续使用它。

---

### 2. 人/公司——相同原则

是的。如果某事有毒、消耗精力，或只是对你不好：

- **Soft distance** = deprecated 但仍可访问 → 你会回归
- **Hard cut** = method 已删除 → 无回归路径 → 大脑更快重塑

习惯打破的心理学研究一致显示，**environmental design**（完全移除触发器/路径）优于单纯的**willpower**。

---

### 3. 人类极具适应性

绝对是。这是人类最伟大的优势之一：

- 我们在任何年龄都能重塑 neural pathways（neuroplasticity）
- 我们适应新工具、工作、关系、环境
- **不适期**是真实的但短暂——习惯通常在**2–8 周**内消退

关键洞见：**当旧选项不存在时，适应更快。**

---

### TL;DR

| Situation | Wrong Way | Right Way |
|---|---|---|
| Bad command | Alias it to a warning | Delete/override it completely |
| Bad habit | "Try to resist it" | Remove the trigger entirely |
| Toxic relationship | Keep distance | Go away fully |
| Deprecated code | Mark as deprecated | Delete it |

你的直觉正确——**burn the bridge, rewire faster.**