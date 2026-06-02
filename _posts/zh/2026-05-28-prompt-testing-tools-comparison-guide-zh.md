---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 提示测试工具比较指南
translated: true
type: note
---

**问题：** 用于提示词测试/游乐场的最佳开源工具是什么——特别是用于比较不同提示词并了解哪些有效、哪些无效？

**回答：**

以下是按对 CLI 优先、快速构建工作流的适合程度排序的现状：

---

## 1. **`promptfoo`** —— 你的黄金标准

**GitHub：** https://github.com/promptfoo/promptfoo —— 约 1 万星标

CLI 优先、开源，使用存储在仓库中的 YAML 配置，专为在终端中生活的开发者设计。将提示词评估视为软件测试：声明式配置、批量测试、回归检查。

这就是你想要的工具。以下是最简工作流：

```bash
npx promptfoo@latest init
# 创建 promptfooconfig.yaml

npx promptfoo@latest eval
# 运行 提示词 × 模型 × 测试用例 的矩阵

npx promptfoo@latest view
# 打开本地 Web UI，提供并排比较
```

用于提示词 A/B 测试的典型配置：

{% raw %}
```yaml
# promptfooconfig.yaml
prompts:
  - "总结以下内容：{{text}}"
  - "你是一个简洁的助手。用两句话总结：{{text}}"

providers:
  - openai:gpt-4o-mini
  - anthropic:claude-sonnet-4-5

tests:
  - vars:
      text: "Transformer 架构使用注意力机制来加权 token 之间的关系..."
    assert:
      - type: contains
        value: "attention"
      - type: llm-rubric
        value: "总结是否准确且不超过 100 词？"

  - vars:
      text: "反向传播通过链式法则计算梯度..."
```
{% endraw %}

运行 `npx promptfoo@latest eval`，它会将每个测试用例应用于每个模型/提示词组合。然后 `npx promptfoo@latest view` 打开带有矩阵的 Web 查看器。

杀手级功能：红队测试——探测提示词的漏洞，测试提示注入、PII 泄露以及可能破坏护栏的边缘情况。这是唯一一个专门为安全性测试和性能评估而构建的工具。

CI/CD 集成：有一个 GitHub Action，当你的提示词文件发生变化时，会在 PR 上发布前后差异。

---

## 2. **Langfuse** —— 如果你想要 UI + 追踪

**GitHub：** https://github.com/langfuse/langfuse

Langfuse 的游乐场支持并排提示词比较，并可并行执行 LLM。每个变体都有自己的 LLM 设置、变量、工具定义和占位符——你可以立即看到每个更改的影响。

当你在追踪中看到糟糕的结果时，可以直接跳转到游乐场对其进行迭代。通过 Docker Compose 约 5 分钟即可自托管。

最适合：你已经在追踪生产调用，并希望在线重现并修复一个糟糕的输出。

---

## 3. **Agenta** —— 完整 LLMOps 平台

**GitHub：** https://github.com/Agenta-AI/agenta

Agenta 将提示词视为代码并带有版本控制，包含一个游乐场，可让你同时微调并比较来自 50 多个 LLM 的输出。

并排模型比较，跨 GPT-4、Claude、Gemini、Mistral、DeepSeek 进行测试，并显示成本和延迟差异，以便做出明智决策。

比 promptfoo 更重，但更完整。可自托管。

---

## 4. **Arize Phoenix** —— 用于智能体评估

Phoenix 提供提示词游乐场和 LLM 评估，并且是少数不需要单独数据库的开源平台之一——无需 Redis 或 ClickHouse。兼容 OpenTelemetry 的追踪。

如果你正在评估智能体/RAG 管道，它是不错的选择。

---

## 我的推荐

**从 `promptfoo` 开始。** 它完美契合你的工作流：

```bash
# 全局安装
npm install -g promptfoo

# 或直接使用 npx
npx promptfoo@latest init --example compare-models

# 然后迭代：
# 1. 编辑 promptfooconfig.yaml（提示词 + 测试用例）
# 2. npx promptfoo eval
# 3. npx promptfoo view（Web 矩阵 UI）
```

YAML 即代码的模式意味着你将提示词实验版本化到 Git 中，在 CI 上运行评估，并获得清晰的“提示词变体 × 模型 × 测试用例 → 通过/失败 + 输出”矩阵。这正是你想要的“什么有效、什么无效”的答案——不是凭感觉，而是一个可 diff 的评估网格。

对于你在银行从事的 AI 工程师工作，红队测试功能（`npx promptfoo@latest redteam`）在演示企业环境中的提示词鲁棒性方面也很有用。

**参考：**

- [promptfoo GitHub](https://github.com/promptfoo/promptfoo)
- [promptfoo 入门](https://www.promptfoo.dev/docs/getting-started/)
- [Langfuse 并排游乐场](https://langfuse.com/changelog/2025-07-28-playground-side-by-side)
- [Agenta 提示词游乐场 2.0](https://agenta.ai/blog/prompt-playground)
- [2025 年 7 大开源提示工程工具](https://latitude.so/blog/top-7-open-source-tools-for-prompt-engineering-in-2025)
