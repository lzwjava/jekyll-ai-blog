---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 克劳德的双重知识来源详解
translated: true
type: note
---

**问题：** Claude 如何分析事物——它使用网络搜索，还是仅仅使用模型知识（具有截止日期）？这是否适合向 Hermes 风格的智能体提问？

**答案：**

## Claude 如何分析

两种模式，取决于问题：

### 1. 模型知识（默认）
- 训练时嵌入，截止日期 **~2025年8月**
- 用于：计算机科学基础、数学、架构模式、代码、任何稳定的内容
- 快速，无延迟，无虚假 URL
- 风险：对截止日期之后的内容（新模型发布、API 变更、近期论文）可能过时

### 2. 网络搜索（触发时）
- 通过搜索工具实时获取
- 自动触发条件：需要最新信息时，例如询问当前事件、价格、谁担任某个角色、近期发布等。
- 如果我认为主题变化较快（例如“最新的 Claude API 定价”），也会手动触发。
- 您也可以明确说 **“搜索 X”** 来强制触发。

我使用的启发式规则：
```
if topic.is_stable() → model knowledge
if topic.requires_current_state() → web_search first, then answer
if topic.is_ambiguous() → search to verify
```

---

## 这是否适合向 Hermes 风格的智能体提问？

是的——以下是它为何是**结构良好的智能体查询**的原因：

```
"Do you use tool X or capability Y for task Z?"
```

这是关于智能体自身工具使用的**元推理**——这正是那种内省式查询：

1. **测试智能体的自我模型**——它是否了解自己的架构？
2. **帮助您校准信任**——知道*何时*信任模型知识而非实时搜索对于构建可靠的管道至关重要
3. **揭示工具使用透明度**——好的智能体应明确说明其使用的来源

对于您正在构建的 `hermes-agent` 或任何智能体，这个模式很有用：

```python
# Make your agent declare its source
system_prompt = """
When answering, always end with:
Source: [model_knowledge | web_search | tool:X]
Cutoff risk: [low | medium | high]
"""
```

这为您提供了**可追溯的输出**——在银行环境中，可审计性至关重要。

---

**总结：** 我默认使用模型知识，在需要最新信息时使用网络搜索。您关于工具使用的元问题是探查任何智能体的好方法——为您的智能体添加来源声明以实现生产可靠性。
