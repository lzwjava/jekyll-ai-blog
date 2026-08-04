---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 指导解码中的合规性
translated: true
type: note
---

**问题：在这个 SGLang 引导解码上下文中，"compliance" 是什么意思？**

**回答：**

在这里，**compliance 指的是 LLM 输出遵循所需格式/约束的频率**，而不是答案在事实上的正确性。

在引文中：

> 在没有约束解码的情况下，典型 LLM JSON 合规率为 90-94%；使用 SGLang 的压缩 FSM 后，合规率达到 96-98.2%。

这意味着：

* 你让模型：

```text
生成一个匹配该 schema 的 JSON 对象：

{
  "name": string,
  "age": integer,
  "email": string
}
```

* 模型生成：

✅ 合规的：

```json
{
  "name": "Alice",
  "age": 30,
  "email": "alice@example.com"
}
```

❌ 不合规的：

```text
当然！这是 JSON：

{
  "name": "Alice",
  "age": "thirty"
}
```

或者：

```json
{
  "name": "Alice",
  "age": 30,
}
```

（末尾逗号）

或者：

```json
{
  "name": "Alice",
  "age": 30,
  "extra_field": true
}
```

如果禁止额外字段。

---

### 为什么引导解码能提高合规性

通常 LLM 生成流程是：

```
提示词
  |
  v
Transformer 前向传播
  |
  v
词汇表上的 logits
  |
  v
采样下一个 token
```

模型可以选择任何 token：

```
{ "age": "thir...
```

因为 `"thirty"` 是一个有效的 token 序列，尽管 schema 要求整数。

---

引导解码添加了一个约束层：

```
              JSON FSM / 文法
                    |
                    v
提示词 --> LLM --> logits --> 屏蔽无效 token --> 采样
```

例子：

当前状态：

```
{
 "age":
```

下一个有效 token：

```
0 1 2 3 4 5 6 7 8 9
```

无效的：

```
"
t
null
true
```

解码器将无效 token 的概率设为 `-inf`：

```python
logits[invalid_tokens] = -inf
```

然后 softmax 无法选中它们。

---

### FSM 含义

SGLang 的压缩 FSM = 有限状态机，表示允许的输出路径。

对于 JSON schema：

```
START
 |
 {
 |
 "name"
 |
 :
 |
 STRING
 |
 ,
 |
 "age"
 |
 :
 |
 INTEGER
 |
 }
 |
END
```

FSM 告诉运行时：

> 在当前生成步骤，只有这些 token 是合法的。

---

### 为什么只有 96-98.2%，而不是 100%？

因为"合规性"通常衡量的是整个流水线，而不仅仅是 token 的有效性。

失败仍然可能发生：

1. **Schema 歧义**

例子：

```
age: integer
```

模型输出：

```json
{"age": 30.5}
```

取决于实现。

2. **停止处理**

模型可能提前停止：

```json
{
 "name": "Alice"
```

3. **解析器差异**

生成的输出可能通过一个 JSON 解析器，但在另一个上失败。

4. **外部约束**

例子：

```
email 必须是真实电子邮件地址
```

文法无法验证这一点。

---

对于生产级 LLM 系统，人们通常区分：

| 指标             | 含义                           |
| ---------------- | ------------------------------ |
| JSON 合规性      | 输出可解析且匹配 schema         |
| 任务准确率       | 答案内容正确                   |
| 语义质量         | 对人类的有用性                 |
| 延迟             | 每次请求的时间                 |

SGLang 的声明主要关于**结构化生成的语法可靠性**。这对于 agent 系统尤其重要，因为 LLM 必须发出工具调用：

```json
{
  "tool": "search",
  "arguments": {
    "query": "latest NVIDIA GPU"
  }
}
```

一个 98% 合规的 agent 比一个 90% 合规的容易运行得多，因为失败会随着长工作流累积。