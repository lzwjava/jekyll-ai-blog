---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型分词机制浅析
translated: true
type: note
---

很好的问题——LLM API中的token概念起初确实容易让人困惑。让我来清晰地解释一下。

---

## 什么是Token

* **Token**是模型处理文本的最小单位
* **并不完全等同于单词**。根据语言和分词器的不同，token可能是词段、完整单词、标点符号甚至空格
* 大语言模型（如OpenAI的GPT系列）会通过预设的**分词器**将文本分割成token

例如：

* `"cat"` → 1个token
* `"cats"` → 可能被分割为`"cat"` + `"s"` → 2个token
* `"You're handsome."` → 可能分割为`"You"`, `"'re"`, `" handsome"`, `"."` → **4个token**

所以token实际上是**子词单元**，经过优化后能让模型高效处理多种语言和生僻词

---

## Token在API中的重要性

1. **计费依据**——大多数LLM API按token数量收费（输入+输出）
2. **限制条件**——模型有最大token限制（例如GPT-4 Turbo的128k就是指输入+输出总共最多128,000个token）
3. **效率优化**——减少提示词中的token数量可以降低成本并确保不超限

---

## 实际应用中的Token处理

* **估算token数量**：英语文本大致按每4个字符对应1个token估算。1000词的英语文章（约5000字符）大约需要1200-1300个token
* **精确统计token**：大多数SDK（如Python中的`tiktoken`）支持在发送前统计token数量
* **优化提示词**：

  * 删除不必要的空格/词语
  * 使用简洁的指令
  * 对上下文进行总结而非直接粘贴原始文本

---

## 示例

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
text = "You're handsome."
tokens = enc.encode(text)
print(tokens)        # 输出token ID列表
print(len(tokens))   # 输出token数量
```

这段代码可能输出类似`[9125, 3938, 13]` → 3个token（具体取决于分词器版本）

---

✅ 总结：**token ≠ 单词**。它们是LLM理解文本的基础单元。`"You're handsome."`大约包含3-4个token，而不是2个单词

---

需要我演示**如何统计你自己文本（如转录稿、文章、代码）的token数量**吗？这样你就能在调用API前预估成本和限制。
