---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 科学空间的最佳英文替代方案
translated: true
type: note
---

问题：**有哪些好的英语替代品可以替代苏剑林的“科学空间”（`spaces.ac.cn`）？**

回答：有的。但**没有完全1:1的等价物**。Scientific Spaces 之所以特别出色，在于它结合了：

* 数学推导
* 实现层面的理解
* 关注“为什么这样工作”而非仅仅“这是什么”
* Transformer/LLM 架构
* 多年追踪研究进展
* 偶尔自己提出或分析新想法

针对你的水平，我对英语生态的排名如下：

### 1. Sebastian Raschka —— 整体最接近

Sebastian Raschka

[Sebastian Raschka 的博客](https://sebastianraschka.com/?utm_source=chatgpt.com)

这很可能是**你目前最接近的英语等效资源**。

他从实践者/研究者的角度写作，经常从公式 → PyTorch → 实际模型行为。

尤其擅长：

* LLM 架构
* 注意力机制
* 缩放（scaling）
* 训练
* PyTorch 实现
* 通过重建来阅读论文

他当前的文章索引明确涵盖了 **LLM 架构、推理模型、PyTorch 以及从头实现**。([Sebastian Raschka, PhD][1])

他的 LLM 阅读列表也明确推荐 Jay Alammar 和 Lilian Weng 作为补充技术资源。([Sebastian Raschka, PhD][2])

---

### 2. Lilian Weng —— 数学/概念深度最强

Lilian Weng

[Lilian Weng 的博客](https://lilianweng.github.io/?utm_source=chatgpt.com)

这不像苏剑林那样“我发明/分析了这个架构”，但在构建现代 ML 的**概念/数学地图**方面非常出色。

好的主题包括：

* 注意力机制
* 扩散模型
* 强化学习
* RLHF
* 智能体
* 生成模型
* LLM 推理

当你想要以下内容时，可以使用 Lilian Weng：

> “给我这个技术周围的数学全景。”

---

### 3. Jay Alammar —— 最佳视觉直觉

Jay Alammar

[图解 Transformer](https://jalammar.github.io/illustrated-transformer/?utm_source=chatgpt.com)

与 Scientific Spaces 风格截然不同，但非常有用。

他著名的**图解 Transformer** 给出了前向传递的可视化理解：

```text
tokens
  ↓
embeddings
  ↓
Q K V
  ↓
attention
  ↓
FFN
  ↓
residual
  ↓
next layer
```

在深入学习某个架构的公式之前，这很难被超越。

---

### 4. Aman Arora —— 实现优先的深度学习

[Aman Arora 的博客](https://amaarora.github.io/?utm_source=chatgpt.com)

这更接近：

> “让我们实际实现这篇论文，理解每个张量。”

如果你希望从以下路径出发，而不是仅仅阅读概念解释，这很有用：

```text
paper
  ↓
equations
  ↓
PyTorch
  ↓
tensor shapes
  ↓
experiment
```

---

### 5. Jay Shah / Raschka 风格的“从零实现”材料

另一个特别有用的类别是**从零实现 LLM 的博客**。

例如，Raschka 的《Build a Large Language Model (From Scratch)》生态系统非常出色，因为它迫使你理解实际计算，而不是将 Transformer 视为黑箱。

[Build a Large Language Model (From Scratch)](https://sebastianraschka.com/books/ml-python/?utm_source=chatgpt.com)

对于从事你这类工作的人来说，我认为这种风格比一般的“AI 教程”更有价值。

---

### 6. 官方研究工程师有时比博客更好

对于**现代架构**，我也会直接阅读原始作者/仓库。

例如，Scientific Spaces 的 Transformer 系列深入探讨了诸如：

```text
MHA
 ↓
MQA / GQA
 ↓
RoPE
 ↓
long-context methods
 ↓
MLA
 ↓
low-rank KV representation
```

苏剑林的 MLA 分析特别有趣，因为他不仅描述 MLA，还尝试从理论上解释*为什么* MLA 有效。([Spaces][3])

对于英语资源，我会将博客与以下内容配对：

```text
DeepSeek 论文
Qwen 技术报告
Meta Llama 论文
Google 研究
Anthropic 研究
OpenAI 研究
```

而不是寻找一个博客来替代 Scientific Spaces。

---

## 针对你的使用场景的个人排名

鉴于你目前正在研究像 **MLA、QK 投影、RoPE、Transformer 演进和模型实现**这样的内容，我推荐使用以下组合：

| 资源                          | 最适合                             | 与 Scientific Spaces 相似度 |
| ----------------------------- | ---------------------------------- | -------------------------: |
| **Sebastian Raschka**         | LLM + 实现 + 架构                  |                        ★★★★★ |
| **Lilian Weng**               | 数学/概念综合                      |                        ★★★★☆ |
| **Aman Arora**                | 代码/实现                          |                        ★★★★☆ |
| **Jay Alammar**               | 视觉直觉                           |                        ★★★☆☆ |
| **原始论文 + 仓库**           | 前沿架构                           |                        ★★★★★ |
| **Hugging Face 博客**         | 实践生态系统                       |                        ★★★☆☆ |

重要的是，**Scientific Spaces 作为个人博客，其研究导向异常强烈**。例如，苏剑林的 Transformer 系列不仅解释 RoPE，还分析正弦位置编码为何如此表现，并进而开发了 RoFormer/RoPE。([Spaces][4])

因此，如果你在寻找具有相同精神的英语资源，我建议从以下开始：

**Raschka → Lilian Weng → 原始论文 → 自己实现。**

而针对你当前的具体主题，我实际上推荐 **Raschka + DeepSeek 论文/仓库**，而不是试图找到一个完美的英语等价物。

参考文献：

* [Scientific Spaces / 苏剑林](https://spaces.ac.cn/?utm_source=chatgpt.com)
* [Sebastian Raschka](https://sebastianraschka.com/?utm_source=chatgpt.com)
* [Lilian Weng](https://lilianweng.github.io/?utm_source=chatgpt.com)
* [Jay Alammar](https://jalammar.github.io/?utm_source=chatgpt.com)
* [Aman Arora](https://amaarora.github.io/?utm_source=chatgpt.com)

[1]: https://sebastianraschka.com/best-articles/?utm_source=chatgpt.com "Best Articles by Topic | Sebastian Raschka, PhD"
[2]: https://sebastianraschka.com/blog/2023/llm-reading-list.html?utm_source=chatgpt.com "Large Language Models Reading List | Sebastian Raschka, PhD"
[3]: https://www.spaces.ac.cn/author/1/8/?utm_source=chatgpt.com "苏剑林 发布的文章 - 科学空间|Scientific Spaces"
[4]: https://www.spaces.ac.cn/author/1/37/?utm_source=chatgpt.com "苏剑林 发布的文章 - 科学空间|Scientific Spaces"
