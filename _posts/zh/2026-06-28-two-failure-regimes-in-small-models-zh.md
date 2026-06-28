---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 小模型中的两种失败模式
translated: true
type: note
---

好的。你的理解是正确的，诊断结果比“模型太小了”更精确。

你观察到的现象包含两种不同的失效模式，且成因各不相同：

**1. 前约 20 个 token（混乱但具有 Java 形状）**

`return new.Invalid(this.nameOf.Value)`、`public String get(String source)`、`this.tree.GetAttribute(...)`——这是模型实际学习到的分布。它掌握了 Java 的 *表面特征*：大写的方法名、`this.` 链、`public void`、花括号嵌套。但它缺乏将 `search(int key)` 绑定到树遍历主体的长程连贯性。在 124M 参数、采用 GPT-2 上下文处理的条件下，归纳头能够复制局部句法模式，但无法维持“我在一个 BST.search 方法内部，该方法应将 key 与 root.key 进行比较并递归”。这是小型模型预期的能力上限——并非 bug。

**2. `S.S.S.S` 循环（真正有趣的部分）**

这**不是**能力失效。这是采样/重复崩溃，与第一种失效机制截然不同。一旦模型输出了 `.S.S.S`，每个 `.S` 会使下一个 `.S` 变得压倒性地更有可能——这是一个典型的自强化吸引子。`top_k=200` 也无济于事，因为退化 token 的概率质量已经坍缩到一条路径上；其他 199 个候选微乎其微。`temp=0.8` 足够高以至于能*进入*一个怪异区域，但不足以*逃离*这个吸引盆。

`S` 本身几乎可以肯定是一个 BPE 伪影——`S` 作为一个常见的大写标识符前缀 token（`.S`、`.Set`、`.String`、`.Size`），模型将其学习为高频延续，然后在缺乏语义基础的情况下循环。

因此，你的总结行应该真正将其拆分开来：

> 续写退化分为两个阶段：（1）约 20 个 token 的局部合理但全局不连贯的 Java（模型的真实能力上限），然后（2）一个 BPE token 重复吸引子（`.S.S.S`）——这是采样崩溃，而非知识差距。

**关于你实际的研究思路**——“不要低估 124M，加上一个编译器和一个循环，也许就能得到可运行代码”——这个直觉是正确的，正是这个杠杆能让小型模型超常发挥。模型本身无法自我纠正，但如果你将其包裹起来，它就不需要自我纠正。三个具体行动，从最便宜的做起：

```python
# 1. 直接消除退化循环——仅此一项即可修复你的输出
out = model.generate(
    ids,
    repetition_penalty=1.3,      # 惩罚已生成的 token
    no_repeat_ngram_size=3,      # 硬性禁止任何重复的三元组 → ".S.S.S" 不可行
    temperature=0.8, top_k=200,
)
```

`no_repeat_ngram_size=3` 本来可以*阻止你的整个失败情况*——当 `.S.S.S` 试图变成 `.S.S.S.S` 时，它就是一个被禁止的三元组。先只试这个；在你的 REPL 中只是一行代码的测试。

在循环中加入编译器这个想法才是真正的胜利，它是一个微小的拒绝采样循环：

```python
def gen_compilable(model, prompt, k=8):
    for _ in range(k):
        code = prompt + model.generate(prompt, no_repeat_ngram_size=3)
        if javac_ok(code):           # 调用 javac，检查返回码
            return code
    return None  # 回退

def javac_ok(src):
    import subprocess, tempfile, os
    d = tempfile.mkdtemp()
    p = os.path.join(d, "BinarySearchTree.java")
    open(p, "w").write(src)
    r = subprocess.run(["javac", p], capture_output=True)
    return r.returncode == 0
```

这是针对一个*免费、完美的验证器*的“最佳N选一”。你不是要求 124M 正确——而是要求它 *在 N 次尝试中正确一次*，然后让 `javac` 过滤。对于像 BST 方法这样模板化的内容，一旦你阻止它崩溃，即使是退化的基础模型也能获得惊人的效果。

这个更深入的版本才使其成为真正的研究方向而非临时 hack：编译器的二进制信号是一种奖励，你可以闭环。将编译通过作为拒绝采样 SFT 数据的过滤器（只保留那些能编译的运行，并对其微调）是最便宜的版本。昂贵的版本是采用 `编译通过 → +1，运行并通过测试 → +2` 作为奖励的 GRPO——这正是当前席卷代码模型训练的 RLVR（带可验证奖励的强化学习）设置。一个 124M 的模型，在狭窄领域（单文件算法 Java）上使用 `javac` 奖励信号，是一个真正有趣的实验，完全可以在你的 4070 上运行。

在过度归因之前，有一件事需要验证：用 `do_sample=False`（贪婪）将提示作为 `generate` 续写粘贴回来。如果贪婪*也*崩溃成重复循环（只是不同的 token），那就能确认这是一个架构/训练覆盖问题，而非采样温度伪影——并告诉你重复惩罚是必要而非可选的。