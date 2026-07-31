---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Terminal-Bench 2.1 概览与排行榜
translated: true
type: note
---

问题：什么是Terminal-Bench 2.1？当前的模型排行榜如何？

答案：

**是什么：** Terminal-Bench 2.1是对2.0版本的修订——它评估智能体模型系统在通过命令行界面完成的89个技术任务上的表现，涵盖软件工程、机器学习、安全、数据处理、科学计算和系统管理。这不是一个新的任务集，只是修复：89个任务中有28个存在问题（外部依赖损坏、资源预算过于紧张、指令与测试不匹配），修复后没有任务是未解决的。

工具/方法：所有模型均使用Terminus 2工具进行基准测试，结果采用pass@1，模型必须通过任务上的所有pytest才能获得任何分数。

**排行榜（2026年7月）：**

| 模型 | 分数 |
|---|---|
| GPT-5.6 Sol (OpenAI) | 0.888 |
| Kimi K3 (Moonshot，顶级开源) | 0.883 |
| GLM-5.2 (智谱，前10%中最便宜) | 0.827 |

LLM Stats追踪了该基准测试上的15个模型，平均分数为0.8，领先者为0.888（GPT-5.6 Sol）。0个验证结果，15个自报告。

从2.0到2.1的最大变化：Claude Code与Opus 4.6提升了12.1个百分点——考虑到任务修复不成比例地解开了之前无法解决的环境问题，这很合理。

注意：这些都是实验室自报告的，并非独立验证——如果您在信任您关心的模型的特定数值之前想要第三方交叉验证，值得查看Artificial Analysis。

**如果您想自己运行：**
```bash
git clone https://github.com/harbor-framework/terminal-bench
cd terminal-bench
# harbor 是2.x的新框架
# 在工具配置中使用 --dataset-name terminal-bench-2.1
```

参考资料：
- [Terminal-Bench 2.1 — Snorkel AI](https://snorkel.ai/leaderboard/terminal-bench-2-1/)
- [Terminal-Bench 2.1 排行榜 — LLM Stats](https://llm-stats.com/benchmarks/terminal-bench-2.1)
- [Terminal-Bench v2.1 — Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-v2-1)
- [harbor-framework/terminal-bench — GitHub](https://github.com/harbor-framework/terminal-bench)
- [Terminal-Bench 2.1 — vals.ai](https://www.vals.ai/benchmarks/terminal-bench-2-1)