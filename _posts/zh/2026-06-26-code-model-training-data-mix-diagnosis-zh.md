---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代码模型训练数据混合诊断
translated: true
type: note
---

**问题：** 是否无法仅用代码训练代码模型——应该混合比如20%代码、80%其他内容？以及如何看待这种训练诊断？

**回答：**

这里有两个独立问题。让我依次回答。

### 1. “不能只用代码训练，应该是20%代码？”

你*可以*用纯代码训练——CodeParrot、StarCoder-base、最初的Codex都是在几乎100%代码上训练的，效果不错。所以“必须混入自然语言”的说法**不是硬性规则**。但你直觉背后确实有真实的信号：

- **纯代码模型**（CodeParrot、SantaCoder、StarCoderBase）→接近100%代码，擅长补全，但在遵循指令或解释方面较弱。
- **通用代码模型**（DeepSeek-Coder-V2、Qwen2.5-Coder、Llama、GPT）→刻意混合。论文中的确切比例：
  - **DeepSeek-Coder-V2**：预训练数据约60%代码、10%数学、30%自然语言。
  - **DeepSeek-Coder (v1)**：87%代码、10%与代码相关的英文自然语言（markdown、StackExchange）、3%中文自然语言。
  - **StarCoder2 / The Stack v2**：代码为主，但包含pull request、issue、notebook、文档——即代码*加上*代码周围的自然语言。

所以混合比例不是“20%代码”。通常是相反的——**代码为主加上少量自然语言（10–40%）**。自然语言有助于：注释、文档字符串、变量命名语义和推理。为什么它甚至对纯代码生成也有帮助？因为代码中充满了自然语言（标识符、注释、字符串），而自然语言预训练让模型对这些token有比仅在代码上下文中看到它们时更好的先验。

对于你的124M nanoGPT规模模型，混合比例**不是你的问题**。暂时不要添加自然语言。你的问题是数据质量，而诊断准确地指出了这一点。

### 2. 诊断——对吗？

基本正确，但有一个重要的修正。

**正确的部分：**

- **脏数据是真正的罪魁祸首。** `codeparrot/github-code`是原始转储。许可证头部、HTML javadoc、配置存根——都是真的。这正是BigCode构建经过积极过滤的The Stack、以及每个严肃的代码模型都大量去重的原因。仅去重就在StarCoder工作中带来了可衡量的改进。
- **参考损失大致正确。** GPT-2 124M在OWT上大约为2.85–2.9。CodeParrot-small约为3.0。你的3.47确实很高，意味着模型还有很多提升空间。
- **选项A/B（清理或更换数据）是最高影响修复。** 正确。在相同计算量下，使用The Stack v2（`bigcode/the-stack-v2`）甚至`bigcode/the-stack-dedup`将优于原始github-code。

**错误或误导的部分：**

**“空格token主导”的说法基本上不是问题。** 26%的空格对于代码来说是*正常*的——缩进是真正的结构，不是噪声。GPT-2的BPE分词器在代码上表现很差，正是因为它将空白拆分成许多单个空格token；这是*分词器*的问题，不是数据问题。模型在`def quicksort(arr):`之后预测46.8%的空格并不是病态——换行加缩进确实是可能性最大的延续。因此我会忽略这一点。**如果你想在这里找到一个真正的杠杆，可以切换到代码感知的分词器**（StarCoder的分词器使用专用token处理连续空格/制表符），仅此一项就能改善有效上下文和损失。

**“欠拟合而非过拟合”——训练损失 > 验证损失是一个值得检查的红旗，不能盲目相信。** 对于从头训练的124M模型，训练损失*高于*验证损失通常意味着：
- 验证集比训练集更简单/多样性更低（验证集划分很小或缺乏代表性——用一个数据集的很小保留切片非常常见），
- 你在训练时使用了dropout而验证时没使用（dropout会抬高训练损失），
- 学习率仍然过高 / 你在一个噪声估计上停止了。

这并不自动意味着“模型无法学习模式”。124M*可以*学习github代码模式至约3.0。所以我会把问题3重新定义为“检查你的评估框架和dropout设置”，然后才下结论说容量/数据是瓶颈。

**选项C（训练更长时间）被低估了，*如果*损失仍在下降的话。** 在427k次迭代且单调递减的情况下，你并未达到计算饱和。但诊断正确地指出数据质量限制了你最终能降到多低——更干净的数据降低了渐近线，更多的步数只是让你沿着数据允许的渐近线前进。

### 我实际会做的顺序

1. **将分词器换成StarCoder的**（通过`tiktoken`/HuggingFace使用`bigcode/starcoder`分词器）。对代码来说性价比最高的改进；从根本上解决“空格”症状。
2. **将数据换成`bigcode/the-stack-dedup`**（或者过滤github-code，但更换比编写清理脚本工作量小）。选择3–5种语言，不要全部——语言越少，124M的信号越密集。
3. **修复评估**——确保在验证损失测量时dropout关闭，并且验证集划分是代表全体数据的随机洗牌，而非连续块。重新确认训练>验证的差距。
4. 只有到那时才考虑更长的训练或混合自然语言。

诊断的直觉（在这个规模下数据比什么都重要）是正确的，且符合Karpathy的理念。我只会消除空格token的恐慌和忽略分词器的框架，并在相信“欠拟合”结论之前验证训练/验证反转。

如果你坚持使用github-code而不是更换，一个快速的清理过滤器：

```python
def keep(text: str) -> bool:
    n = len(text)
    if n < 200:                      # 配置存根
        return False
    if text.count('<') / n > 0.05:   # HTML/javadoc过多
        return False
    head = text[:600].lower()
    if ('copyright' in head or 'license' in head) and 'def ' not in head and '{' not in head[:200]:
        return False                 # 许可证头部主导
    return True
```

但老实说——换成去重且经过筛选的数据集加上代码分词器，将胜过在原始转储上任何数量的正则清理。

**参考文献：**

- [DeepSeek-Coder-V2论文（数据混合）](https://arxiv.org/abs/2406.11931)
- [DeepSeek-Coder论文（87/10/3混合，仓库级去重）](https://arxiv.org/abs/2401.14196)
- [StarCoder2和The Stack v2](https://arxiv.org/abs/2402.19173)
- [The Stack（去重、许可证过滤）](https://arxiv.org/abs/2211.15533)
- [bigcode/the-stack-dedup在HuggingFace上](https://huggingface.co/datasets/bigcode/the-stack-dedup)