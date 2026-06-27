---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LoRA微调的反常识真相
translated: true
type: note
---

问题：关于使用LoRA低成本重新微调冻结的开放基础模型，有哪些非主流或反共识的观点？

答案：

以下是经得起推敲的反共识观点，大致按与主流共识的背离程度排序。

**1. LoRA不仅仅是"学得少"——它学得*不一样*，而这种差异往往是一种降级。**

流行的说法是"LoRA ≈ 全参数微调，更便宜，但效果略差"。来自*入侵维度*研究（Shuttleworth等人，2024）的更尖锐观点是结构性的：LoRA在权重矩阵中引入了全参数微调解中不存在的高秩奇异向量。在分布内任务准确率相同，但谱结构不同，这些入侵维度与更差的分布外泛化能力和对预训练分布的更多遗忘相关。因此，"LoRA在我的评估中匹配了全参数微调"可能隐藏了你构建了一个更脆弱的模型这一事实。

**2. 在真正的领域自适应场景中，"冻结基座+适配器"是虚假的经济学。**

LoRA是参数高效的，而非*知识*高效的。对注意力/MLP投影进行低秩更新可以重新调整输出风格，并以低成本教授格式/任务，但它是注入真正*新*知识或大幅偏移基础分布的糟糕载体。"Tale of Tails"/持续预训练文献和LIMA风格的观察都指向同一方向：如果你需要新事实或不同的领域先验，你需要全参数微调或持续预训练，而不是一个秩为16的补丁。LoRA擅长*行为*，但在*知识*方面表现不佳。

```python
# 诚实的决策规则
def should_use_lora(task):
    if task in ("format", "style", "tone", "task-following", "persona"):
        return True              # LoRA的强项
    if task in ("new domain knowledge", "new language", "factual recall"):
        return False             # 全参数微调/持续预训练
    if task == "reasoning/math hard skill acquisition":
        return "maybe — rank matters, often disappointing"
```

**3. 秩大多是障眼法；*适配哪些模块*要重要得多。**

大众智慧痴迷于`r`。实证上（QLoRA消融实验、原始LoRA论文本身仅限注意力的选择），从r=8到r=64的收益快速递减，而*将LoRA应用于包括MLP在内的所有线性层*相比仅应用于注意力层，是一个更大的杠杆。反共识的结论是：大多数人调错了旋钮。在考虑提高秩之前，先以低秩适配所有层（`q,k,v,o,gate,up,down`）。

**4. QLoRA的量化基座是一个人们假装不存在的隐性精度税。**

QLoRA通过在4位NF4冻结基座上训练适配器，让LoRA*感觉*免费。反量化推理的故事很干净，但你正在针对有损基座优化适配器，合并/服务的模型继承了这一点。对敏感任务来说，差距是真实存在的——只是通常低于弱评估的噪音水平。"QLoRA = 1/4内存下的LoRA质量"是营销话术，而非衡量的等价性。

**5. 将LoRA合并回基座是有损的，而且往往毫无意义。**

`W' = W + BA` 是精确算术，但LoRA的*魅力*——可交换适配器、多租户服务（S-LoRA）、可组合性——在合并的瞬间就消失了。而且合并多个LoRA在任何原则性意义上都不是可加的；适配器之间的干扰是一种已知的失败模式。反共识立场：如果你打算合并并服务一个模型，你就已经丢掉了LoRA唯一的结构性优势，应该直接做全参数微调（或者纯粹将合并作为部署便利，知道这是单向门）。

**6. LoRA的超参数敏感性被低估，且很少被报告。**

α/r缩放、学习率（LoRA需要比全参数微调高约10倍的学习率）和初始化三者之间的交互非平凡。论文报告的是获胜配置；实践者发现LoRA要达到全参数微调的同等水平，比其"开箱即用"的名声要*更*难调优。rsLoRA（秩稳定缩放）的存在正是因为朴素的α/r缩放在高秩时会失效——这证明默认配方在悄无声息地出错。

```python
# 人们复制但通常次优的默认值：
LoraConfig(r=8, lora_alpha=16)   # alpha/r=2 缩放 — 低秩时没问题，
                                  # 随秩增长退化 → 使用rsLoRA
# 实践上：LoRA学习率约1e-4到3e-4，而不是全参数微调用的1e-5/2e-5
```

**7. "1000次廉价实验"的承诺是真实的，但会制造评估债务。**

LoRA真正的优势是迭代速度——你可以为一次全参数微调的成本运行50个适配器变体。但用相同的弱评估进行廉价训练只会让你更快地过拟合到评估上。瓶颈悄然从计算转移到评估质量，而大多数LoRA管道从未升级评估以匹配。成本并没有消失；它转移到了你未衡量的地方。

**8. 对于非常小的模型，LoRA的合理性部分崩塌。**

整个卖点是"基座庞大且全参数微调昂贵"。在nanoGPT/124M–760M规模、MI300X 192GB内存上，你可以轻松地进行全参数微调。那里的LoRA大多是盲目照搬——你支付了入侵维度/容量代价来节省你过剩的内存。将LoRA保留在全参数微调真正无法容纳的规模（7B+在4070上），而你的GPT-2 760M实验直接做全参数微调。

总结：LoRA是一个*行为重新风格化*工具，带有*知识注入*天花板、*量化*税、*谱*副作用，以及合并时放弃的*服务*优势。将其视为"免费的全参数微调"是普遍错误；将其视为"廉价的格式/任务适配，全参数微调用于知识"才是校准的立场。

参考文献：

- [LoRA vs Full Fine-tuning: An Illusion of Equivalence (intruder dimensions)](https://arxiv.org/abs/2410.21228)
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314)
- [A Rank Stabilization Scaling Factor for Fine-Tuning with LoRA (rsLoRA)](https://arxiv.org/abs/2312.03732)
- [S-LoRA: Serving Thousands of Concurrent LoRA Adapters](https://arxiv.org/abs/2311.03285)
- [LoRA Learns Less and Forgets Less](https://arxiv.org/abs/2405.09673)