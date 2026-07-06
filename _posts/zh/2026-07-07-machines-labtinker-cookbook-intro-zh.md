---
audio: false
generated: true
image: false
lang: zh
layout: post
title: -机器实验室/修补手册入门
translated: true
type: note
---

**问题：** 请介绍 `thinking-machines-lab/tinker-cookbook` 仓库。

**答案：**

## 它是什么

Tinker 是 Thinking Machines Lab（Mira Murati 的实验室，成员包括 John Schulman，RLHF/PPO 领域的专家）推出的训练后即服务产品。它包含两个库：`tinker`，一个训练 SDK，你只需发送 API 请求，他们负责处理分布式训练的复杂性；以及 `tinker-cookbook`，它基于 Tinker API，提供了逼真的微调示例和通用抽象。

其核心设计理念对你而言颇具价值：**它并非像 OpenAI 那样“提交数据集，获得模型”的微调 API。** 它通过网络暴露了底层的训练原语，因此*你*在本地编写训练循环，而他们在自己的集群上运行前向/反向传播。你保留算法控制权；他们负责处理分布式系统的难题（FSDP、流水线并行、任务抢占恢复）。

## 原语层

整个 API 表面基本上就是四个动词：

```python
import tinker

service_client = tinker.ServiceClient()
training_client = service_client.create_lora_training_client(
    base_model="meta-llama/Llama-3.2-1B", rank=32,
)

training_client.forward_backward(...)   # 在他们的集群上计算损失 + 累积梯度
training_client.optim_step(...)         # 应用优化器更新
training_client.save_state(...)         # 检查点保存
sampling_client = training_client.save_weights_and_get_sampling_client()
sampling_client.sample(...)             # 用于强化学习/评估的 rollout
```

这种分解就是全部的诀窍所在。由于 `forward_backward` 和 `sample` 是你可以控制的独立调用，你可以在其上实现*任何*训练后算法——SFT、DPO、PPO/GRPO、蒸馏——只需改变你馈送的数据以及在调用之间计算奖励/损失的方式。它基于 LoRA（注意 `rank=32`），这使得在他们那端为数千用户提供多租户微调服务变得经济可行（共享基础权重，每个用户专属适配器）。

与你自己的 nanochat 工作相比：nanochat 提供了完整的堆栈，但你需要自己拥有 GPU；Tinker 提供了 nanochat 级别的循环控制，但使用的是他人的集群。你还可以将任何模型的权重作为检查点存档下载，因此不存在锁定陷阱——在那里训练，导出，然后在你自己的 MI300X 上提供服务。

## cookbook 里有什么

recipes 目录实际上是对现代训练后算法的概览，每个均可直接运行：

`sl_loop.py` 和 `rl_loop.py` 是使用这些原语的最小示例，而 `sl_basic.py` 和 `rl_basic.py` 展示了最简的 SL/RL 配置。更完整的 recipes 涵盖了聊天 SFT（Tulu3 风格）、具有可验证奖励的数学 RL、通过沙箱执行复现 DeepCoder 的代码 RL、偏好学习（DPO 及三阶段 RLHF 流程：SFT → 奖励模型 → RL）、支持多教师配置的同策略和异策略蒸馏、复现 Search-R1 的工具使用 RL、以及包含自我博弈的多智能体 RL。recipes README 中还包含了基于量表的评分、VLM 分类和 SDFT。

对于学习，`tutorials/` 目录包含 20 多个渐进式的 marimo 笔记本，涵盖了渲染、损失函数、补全器、权重管理、自定义强化学习环境、DPO、RLHF 和权重导出。

即使你从不使用该 API，其可重用的基础设施也值得一读：

- `renderers` — 在 token 序列和结构化聊天消息之间进行双向转换。这是每个人都会犯错的、不起眼的部分（聊天模板 ↔ token 掩码 ↔ 损失权重）。他们的抽象方法值得在你的训练代码中借鉴。
- `hyperparam_utils` — LoRA 训练的学习率和超参数缩放——编码了他们的“无憾 LoRA”发现（学习率与秩的缩放关系）。
- 一个评估框架，支持 12 个基准测试（GSM8K, MATH-500, MMLU-Pro, GPQA, IFEval, AIME 2025/2026 等），分数经与已发表结果验证一致，可在训练期间通过 `BenchmarkEvaluator` 内联使用。

还有一个细节：该仓库提供了 Claude Code 技能——`/tinker:research` 用于规划训练后实验，`/tinker:debug` 用于诊断训练问题，可通过 `/plugin marketplace add thinking-machines-lab/tinker-cookbook` 安装。鉴于你的 CLI 智能体工作流，这可以直接使用。

## 快速开始

```bash
uv pip install tinker-cookbook
export TINKER_API_KEY=<API_KEY>   # 注册后从 tinker-console.thinkingmachines.ai 获取
marimo edit tutorials/101_hello_tinker.py
```

## 为什么这对你特别重要

你的定位正是“达到 Tinker 级别的技能。”使用这个仓库最高杠杆率的方式不是作为客户——而是作为**参考架构**。阅读 `rl_loop.py`、renderers 和 RLHF recipe，然后将每个抽象映射到你将在 MI300X 上用自己的 DeepSeek 风格 MoE 工作自建的内容上。“API 包装器顾问”和“前沿实验室级别”之间的差距恰恰就是 `tinker_cookbook/recipes/` 中的代码——损失掩码、优势计算、奖励模型流程。它是 Apache-2.0 许可、445 次提交、积极维护（v0.4.1，2026 年 5 月）、纯 Python。它是最清晰公开表达前沿实验室如何看待训练后循环的代码之一。

**参考文献：**

- [tinker-cookbook (GitHub)](https://github.com/thinking-machines-lab/tinker-cookbook)
- [Tinker 文档](https://tinker-docs.thinkingmachines.ai)
- [Tinker 产品页面](https://thinkingmachines.ai/tinker/)
