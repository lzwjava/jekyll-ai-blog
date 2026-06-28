---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于切片的模型评估
translated: true
type: note
---

问题：我已经弄清楚了如何评估一个训练好的模型——按提示长度、编程语言和主题对输入进行分类，然后挑选代表性示例进行轻量级评估。这种通过动手实践、探索性地理解训练/推理/评估的方式，对大脑来说确实是一种愉悦的体验，而且有智能体帮忙运行实验，还有什么难的呢？

回答：

没错——而且你得到的直觉（按输入维度做分层采样）正是严肃的评估框架所形式化的东西。你是通过构建发现的，这是最扎实的方式。让我再深入一层，让这种直觉不断强化。

你所描述的是**基于切片的评估**。核心思想是：单一的聚合分数（困惑度、平均准确率）会隐藏失败模式。你应当将输入分布分解为多个切片，并逐个测量，因为一个模型可能在短英文提示上表现优异，但在长多轮Rust提示上完全崩溃——平均值会掩盖真相。

你选的三个轴都很好。需要内化的是*为什么*每个轴在机制上重要：

- **提示长度** → 测试位置泛化能力以及在超出训练主导长度时的KV缓存/注意力行为。一个主要在短序列上训练的GPT-2规模模型，在超出有效上下文后性能会下降。这正是捕获长度外推失败的地方。
- **编程语言** → 测试分词器效率和训练数据覆盖度。训练表示稀疏的语言分词效果更差（每个语义单元对应更多token），损失更高。这直接反映了你的数据集构成。
- **主题** → 测试领域覆盖度，你会在这里看到知识缺口的“长尾”。

你的描述缺少的是：**每个切片的一个评分函数**。“挑选一些示例”给了你输入；你仍然需要一个指标。对于基础语言模型，按构建成本排序的选项如下：

```python
# 最便宜，无需标签：每个切片的损失/困惑度
import torch, torch.nn.functional as F

@torch.no_grad()
def slice_perplexity(model, tokenizer, prompts, device="cuda"):
    losses = []
    for p in prompts:
        ids = tokenizer.encode(p, return_tensors="pt").to(device)
        logits = model(ids).logits
        # 偏移：从 tokens <t 预测 token t
        loss = F.cross_entropy(
            logits[:, :-1].reshape(-1, logits.size(-1)),
            ids[:, 1:].reshape(-1),
        )
        losses.append(loss.item())
    mean = sum(losses) / len(losses)
    return {"ppl": float(torch.exp(torch.tensor(mean))), "n": len(prompts)}

slices = {
    "short_python":  [...],
    "long_python":   [...],
    "short_rust":    [...],
    "long_prose_en": [...],
}
report = {name: slice_perplexity(model, tok, ps) for name, ps in slices.items()}
```

困惑度是免费的（不需要标签），而且能捕获很多问题。但它测量的是*下一个token的惊讶程度*，而不是*任务成功率*。对于代码而言，黄金标准的评估是**功能正确性**，而不是损失——即pass@k（在可执行测试上的成绩，如HumanEval风格），因为一个模型可以有很低的损失，但仍然生成无法运行的代码。

```python
# pass@1 草图：生成，针对测试执行，统计通过次数
def pass_at_1(model, problems):  # problems: [{"prompt", "test", "entry_point"}]
    passed = 0
    for prob in problems:
        code = generate(model, prob["prompt"])          # 你的采样函数
        ns = {}
        try:
            exec(code + "\n" + prob["test"], ns)         # 实际中应在沙箱中运行
            ns["check"](ns[prob["entry_point"]])
            passed += 1
        except Exception:
            pass
    return passed / len(problems)
```

将玩具级评估与可信评估区分开来的三个原则：

1. **锁定评估集并做好版本管理。** 一旦你的评估集发生漂移，不同检查点之间的分数就无法比较。对于追踪训练进度，一个固定的200示例集比一个全新但含2000示例的集更好。
2. **注意污染问题。** 如果评估提示泄露到了训练数据中，你的数字就是虚构的。在nanoGPT规模的数据集上，你可以控制这一点；保留一个从未参与训练而独立持有的测试集。
3. **采样设置也是评估的一部分。** 温度0与0.8下的pass@k是不同的度量。固定温度、top-p和最大token数，否则你测量的只是噪声。

关于“有智能体，没什么难的”这种感觉——基本正确，这种乐趣是真实的。但有一点需要注意：智能体让*生成*评估变得廉价，但也容易让你*不注意到评估本身出了问题*。困难从来不是运行实验，而是信任这个数字。如果测试框架悄悄地吞噬了异常，那么一个绿色的pass@1为0.9就毫无意义。因此，真正能产生复利的自律不是“运行更多实验”，而是“对每个指标保持怀疑，直到我看到它按照物理规律应当的方向变化”（例如，随着训练进行损失必然下降；在受污染数据上的pass@k是个危险信号，而不是胜利）。

你已经掌握了正确的循环。加上评分函数，冻结评估集，并且用检查模型输出时同样的怀疑态度来对待你的评估框架。