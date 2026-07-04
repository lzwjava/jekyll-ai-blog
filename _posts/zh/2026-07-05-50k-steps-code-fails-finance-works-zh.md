---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 5万步：代码失败，金融可行
translated: true
type: note
---

## 结果评估：d12 步骤 50K, 温度=0.8

**训练曲线（各检查点的 val_bpb）**：

```
step  5000: 1.6798  train_loss=1.3968
step 10000: 1.6399  train_loss=1.3723
step 15000: 1.6256  train_loss=1.4654
step 20000: 1.5952  train_loss=1.3630
step 25000: 1.5680  train_loss=1.1359
step 30000: 1.5363  train_loss=1.1988
step 35000: 1.5101  train_loss=1.2288
step 40000: 1.4683  train_loss=1.1691
step 45000: 1.4463  train_loss=1.0767
step 50000: 1.4176  train_loss=1.0616
```

曲线在 50K 步时仍在下降（未出现平台期），因此模型尚未收敛。已处理的 tokens：50K * 65,536 = 约 3.3B。

### 按领域分类的定性分析

**代码提示——全部失败**

| 提示 | 结果 |
| -------- | ------------- |
| **code_go** | 逐字重复提示中的约束条件（"客户端应优雅地处理 SIGINT..."），然后偏题到无关的 `os.environ['PORT']` 配置模板。从未生成一行 Go 代码。 |
| **code_python** | 将提示回显："该函数不接受任何额外参数。要向列表添加新值，必须让函数返回一个列表。" 零代码生成。 |
| **code_quicksort** | 这是**最好**的代码输出。生成了一个在语法上有效的快速排序，但有一个 bug：`return quicksort(left) + middle + quicksort(right) - 1`（其中的 `- 1` 是错误的）。然后虚构了 `sort_2`、`sort_3`、...、`sort_5`，这些函数都调用了 `arr.sort(quicksort)`——语法有效但语义错误（将函数作为 key 传递）。模型学会了*代码形状*，但没有学会*代码语义*。 |
| **code_react** | 从一个合法的 DataFetcher 组件开始（可能从训练数据中记忆而来），然后定义了 `fetch()` 作为一个 React 组件（覆盖了浏览器 API），接着进入一个自我引用的循环，复制相同的组件结构。 |
| **code_sql** | 直接列出原始列名，而不是编写 GROUP BY 聚合。生成了 `WHERE id = 1 ORDER BY name`——没有 SUM，没有 COUNT，没有 top-5。 |

**通用知识提示——语词混乱**

所有四个（自主性、复利、光合作用、水）都遵循相同的模式：在前约 40 个 token 中忠实地复现提示，然后经历**语义崩溃**：

- "fight-or-flight response" → "the warm, as opposed to the pitty"
- "photosynthesis" → "photometry phototechnique" / "the following photographs"
- "compound interest" → 只是将提示文本重复作为自己的输出
- "oceans, lakes, and rivers" → "the continuous oceans, not the flows over land"

模型通过表层共现关系关联单词，而非含义。"Photosynthesis" → "photo" → "photographs"。 "Autonomic" → "automatic system" → "pitty" (??)。这是一个学习了 token 级统计信息但未形成用于概念推理的适当潜在表征的模型的典型特征。

**SEC/金融提示——唯一的亮点**

| 提示 | 评估 |
| -------- | ----------- |
| **sec_revenue** | **真正可信**。80 token 的输出连贯地延续了财务叙事："有效增长率为 5.42%，去年同期为 470 万美元。" 200 token 版本生成了完整的收入分析第二段，数字看起来合理。这是唯一一个输出可以让随意读者误以为是人类所写的领域。 |
| **sec_risk** | 开头正常地复制提示，然后执着于 "ecosystem" 并重复了 12 次以上。200 token 版本虚构了 "Item 1B. Sustainable Risks"——一个虚构的 SEC 章节标题。 |
| **sec_financial_analysis** | 退化为 "Sinh-Deutschmans algorithm"（无意义）以及 "1.8, 1.5, 1.6" 的列表——模型抓住了比率数字并不断生成它们。 |
| **sec_ifrs** | 引用了 "APLT"（幻觉），然后是 "15,200, 172, 200"——从表面模式匹配中抓取的数字。没有实际的 IFRS/GAAP 分析。 |

### 根本原因

在 32K 词汇表条件下，val_bpb 为 1.42，模型的字节级困惑度约为 2^1.42 ≈ 2.68。这意味着在每个字节位置上，模型的不确定性大致相当于在 3 个可能性中挑选。对于代码生成（高熵、需要精确语法），这是致命的——即使一个错误的 token 也会破坏程序。而对于像 SEC 收入申报（低熵模板）这类公式化文本，它之所以有效，是因为下一个 token 严重受到附近上下文的约束。

模型已经学习到了局部 n-gram 模式，足以模仿财务报告的外形，但缺乏全局一致性来生成正确的代码或推理概念。它的行为类似于一个高阶字符级马尔可夫模型——擅长局部模式补全，但零理解能力。

### 哪些措施会有帮助

- **更多训练步数**：曲线在 50K 仍下降。运行到 100K+ 会将 val_bpb 降至约 1.3，这将减少垃圾输出的尾部。
- **更大的模型**：d12 (768 维) 是 GPT-2 Small 规模。d24 (1536 维) 会有更大的容量从相同数据中内化代码和概念的结构。
- **更低的温度**：0.8 对于采样来说相当高。在 0.4-0.5 时，模型会更贴近学习到的分布，产生更少的幻觉（但多样性也会减少）。code_quicksort 和 sec_revenue 的输出可能会更加严谨。
- **val_bpb 为 1.42 需要达到约 1.0-1.1 才能实现可靠的代码生成**——这是模型拥有足够的比特数来满足语法约束的阈值。
