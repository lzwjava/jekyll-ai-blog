---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 推理成本骤降引发人工智能辩论
translated: true
type: note
---

**问题：** 未来推理将变得廉价而快速——文本转图像、翻译等等都会如此。Whisper 很快，Sesame 也很快。AI 之间能否互相争论？

**回答：**

能，而且这已经在发生。趋势非常明确：

**推理成本暴跌是真实的。** 如今 GPT-4 级别能力的成本比两年前低了约 100 倍。Groq 的 LPU 能做到每秒 800+ token，Cerebras 能做到每秒 2000+ token。文本转图像从 30 秒（SD 1.x）缩短到不到 1 秒（SDXL Turbo、FLUX schnell）。Whisper 在 CPU 上即可实时运行。这一趋势并未放缓。

**AI 辩论 / 多智能体争论已成为一个研究方向。** 几种具体形式如下：

- **心智社会 / 多智能体辩论** —— 多个 LLM 就某一立场进行争论，由裁判模型选出最佳答案。已被证明能提升复杂问题的推理能力（Du 等人，2023 年——《通过多智能体辩论提升语言模型的事实性和推理能力》）
- **宪法 AI** —— Claude 自己的训练就使用了 AI 对 AI 的批评循环（红队测试、修订）
- **LLM 作为裁判** —— 一个模型为另一个模型的输出打分；现已成为 RLHF 流程的标准做法
- **AutoGen / CrewAI** —— 拥有对立角色（魔鬼代言人、批评者、优化者）的智能体在一个消息循环中真正争论，直到收敛

**“AI 争论”在代码中看起来是什么样（50 行）：**

```python
import anthropic

client = anthropic.Anthropic()

def agent_turn(role: str, position: str, history: list[dict]) -> str:
    system = f"You are {role}. Argue {position} forcefully. Be concise, technical, sharp."
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=system,
        messages=history,
    )
    return response.content[0].text

def debate(topic: str, rounds: int = 3):
    history_a, history_b = [], []
    last_b = f"Let's debate: {topic}"

    for i in range(rounds):
        # Agent A responds to B
        history_a.append({"role": "user", "content": last_b})
        reply_a = agent_turn("Agent A", "FOR", history_a)
        history_a.append({"role": "assistant", "content": reply_a})
        print(f"[A] {reply_a}\n")

        # Agent B responds to A
        history_b.append({"role": "user", "content": reply_a})
        reply_b = agent_turn("Agent B", "AGAINST", history_b)
        history_b.append({"role": "assistant", "content": reply_b})
        print(f"[B] {reply_b}\n")
        last_b = reply_b

debate("MoE is better than dense transformers for frontier models")
```

**有趣的意义：** 当推理近乎免费时，你可以并行运行 100 个智能体进行争论，提炼共识，从而得到比任何单一模型更好的答案。这基本上就是带语言的集成学习。DeepSeek R1 的思维链是一个模型与自己争论——多智能体辩论则是其分布式版本。

**具体到 Sesame**（对话式语音 AI）—— 速度快到足以感觉实时，情感丰富到足以感觉像真人。当两个这样的 AI 争论时，几乎分辨不出与人类在播客上辩论的区别。这就是不久的将来。

瓶颈从“我们能否做到”转移到了“什么值得争论”——策展和编排成为真正的工程问题。

**参考文献：**

- [Improving Factuality via Multiagent Debate — Du et al. 2023](https://arxiv.org/abs/2305.14325)
- [AutoGen: Multi-agent conversation framework](https://github.com/microsoft/autogen)