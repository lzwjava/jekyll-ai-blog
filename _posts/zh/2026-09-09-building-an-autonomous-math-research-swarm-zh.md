---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建自主数学研究群体
translated: true
type: note
---

问题：**如何构建你自己的OpenAI式自主数学/研究集群？Karpathy的`autoresearch`是正确的起点吗？**

答案：**是的——但`autoresearch`是正确的*模式*，而非完整的框架。** 对于你的目标，我会围绕它构建一个小型的**ResearchOS**，而不是直接采用一个重量级的智能体框架。

Karpathy的`autoresearch`已经包含了核心循环：智能体修改研究程序，运行一个固定预算的实验，衡量结果，保留或回退更改，然后重复。([GitHub][1])

对于数学研究，将目标从：

```text
修改 train.py
        ↓
5分钟训练
        ↓
val_bpb
        ↓
保留 / 丢弃
```

改为：

```text
猜想 / 问题
        ↓
生成想法
        ↓
实现证明 / 实验
        ↓
形式验证器 / 数值验证器
        ↓
批评智能体
        ↓
评分
        ↓
保留有前景的分支
        ↓
迭代
```

### 1. 我不会从LangGraph / CrewAI开始

对你来说，我会使用：

```text
Python
  +
asyncio
  +
git worktrees
  +
Claude Code / Codex / Gemini CLI
  +
Lean
  +
SQLite
  +
Docker
```

这足够了。

你实际上并不需要一个“智能体框架”。

重要的抽象是**研究循环**。

```python
while budget_left():

    problem = db.get_problem()

    ideas = parallel([
        researcher(problem),
        researcher(problem),
        researcher(problem),
        researcher(problem),
    ])

    candidates = parallel([
        solver(problem, idea)
        for idea in ideas
    ])

    verified = parallel([
        verify(candidate)
        for candidate in candidates
    ])

    critiques = parallel([
        critic(candidate)
        for candidate in verified
    ])

    score = evaluate(verified, critiques)

    if score > threshold:
        db.commit(candidate)
```

这基本上就是从它出发可以构建10,000个智能体系统的原始基础。

---

## 2. 关键在于**验证**，而不是智能体的数量

这是从当前OpenAI故事中得到的最大教训。

你不希望：

```text
1000个智能体
    ↓
1000条意见
    ↓
LLM说“看起来正确”
```

你希望：

```text
             ┌── 智能体 A ──┐
             ├── 智能体 B ──┤
问题 ────►├── 智能体 C ──┤
             └── 智能体 D ──┘
                    │
                    ▼
             候选证明
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Lean       符号化       数值
     验证器      验证器       验证器
        │           │           │
        └───────────┼───────────┘
                    ▼
                 批评者
                    │
                    ▼
              研究数据库
```

对于严肃的数学，**确定性验证器就是你的奖励模型**。

Lean在这里特别有趣，因为你可以将最终标准设为：

```text
Lean是否接受这个定理？
```

而不是：

```text
GPT是否认为证明看起来令人信服？
```

据称当前的OpenAI报告本身就包含了Lean形式化，这正是我会采取的方向。([华尔街日报][2])

---

# 3. 你的第一个版本应该很小

不要一开始就尝试Navier–Stokes。

构建类似这样的东西：

```text
research/
├── problem.md
├── program.md
├── agents/
│   ├── researcher.py
│   ├── solver.py
│   ├── critic.py
│   └── verifier.py
├── experiments/
├── proofs/
├── memory/
├── db.sqlite
└── orchestrator.py
```

`problem.md`：

```markdown
# 问题

证明：

对于所有 n >= 1，
1 + 2 + ... + n = n(n+1)/2。

要求：

- 生成 Lean 证明
- 不含 `sorry`
- 最小化证明复杂度
```

然后：

```bash
python orchestrator.py
```

智能体 1：

```text
尝试归纳法
```

智能体 2：

```text
尝试代数恒等式
```

智能体 3：

```text
搜索现有引理
```

智能体 4：

```text
尝试直接 Lean 证明
```

然后由 Lean 决定。

---

# 4. 然后将搜索树变得巨大

有趣的架构变为：

```text
                         问题
                            │
                 ┌──────────┼──────────┐
                 ▼          ▼          ▼
              策略       策略       策略
                 │          │          │
             ┌───┴───┐  ┌──┴───┐  ┌───┴───┐
             ▼       ▼  ▼      ▼  ▼       ▼
           证明    证明     证明       证明
             │       │        │           │
             └───────┴────────┴───────────┘
                         │
                         ▼
                      验证器
                         │
                  ┌──────┴──────┐
                  ▼             ▼
                失败          通过
                  │             │
                  ▼             ▼
               批评者        形式化
                  │             │
                  └──────┬──────┘
                         ▼
                       记忆
```

现在你有了**蒙特卡洛树搜索式的数学思想探索**。

这比传统的多智能体框架有趣得多。

---

# 5. `autoresearch` 的位置

我真的会借鉴Karpathy的设计哲学。

原始项目有着极其简洁的接口：

```text
prepare.py
train.py
program.md
```

智能体修改实验、运行它、衡量结果，并从结果中学习。([GitHub][1])

对于你的数学版本：

```text
problem.md
research.py
program.md
verify.py
```

其中：

```text
problem.md
    ↓
program.md
    ↓
智能体
    ↓
research.py
    ↓
Lean / Python / Mathematica
    ↓
评分
```

美妙之处在于**`program.md` 成为了你的研究组织方式**。

你可以告诉智能体：

```markdown
你是首席数学家。

不要仅仅生成证明。

对于每一次失败的尝试：

1. 识别确切的障碍
2. 将其记录到记忆中
3. 生成3种替代策略
4. 避免重复失败的策略
5. 优先选择有独立数学依据的想法

只有当Lean验证通过时，证明才会被接受。
```

这本质上是可执行的研究方法论。

---

# 6. 然后添加特化的智能体

不要让每个智能体都相同。

我会创建：

```text
                    协调器
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
    探索者            数学家             图书管理员
       │                 │                  │
       ▼                 ▼                  ▼
 生成想法          构造证明            搜索论文
       │                 │                  │
       └─────────────────┼──────────────────┘
                         ▼
                      批评者
                         │
                         ▼
                    形式化器
                         │
                         ▼
                      Lean
```

之后：

```text
探索者
求解器
反例猎手
文献智能体
形式化智能体
证明批评者
数值实验者
元研究者
```

**反例猎手**尤其重要。

不要问：

> “你能证明这个吗？”

而是问另一个模型：

> “假设这个定理是假的。找到最小的反例。”

这是一个极其强大的对抗循环。

---

# 7. 记忆变得关键

不要仅仅把对话转储到向量数据库中。

我会维护结构化的研究状态：

```sql
CREATE TABLE experiments (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    strategy TEXT,
    hypothesis TEXT,
    result TEXT,
    score REAL,
    status TEXT
);

CREATE TABLE failures (
    strategy TEXT,
    obstruction TEXT,
    evidence TEXT
);

CREATE TABLE discoveries (
    statement TEXT,
    proof TEXT,
    confidence REAL
);
```

然后智能体可以查询：

```python
failures = db.search_failures(
    current_strategy
)
```

这样可以防止：

```text
智能体 #37：
“我有一个绝妙的想法！”

智能体 #12 在400次迭代前就已经尝试过了。
```

---

# 8. 扩展到1000个智能体

一旦单智能体循环工作起来，**不要重写架构**。

只需：

```python
tasks = [
    ResearchTask(problem, seed=i)
    for i in range(1000)
]

await asyncio.gather(
    *(run_agent(t) for t in tasks)
)
```

但使用不同的搜索分布：

```python
temperature = {
    "conservative": 0.2,
    "normal":       0.7,
    "creative":     1.2,
    "crazy":        1.8,
}
```

然后也许：

```text
700个利用型智能体
200个探索型智能体
50个批评者
50个形式化者
```

初始时具体数字并不重要。

**搜索轨迹的多样性才是关键。**

---

# 9. 你的GPU在这里确实有用

并非每个角色都需要前沿API模型。

例如：

```text
                         协调器
                              │
                   前沿模型 API
                              │
          ┌───────────────────┼──────────────────┐
          ▼                   ▼                  ▼
       规划               批评               综合
          │                   │                  │
          └───────────────────┼──────────────────┘
                              ▼
                       本地模型
                              │
                    RTX 4070 / 云GPU
                              │
                   廉价的并行智能体
```

使用昂贵模型用于：

```text
研究方向
证明策略
最终综合
```

使用廉价/本地模型用于：

```text
证明变异
引理搜索
反例生成
代码编辑
常规批评
```

这更接近你如何经济地构建一个真正的研究集群。

---

# 10. 是的：从Karpathy的`autoresearch`开始

我会分阶段进行：

```text
阶段 1
-------
karpathy/autoresearch
        ↓
理解自主实验循环


阶段 2
-------
autoresearch
        +
Lean
        ↓
自主定理证明


阶段 3
-------
多个智能体
        ↓
并行假设搜索


阶段 4
-------
持久化研究数据库
        ↓
智能体从之前的失败中学习


阶段 5
-------
智能体特化
        ↓
研究组织


阶段 6
-------
数百/数千个智能体
        ↓
分布式研究集群
```

已经有社区扩展朝这个方向发展；例如，`autoresearch-agents` 增加了协调器/研究者/实现者角色，同时保留了基本的autoresearch循环。([GitHub][3])

而原始的`autoresearch`仓库本身有意保持最小化：**一个GPU、一个训练脚本、一个程序规范、自主迭代**。([GitHub][1])

### 在你这种情况下我会构建什么

鉴于你已经在做**LLM训练 + CUDA + 智能体**，我会做一个像这样的项目：

```text
        ┌───────────────────────────┐
        │       ResearchOS          │
        │                           │
        │  问题 → 假设              │
        │          ↓                │
        │      智能体集群            │
        │          ↓                │
        │   实验/证明               │
        │          ↓                │
        │       验证器              │
        │          ↓                │
        │   评分 + 记忆             │
        │          ↓                │
        │     下一代生成            │
        └───────────────────────────┘
```

**从4个智能体开始，而不是10,000个。**

如果你能让**4个智能体在夜间自主发现一些非平凡的东西**，扩展到100或1,000就只是一个工程问题。

如果4个智能体无法产生有用的研究，**10,000个智能体大多只会产生10,000堆垃圾**。

这正是为什么`autoresearch`是一个如此好的起点：它强迫你在投入计算资源之前先解决**评估循环**。([GitHub][1])

参考文献：

* [Karpathy — autoresearch](https://github.com/karpathy/autoresearch?utm_source=chatgpt.com)
* [autoresearch-agents 多智能体分支](https://github.com/artificialguybr/autoresearch-agents?utm_source=chatgpt.com)
* [OpenAI Navier–Stokes 报道](https://www.theverge.com/ai-artificial-intelligence/991710/openai-navier-stokes-solution?utm_source=chatgpt.com)

[1]: https://github.com/karpathy/autoresearch?ref=stdy.blog&utm_source=chatgpt.com "GitHub - karpathy/autoresearch at stdy.blog · GitHub"
[2]: https://www.wsj.com/tech/ai/openai-millennium-prize-navier-stokes-math-2bf240f8?utm_source=chatgpt.com "OpenAI Says It Has Solved a Millennium Prize Problem-a Holy Grail of Math"
[3]: https://github.com/artificialguybr/autoresearch-agents?utm_source=chatgpt.com "GitHub - artificialguybr/autoresearch-agents: AI agents running research on single-GPU nanochat training automatically · GitHub"
