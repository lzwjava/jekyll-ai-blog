---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 生成器-验证器幻觉减少
translated: true
type: note
---

**问题：**什么是 Probably Company，他们如何使用验证器来减少幻觉？  
**回答：**

我在 AI 幻觉领域找不到一个确切叫 "Probably" 的公司——很可能你想的是以下候选之一，或者名字略有偏差：

- **Probably.ai** —— Tárik S. Salem 的个人研究博客，主题是概率性 AI，并非产品公司。
- 你描述的模式（"使用验证器来减少幻觉"）对应着几个真实且知名的技术和公司。

让我给你完整地说明这个模式究竟是什么，因为它对你的 AI 工程工作确实很重要。

---

## 用于减少幻觉的验证器模式

这就是 **生成器 → 验证器** 架构。核心思想：不要信任单个模型的输出。在返回给用户之前，用第二个模型（验证器）检查事实一致性。

### 架构

```
用户提示
     │
     ▼
┌──────────┐     响应      ┌──────────────┐
│ 生成器   │ ────────────────►  │   验证器    │
│  (LLM)   │                   │  (裁判 LLM) │
└──────────┘                   └──────┬───────┘
                                      │
                              ✓ 通过 / ✗ 失败
                                      │
                              ┌───────▼────────┐
                              │ 重新提示或     │
                              │ 返回结果       │
                              └────────────────┘
```

这被广泛称为 **LLM-as-judge** 或 **验证代理**。

### 工作机制

验证器接收：
1. 原始用户查询
2. 生成器的响应
3. （可选）从 RAG 检索的上下文

然后输出结构化裁决：`{verdict: "hallucinated" | "faithful", reason: "..."}`。

典型的生成系统使用 GPT-4o 作为主要生成器，Claude 作为验证器——不同模型家族以避免关联故障模式。其权衡大约是幻觉减少 30-50%，代价是 2 倍的 token 开销和 1-3 秒的额外延迟。

### 实际在做的公司

- **AIMon** —— 专用的幻觉检测模型（HDM-1）。HDM-1 是专门的幻觉检测模型，可用于实时或离线，提供本地部署或托管配置，延迟足够低以支持重新提示和多采样工作流。

- **Galileo** —— 使用多种评估方法，包括基于嵌入的相似性、思维链分析以及专有的 G-Eval 指标，衡量上下文对齐和推理质量。

- **Datadog LLM Observability** —— 使用 LLM-as-judge 方法，配合优化后的裁判提示和通过有限状态机强制执行结构化输出，确保验证器的裁决始终是可解析的 JSON。

### 验证器实现（最小化）

{% raw %}
```python
import anthropic

client = anthropic.Anthropic()

def generate(prompt: str) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.content[0].text

def verify(query: str, response: str, context: str = "") -> dict:
    judge_prompt = f"""你是一个事实验证器。给定：
查询：{query}
上下文：{context}
响应：{response}

该响应是否忠于上下文且事实准确？
仅以 JSON 格式回复：{{"verdict": "faithful"|"hallucinated", "reason": "..."}}"""

    r = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": judge_prompt}]
    )
    import json
    return json.loads(r.content[0].text)

def generate_with_verification(prompt: str, context: str = "", retries: int = 2) -> str:
    for _ in range(retries):
        response = generate(prompt if not context else f"上下文：{context}\n\n{prompt}")
        verdict = verify(prompt, response, context)
        if verdict["verdict"] == "faithful":
            return response
        prompt += f"\n\n之前的尝试是错误的：{verdict['reason']}。请仔细重试。"
    return response  # 重试后返回最佳结果
```
{% endraw %}

### 为什么验证器有效

幻觉是当前 LLM 训练方法不可避免的副产品：最大化大规模文本语料上的预测性能，而没有内置验证器。验证器通过事后层的方式添加了缺失的事实检查约束，而不是将其融入训练过程。

ICML 2025 上发表的论文（VeriFY）教导模型在生成过程中评估事实不确定性，而非依赖事后检查——模型学会在产生陈述的同时自我验证，跨模型家族的幻觉减少 9.7–53.3%，且召回损失较小。这是下一步的演进：将验证器内化到生成器本身（比如过程奖励模型、基于事实性的 RLHF）。

---

如果你能提供更多关于你在哪里听说 "Probably company" 的背景——播客、推文、论文、视频——我可以帮你找到准确的引用。这个名字可能略有不同（例如 "Proba"、"ProbAI"、"Probably Good" 等）。