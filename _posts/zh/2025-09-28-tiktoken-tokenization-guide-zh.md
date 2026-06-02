---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-sonnet-4
title: TikToken分词指南与实例解析
translated: true
type: note
---

这段代码演示了如何使用 **TikToken** 库——这是 OpenAI 推出的分词器，用于统计和处理将发送给 GPT-3.5、GPT-4 等语言模型的文本标记。

## TikToken 的功能

TikToken 将文本转换为语言模型处理的基本单位——**标记**。每个标记大致对应一个单词或单词的一部分。理解分词机制至关重要，因为：

- API 费用基于标记数量计算
- 模型对输入/输出有标记数量限制
- 标记数量影响处理速度

## 代码详解

### 1. 基础编码 (`basic_encoding()`)

```python
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
tokens = enc.encode("Hello, how are you doing today?")
```

- 创建 GPT-3.5-turbo 专用的分词器
- 将文本转换为标记ID列表：`[9906, 11, 1268, 527, 499, 3815, 3432, 30]`
- 显示 "Hello, how are you doing today?" 对应 8 个标记
- 可将标记解码还原为原始文本

### 2. 模型对比 (`different_models()`)

比较不同模型对同一文本的分词结果：

- **GPT-4**："The quick brown fox jumps over the lazy dog." = 10 个标记
- **GPT-3.5-turbo**：10 个标记（编码相同）
- **text-davinci-003**：10 个标记（编码相同）

不同模型可能使用不同的分词器，因此标记计数可能存在差异。

### 3. 批量处理 (`batch_processing()`)

展示如何高效处理多段文本：

- 处理 3 条不同长度的消息
- 计算所有消息的总标记数（共 15 个）
- 适用于发送多条消息时的成本预估

### 4. 特殊标记 (`special_tokens()`)

处理特殊控制标记如 `<|endoftext|>`：

- 显示模型可用的特殊标记
- 演示包含特殊标记的文本编码
- 使用 `allowed_special="all"` 处理特殊标记

### 5. 高效计数 (`count_tokens_efficiently()`)

两种标记计数方法：

- **方法一**：存储标记后计数 (`len(enc.encode(text))`)
- **方法二**：直接计数（对大型文本更节省内存）
- 计算标记-单词比例（本例为 1.29）

## 实际应用场景

1. **成本预估**：在发起请求前计算 API 费用
2. **输入验证**：确保文本符合模型标记限制
3. **批量优化**：为 API 调用高效分组消息
4. **性能监控**：在应用程序中跟踪标记使用情况

## 核心洞察

- 简单短语使用的标记数可能少于预期
- 标记计数不一定等于单词计数
- 不同模型的分词结果可能不同
- 特殊标记需要谨慎处理

该库对于使用 OpenAI API 构建应用程序的开发者至关重要，它能提供与 API 实际计费完全匹配的精确标记计数。
