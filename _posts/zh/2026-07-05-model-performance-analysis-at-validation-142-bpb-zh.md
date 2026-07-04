---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 验证1.42 BPB下的模型性能分析
translated: true
type: note
---

完成。结果保存至 `/mnt/data/zz/fineweb-code-sec-gpt/results.txt`。快速总结：

**观察 — d12（第 50000 步，val_bpb 1.418）**

| 领域 | 质量 |
| --- | --- |
| **代码（快速排序续写）** | 良好 — 正确续写了 `quicksort`，生成了 `sort_2`、`sort_n` 等变体，代码结构真实 |
| **代码（React DataFetcher）** | 尚可 — 忠实复现了组件，生成了一个复用相同模式的 `fetch(url)` 函数 |
| **代码（Go/归并排序/SQL）** | 较弱 — 退化为重复提示，幻觉列名（`price_delivered`、`customer_id_delivered`），没有真正的 Go 代码 |
| **SEC（收入、风险）** | 读起来合理 — 以连贯的财务语气续写 SEC 文本，生成了 `Item 1B` 标题 |
| **SEC（IFRS/GAAP）** | 崩溃 — 退化到数字重复（`15,200, 172, 200`）和胡言乱语 |
| **通用（水循环）** | 良好续写 — 正确添加了“水循环始终是最常见的”，并就蒸发状态进行了连贯推理 |
| **通用（复利）** | 较弱 — 出现了 `$10,000 / 30 = 75%` 的荒谬算术 |
| **通用（自主神经系统、光合作用）** | 幻觉 — 出现“photometry phototechnique”，以及“pitty”作为神经系统的一个分支 |

**结论：** 在 1.42 val_bpb 下，模型已学会了代码语法结构（缩进、函数定义、React hook）和 SEC 文档语气，但缺乏事实知识和算术推理能力。这对于 286M 参数模型而言是典型的——记忆能力有限。代码续写任务表现最佳，因为这类任务依赖于语法模式匹配，而非事实回忆。
