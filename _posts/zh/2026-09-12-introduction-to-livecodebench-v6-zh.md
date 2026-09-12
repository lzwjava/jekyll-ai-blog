---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LiveCodeBench v6 简介
translated: true
type: note
---

问题：**“LiveCodeBench v6 — 给我做个介绍。”**

回答：

![图片](https://images.openai.com/static-rsc-4/kAHVDfK0lB23vOCEO8IpX9mn8X18L2p4UlkDiRLHnAt7d9QKl6SC_fIbgvZrNhmxYWeETFHLQWs7d-6cm3AWUze3gSV9hML-O8joujM0yBUNdPo7ePwdzwSSQAR_8DCMQQpjYSLbDEqsI0QHZ6mB4RGXk4sk4pw5wCGyq2F63uPU_kI7OosI-cHC3gHNwRq4?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/qRB-uuBm0u1Nisf-M9JRXEBBnN4wjek7wwn7p-_QRdGEdkmZXuilKEAeercxqj5ug-XSFV3n2Dnpw5gALMd4Um8hJAWQ0f9jPHpueIn_3yz8bzQY7TONTvNIGGJb9cXnY6KWtitIPV95U_3Mj867NvwqwQs9MwbxdlOH-G9GuwO9aswmixNg5RqiUU62ScRW?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/a0Jjoz4_YlnmfIcl89JVZEOOq53j_nQjcEQ-2IbPlsxxP3fATfI2HaTKwMKHNi8yO-BLxEZR1-ECSZGYdmXurDBo85t3l9OD21Q6baakh7Sfdf53wcrF0TrK22S3DjPSlTbF5eqZbPosGLQgP858YqCrKv5x5XkW8Ea2ph9LTBksk-zEALeDrLG7wIcm5_RZ?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/oZlfzDDST93Rv66jQH3jI9T8M60BKaCLSqdkJ5mbO_JwKl6SLHbNud7ZmYDYiE6bBdT0dZ7PJkJ2-mmghMvzAXgcMHXxX77LhwsGOBAMP8ckj2GY--T9GgF8SPKnky_bwgNt-XOeQ52zdan-yUYtKfEI0_GgyxC4_bjGIi0Va7WKOeuEfDFgURzDtPWkgor1?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/tQNrxiac1GRNEwQbo1zh9R4xPK7EN-WLXZRbGz5kPdyFXO_NyKoqwCd04FEc1wMO7vHui0Ot4LeZGmuwwLrRPllwkDTszNxrhABq2SI6jHVaGxGWJo3TKR2pTeZYTfFfKvkHfGgC12oqCQNPtOrAPG_ApJLmhkhkWkqbrdYo0SXMw1XVsLIsTq2KZn63DFPc?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/6iVzz-jGEkIbWyx57rmbcGa5PBUBxwZ1Q4XZyPR03fE4x0fbdnHH3mEGWuC5y6w4M8ld_D6Wys7lNq9NF4MJW3g1Nn_qfT9PItB5vHiySh8_noblM9WR9nZD8SorjxM0dPVnhScUb8D72QLJeL2Xxd981dRjiVRRCIwPfVDQssJQW3PNkOmopdkQbJwqFoRR?purpose=fullsize)

**LiveCodeBench (LCB)** 是一个衡量 LLM 实际解决编程问题能力的基准测试，专门设计用于减少旧有编程基准测试中的**污染/记忆问题**。

核心思想很简单：

> **不要用昨天的编程题目来评估。要评估那些出现在模型训练数据之后的问题。**

LiveCodeBench 持续从 **LeetCode、AtCoder 和 Codeforces** 拉取新的竞赛编程题目，然后针对隐藏测试评估生成的程序。（[GitHub][1]）

### v6 的含义

`release_v6` 是此滚动基准测试的一个**冻结快照**：

| 发布版本 | 问题截止日期 | 问题数量 |
| ------- | -------------: | ---------: |
| v1      |       2024年3月 |        400 |
| v2      |       2024年5月 |        511 |
| v3      |       2024年7月 |        612 |
| v4      |       2024年9月 |        713 |
| v5      |       2025年1月 |        880 |
| **v6**  |   **2025年4月** |  **1,055** |

因此，**v6 并非一个本质上不同的基准测试**。它是同一基准测试的一个更新、更大的时间切片。（[GitHub][1]）

### 它实际衡量什么

有趣的是，LCB 不仅仅是“提示 → 代码”：

```text
                    LiveCodeBench
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   代码生成          代码执行        测试输出
        │                                  │
        ▼                                  ▼
   编写程序                          预测输出
        │
        ▼
   隐藏测试
        │
        ▼
      pass@k

                         +
                   自我修复
```

该存储库支持四大类能力：

1. **代码生成** —— 根据问题描述编写解决方案。
2. **自我修复** —— 利用测试反馈修复生成的代码。
3. **代码执行** —— 推理程序将输出什么。
4. **测试输出预测** —— 为给定测试生成预期输出。（[GitHub][1]）

对于常规代码生成，基本评估循环大致如下：

```python
problem = get_fresh_problem()

completion = model.generate(problem)

result = run_with_hidden_tests(completion)

score = result.passed
```

最后一行很重要：**这是功能正确性，而不是某个 LLM 评判员说代码“看起来不错”。**

### 为什么 LCB 变得重要

将其与 HumanEval 对比：

```text
HumanEval

训练数据 ────────────────► 模型
                    │
                    │ 可能的记忆
                    ▼
                 基准测试
```

对比 LiveCodeBench：

```text
模型训练截止点
        │
        ▼
────────┼──────────────────────────────
        │
        │       新的竞赛题目
        │              │
        │              ▼
        │         LiveCodeBench
        │              │
        │              ▼
        │        编译 + 执行
        │              │
        │              ▼
        │         隐藏测试
```

这赋予 LCB 一个有用的特性：**性能在一个时间分布上进行评估，模型在预训练期间不太可能见过这个分布。**

这就是为什么一个模型可能在 HumanEval 上得分极高，而在 LCB 上却显得不那么亮眼。最初的 LCB 论文明确发现了静态编程基准测试可能出现过拟合/饱和的证据。（[GitHub][2]）

### 对于模型训练，重要的思维模型

我认为应将 LCB 视为衡量接近以下内容：

```text
编码智能
≈
问题理解
×
算法选择
×
推理
×
实现
×
调试
```

而不是简单地：

```text
“模型之前见过这段代码吗？”
```

这也是为什么**推理模型从 LCB 中获益巨大**：许多竞赛题目需要发现一个算法，而不是回忆一个 API。

当前已发布的 2026 年榜单显示，前沿模型在一些报告的 LCB-v6 配置上达到了大约 **90%+**，不过比较数字时需要谨慎，因为采样次数、pass@k、温度、问题窗口和评估策略在不同报告中可能不同。（[BenchLM][3]）

### 如果你打算自己运行

官方仓库是使用的正确选择：

[LiveCodeBench GitHub 仓库](https：//github.com/LiveCodeBench/LiveCodeBench？utm_source=chatgpt.com)

例如：

```bash
git clone https：//github.com/LiveCodeBench/LiveCodeBench
cd LiveCodeBench

# 然后评估模型在 v6 上
python -m lcb_runner.runner.main \
  --model <MODEL> \
  --scenario codegeneration \
  --evaluate \
  --release_version release_v6
```

官方实现使用 vLLM 进行开源模型推理，并支持张量并行，因此将本地模型扔给基准测试相对直接。（[GitHub][1]）

**一句话总结：** **LiveCodeBench v6 本质上是一个包含 1,055 道题目、时间上全新的竞赛编程评估，旨在回答“这个模型真的能解决新的编程问题吗？”而不是“这个模型能复现其训练数据中的编程模式吗？”**

我还可以详细讲解 **LCB v6 评估器的代码路径：从提示 → 采样 → 沙盒 → 检查器 → pass@k**，如果你计划对模型进行基准测试/训练，这部分可能很有用。

[1]：https：//github.com/livecodebench/livecodebench？utm_source=chatgpt.com “GitHub - LiveCodeBench/LiveCodeBench：论文《LiveCodeBench： Holistic and Contamination Free Evaluation of Large Language Models for Code》的官方仓库 · GitHub”
[2]：https：//github.com/noahshinn/LiveCodeBench/blob/main/README.md？utm_source=chatgpt.com “livecodebench/README.md at main · noahshinn/livecodebench · GitHub”
[3]：https：//benchlm.ai/benchmarks/livecodebench-v6？utm_source=chatgpt.com “LiveCodeBench v6 排行榜 & 分数 — 2026年9月 | BenchLM.ai”