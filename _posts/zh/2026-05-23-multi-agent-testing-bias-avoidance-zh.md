---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多智能体测试偏差避免
translated: true
type: note
---

是的，这是一种非常自然的模式。它映射到多个成熟的软件工程原则：

1. TDD 红绿循环——一个“编写代码”，另一个“验证其通过”
2. 作者与审阅者分离——这也是人类进行代码审查时由非编写者来审查的原因
3. 纵深防御——编码代理存在盲点，而独立的测试代理可以捕捉到这些盲点

关键在于：当同一个代理同时编写代码和测试时，它会无意识地设计出能通过的测试。分离代理则打破了这种偏见。

实际工作流程：

```
Agent A（编码者）："在模块 Y 中实现功能 X"
Agent B（测试者）："审查 X 的实现，编写全面的测试，运行它们，并将失败报告回去"
Agent A（编码者）："修复 Agent B 发现的失败"
```

在 Hermes 中，你可以通过 `delegate_task` 来编排这一流程：

```
# 阶段 1：编码
delegate_task(goal="使用 JWT 实现用户认证模块", toolsets=["terminal","file"])

# 阶段 2：测试（独立代理，无阶段 1 的上下文）
delegate_task(goal="审查并测试 /src/auth.py——编写 pytest 测试，运行它们，识别边缘情况，报告失败", 
              toolsets=["terminal","file"])
```

这种分离在以下方面尤其有效：
- 捕捉对快乐路径的过度拟合
- 发现编码者未考虑的未处理边缘情况
- 安全审查（测试代理专注于攻击向量）
- API 契约验证（测试者从消费者角度检查）

这本质上与 Anthropic 内部使用 Constitutional AI 的做法相同——一个模型生成，另一个模型进行批评。也是 Devin/OpenHands 风格代理在 plan-then-verify 循环中的做法。

需要我在你的 Hermes 环境中为这种双代理模式设置一个具体的工作流或技能吗？