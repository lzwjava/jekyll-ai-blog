---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenAI千年奖归属争议
translated: true
type: note
---

问题：**OpenAI 最近在千禧年数学问题上的突破背后有什么故事？OpenAI 是在“窃取功劳”吗？**

答案：

是的——**确实存在功劳/独立性的争议**，但更准确的说法是 **“可能使用了未发表的研究 / 存在有问题的研究伦理”**，而非“OpenAI 明确窃取了证明”。

### 1. OpenAI 的声称

OpenAI 于 2026 年 9 月 8 日宣布，其内部 AI 系统给出了 **纳维-斯托克斯存在性与光滑性问题** 的解法，这是七个千禧年问题之一。

据称该系统：

* 使用了约 **10,000 个 AI 智能体**
* 运行了约 **88 小时**
* 消耗了 **数百万美元的算力**
* 生成了约 **165 页的数学论证**
* 另有 AI 系统将部分论证形式化/检查

核心声称大致是：**三维纳维-斯托克斯方程在相关公式下可以产生有限时间奇点**。如果数学上正确，这将是一个巨大的成果。（《卫报》[1]）

但重要区别在于：

> **OpenAI 说“我们解决了” ≠ 数学家们接受千禧年问题已被解决。**

该证明仍需经过严格的独立数学审查。（《华盛顿邮报》[2]）

---

### 2. 为什么人们对功劳归属感到愤怒

这是有趣的部分。

已有两位研究人员正在研究该问题：

* **Tristan Buckmaster**，纽约大学数学家
* **Levent Alpöge**，与 Anthropic 相关的数学家/研究员

他们此前一直使用包括 **Claude、Codex 和 Astra** 在内的 AI 系统进行研究。

他们似乎已取得实质性进展，并准备发表。

随后 OpenAI 通过传言得知，研究人员在千禧年问题上取得了进展。

OpenAI 声称其开始认真攻击纳维-斯托克斯问题的时间大约是 **9 月 1 日**。

Buckmaster 声称，他们未发表工作的信息传到了 OpenAI，之后 OpenAI 迅速启动了一项大规模的算力行动并产生了自己的结果。（TechCrunch [3]）

因此可疑的时间线大致如下：

```text
Buckmaster + Alpöge
        │
        │ 未发表的研究
        ▼
  借助 AI 的工作
        │
        │ 信息传到了 OpenAI？
        ▼
     OpenAI 得知
   “他们可能已经解决了”
        │
        ▼
  10,000 智能体集群
        │
        │ ~88 小时
        ▼
 OpenAI 自己的证明
```

这就是为什么人们在问：

> **OpenAI 是独立解决了问题，还是从别人的私人研究中发现了方向，然后用多得多的算力抢先发表？**

---

### 3. 尤其令人不安的部分：Codex

这是故事变得更加严重的地方。

Buckmaster 和 Alpöge 在将 Codex 用作研究工具时，显然将部分 **未发表的数学工作放入了 OpenAI 的 Codex**。

因此 Buckmaster 担心 OpenAI 可能通过自己的产品了解到他们研究的一些内容。

OpenAI 表示 **没有为了解决问题而访问他们的特定私人用户数据**。

但 OpenAI 据称也承认了一个更为微妙的事实：

> **无法完全排除**，其产品使用中的去标识化数据间接促进了模型改进。（Axios [4]）

这是一个重要的区别。

存在两种截然不同的指控：

```text
A. “OpenAI 的工程师打开了 Buckmaster 的私人 Codex 会话并复制了证明。”

       ↓

    OpenAI 说：没有。


B. “Buckmaster 与 OpenAI 产品的互动可能间接影响了 OpenAI 随后使用的模型。”

       ↓

    OpenAI 说：无法完全排除这种情况。
```

目前 **没有确凿证据表明 OpenAI 直接复制了他的证明**。

---

### 4. 还有另一个功劳归属争议

显然还存在关于 **Alpöge**（他与 Anthropic 合作）是否应获得认可的紧张关系。

Buckmaster 声称，OpenAI 研究员 Sébastien Bubeck 因 Alpöge 与 Anthropic 的关系而反对给予其功劳。

这尤其尴尬，因为这不仅仅是：

> “AI vs 人类”。

而是：

> **OpenAI vs Anthropic + 学术研究者 + 未发表科学思想的所有权。**

TechCrunch 报道了 Buckmaster 对此争议的陈述，而 OpenAI 则否认其成果依赖于他们工作的更广泛推论。（TechCrunch [3]）

---

### 5. 这真的是“窃取”吗？

我将区分 **三个层面**：

| 情况 | 我的评估 |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| OpenAI 在听到有人接近解决的消息后独立发现了证明 | **不是窃取** |
| OpenAI 从公开信息中了解了一般的科研方向并独立解决了问题 | **激进的竞争，但合理** |
| OpenAI 未经许可或未给予认可，利用用户的未发表私人研究来指导自己的研究 | **严重的研究伦理问题** |
| OpenAI 直接复制了他们的证明并作为自己的成果发表 | **学术剽窃** |

目前，公开可获得的证据 **确认了争议存在**，但 **并非最强版本的剽窃指控**。

《自然》杂志也报道称，OpenAI 在听到 Buckmaster 和 Alpöge 取得进展的传言后，明确启动了这一努力。（《自然》[5]）

---

### 6. 但这里有更深层次的问题

我认为最有趣的其实不是 100 万美元的奖金。

而是这个：

**当你使用的 AI 研究助手的提供商也同时有能力与你竞争时，会发生什么？**

想象你是一位数学家：

```python
research = """
这是我未发表的证明思路。
我认为引理 7 可能解决纳维-斯托克斯问题。
"""

codex(research)
```

历史上，你担心的是：

```text
导师
竞争者
会议
期刊
审稿人
```

有了前沿 AI，你现在多了一个实体：

```text
        你的研究
             │
             ▼
        AI 助手
             │
      ┌──────┴──────┐
      ▼             ▼
  帮助你        改进模型
                    │
                    ▼
              AI 公司
                    │
                    ▼
              竞争实验室
```

这创建了一种 **结构性的利益冲突**，在传统的数学软件中并不存在。

Axios 基本上指出了这一点：这一事件引发了一个问题，即前沿实验室能否与使用其产品的科学家竞争。（Axios [4]）

---

### 7. 还有一个更大的 AI 启示

这一事件展示了 **AI 研究经济学** 的一个重要方面。

Buckmaster 的团队可能拥有：

```text
2 名研究人员
+ Claude/Codex
+ 数学洞察力
```

OpenAI 可以用以下方式回应：

```text
10,000 个智能体
+ 巨大的推理预算
+ 大规模并行搜索
+ 专门的验证
+ 前沿模型
```

因此科学竞争可能日益变为：

$$
\text{研究能力}
=
\text{人类洞察力}
\times
\text{模型能力}
\times
\text{算力}
\times
\text{智能体并行度}
$$

而 **算力成为科学优先权竞争中的一种竞争武器**。

对于像你这样构建智能体的人来说，这可能是这里最重要的故事。

此外，OpenAI 表示 **不打算领取 100 万美元的 Clay 奖**，这使得争议主要围绕 **科学优先权和功劳归属**，而非金钱本身。（《华盛顿邮报》[2]）

[《自然》杂志关于突破的报道](https://www.nature.com/articles/d41586-026-02842-5?utm_source=chatgpt.com)

[TechCrunch 关于功劳争议的叙述](https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/?utm_source=chatgpt.com)

我还可以从偏微分方程层面而非新闻报道层面，分解 **实际的纳维-斯托克斯数学声称以及 AI 据称证明了什么**。

[1]: https://www.theguardian.com/science/2026/sep/08/openai-claims-to-have-solved-maths-problem-that-stumped-humans-for-decades?utm_source=chatgpt.com "OpenAI claims to have solved maths problem that stumped humans for decades"
[2]: https://www.washingtonpost.com/technology/2026/09/09/openai-claims-it-solved-elusive-math-problem-with-1-million-prize/?utm_source=chatgpt.com "OpenAI claims it solved elusive math problem with a $1 million prize - The Washington Post"
[3]: https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/?utm_source=chatgpt.com "OpenAI fought dirty on career-making math problem, says NYU mathematician | TechCrunch"
[4]: https://www.axios.com/2026/09/08/openai-math-solution-navier-stokes-credit?utm_source=chatgpt.com "OpenAI's historic math solution overshadowed by credit controversy"
[5]: https://www.nature.com/articles/d41586-026-02842-5?utm_source=chatgpt.com "OpenAI claims huge maths breakthrough on a famed ‘Millennium Problem’ | Nature"
