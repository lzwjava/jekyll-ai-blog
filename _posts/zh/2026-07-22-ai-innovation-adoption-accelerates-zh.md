---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI创新采用加速
translated: true
type: note
---

问题：你在论证 AI 正在加速创新想法的采纳，因此你愿意早期支持像 Pi Agent 这样的项目，而不是等待主流验证。这方向对吗？

我认为这里有一个真实的趋势。

二十年前，一个创新的开发者工具有着漫长的采纳路径：

> 论文/博客 → 会议 → 早期采用者 → 书籍 → 公司 → 主流

这通常需要 **5-10 年**。

如今更像是：

> GitHub repo → X/Twitter → AI 总结它 → 数以千计的人询问 Claude/ChatGPT → agents 安装它 → 人们当天尝试

AI 极大地降低了**理解成本**。

对于像 Pi Agent 这样的东西，障碍不再是“有人能理解架构吗？”。通常只是：

```bash
git clone ...
uv sync
pi run
```

如果有人遇到困难：

```
paste error → ask GPT/Claude → continue
```

而不是花三个小时读源代码。

---

你关于为什么使用 Pi Agent 的观点，从一位有经验的工程师角度来看，也很有道理。

如果你已经理解一个 agent 从根本上来说是：

```
LLM
+ tool calling
+ context management
+ planning loop
+ execution runtime
```

那么一个新框架并不神秘。

你可以通过问以下问题来评估它：

* tool abstraction 是否干净？
* execution loop 是否优雅？
* context management 是否可扩展？
* extension 是否容易？
* 它是否与其他工具 compose 良好？

而不是

> “其他人是否都在使用它？”

这是一个更强大的评估标准。

---

我也不会将其框定为“Claude Code vs. Hermes vs. Pi Agent”。

它们服务于略有不同的优化目标。

* **Claude Code**: polished UX, broad adoption, production workflow.
* **Hermes**: open CLI ecosystem with good extensibility.
* **Pi Agent**: experimentation, new interaction models, architectural exploration.

优秀的工程师常常同时使用这三者。

许多基础设施理念在成为标准之前看起来都很小众：

* Git
* Docker
* Kubernetes
* PyTorch
* vLLM

早期采用者并不一定是在赌流行性——他们认识到了一种更简单或更强大的抽象。

---

AI 改变的另一个方面是反馈循环。

之前：

```
想法
 ↓
原型
 ↓ 数周
用户
 ↓
反馈
```

现在：

```
想法
 ↓
AI 在数小时内写出原型
 ↓
用户测试
 ↓
AI 分析日志
 ↓
下一个版本
```

这种压缩意味着创新想法要么更快失败，要么更快成功。

---

你提到的心态——像 Liang Wenfeng、Jensen Huang、Andrej Karpathy 或 Alex Ford 这样的人的思考方式——与其说是完美预测未来，不如说是愿意从第一性原理评估想法，而不是等待社会证明。

AI 放大了这一点，因为它降低了探索的成本。如果评估一个新框架只需要一个下午而不是一周，那么尝试更多想法就变得合理了。这是当今软件工程领域发生的最重大转变之一。
