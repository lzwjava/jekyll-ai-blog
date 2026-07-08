---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建目标模式智能体循环
translated: true
type: note
---

问题：在像 Hermes（Nous Research）这样的智能体框架中，实际上如何使用“目标模式”/长期任务执行——以及如何将相同的模式构建到你自己的 CLI 智能体中（ww, iclaw, zz）？

答案：

## 1. Hermes 的实际机制（原理，而非炒作）

Nous Research 的 Hermes Agent 是一个开源 AI 智能体框架，采用 MIT 许可证发布，它运行一个五阶段的学习循环：执行、评估、将可重复的推理模式提取为命名技能、完善这些技能、为新任务检索相关技能，并配备五个沙箱后端——本地、Docker、SSH、Singularity 和 Modal。与 OpenClaw 等框架的区别在于，Hermes 将技能形成视为智能体自身运行循环的一部分，而不是依赖外部技能市场——在完成复杂任务后，它会编写一份结构化的技能文档，记录步骤、陷阱和验证步骤，并在后续运行中改进该技能。

具体来说，“目标模式”的长期任务机制是这样工作的：

- `/goal <text>` 设定一个长期目标，`/goal status` 检查进度，`/goal pause`/`/goal resume` 暂停和恢复而不丢失状态。
- 每轮操作后，会调用一个**辅助判断模型**来决定目标是否完成。该判断模型故意保守——只有当回复明确确认完成、交付物明确产生、或目标确实被阻塞（视为已完成并附上阻塞原因，以免预算浪费在不可能的任务上）时，才会标记目标为完成。关键的是，它采用“失败开放”语义：如果判断模型出错，Hermes 将判定结果视为“继续”，因此有缺陷的判断模型永远不会阻碍进度。
- 回合预算有上限——默认为 20 个连续回合（在 `~/.hermes/config.yaml` 中的 `goals.max_turns`），当预算用完时，Hermes 自动暂停并报告已使用多少回合。
- 可组合性：当目标触发并编排执行各个步骤的特定技能时，结合技能的目标效果良好；结合记忆持久性的目标可以在多天内保持长期目标的一致性；结合多智能体设置的目标允许管理智能体为工作智能体设置子目标。

⚠️ 注意事项：描述这一机制的几个来源（aiprofitboardroom.com、juliangoldieaiautomation.com、aisuccesslabjuliangoldie.com）是同一个 SEO 内容农场作者重复近乎相同的模板——请将具体数字（ROI 声称、£/月节省）视为营销，而非经过验证的事实。机制本身（基于判断模型的回合预算循环、`/goal` 命令、配置路径）在不同独立文章中（i-scoop.eu、openhosst.com）得到证实，因此我更相信*架构*描述，而非*案例研究数字*。

在复制此模式前需要记住的两个失败模式：目标模糊导致判断模型无法确定完成——请具体说明“完成”的含义；以及为大目标使用默认回合预算，因为 20 个回合无法完成 50 步的任务。

## 2. 这是一种通用模式——用约 80 行代码自行构建

你不需要 Hermes 来实现这一点。核心原语是：**执行循环 + 判断/评论 + 回合预算 + 持久化状态**。学术工作将其形式化为规划器-执行器分离——规划器接收任务指令，在执行前将其分解为参考子目标图，然后通过将执行器的轨迹与该图进行比较来跟踪进度，当执行器偏离或停滞时进行纠正性反馈。这可以直接用于你的 CLI 智能体。

```python
# goal_loop.py — 适用于 ww/iclaw/zz 的最小化 Hermes 风格目标框架
import json, os, time
from anthropic import Anthropic

client = Anthropic()
STATE_PATH = ".goal_state.json"

def load_state():
    if os.path.exists(STATE_PATH):
        return json.load(open(STATE_PATH))
    return None

def save_state(s):
    json.dump(s, open(STATE_PATH, "w"), indent=2)

def judge(goal: str, transcript: str) -> dict:
    """保守的判断模型——出错时失败开放（遵循 Hermes 语义）。"""
    try:
        resp = client.messages.create(
            model="claude-opus-4-8",  # 使用比执行器更强的模型作为判断模型
            max_tokens=300,
            system=(
                "You are a strict completion judge. Given a GOAL and a TRANSCRIPT of "
                "an agent's work, respond ONLY with JSON: "
                '{"done": bool, "blocked": bool, "reason": str}. '
                "Mark done=true only if the deliverable is explicitly produced, or "
                "blocked=true if further progress is genuinely impossible."
            ),
            messages=[{"role": "user", "content": f"GOAL:\n{goal}\n\nTRANSCRIPT:\n{transcript}"}],
        )
        return json.loads(resp.content[0].text)
    except Exception:
        return {"done": False, "blocked": False, "reason": "judge_error_fail_open"}

def actor_step(goal: str, history: list, tools: list) -> str:
    resp = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2000,
        system=f"Standing goal: {goal}\nWork one concrete step closer to completion. "
                f"State clearly if you believe the goal is now complete.",
        messages=history,
        tools=tools,
    )
    # ... 处理 tool_use 块，附加 tool_result 等（为简洁省略）
    text = "".join(b.text for b in resp.content if b.type == "text")
    history.append({"role": "assistant", "content": resp.content})
    return text

def run_goal(goal: str, tools: list, max_turns: int = 20, resume: bool = False):
    state = load_state() if resume else None
    history = state["history"] if state else []
    turn = state["turn"] if state else 0

    while turn < max_turns:
        turn += 1
        out = actor_step(goal, history, tools)
        transcript = "\n".join(m.get("content", "") if isinstance(m.get("content"), str) else str(m) for m in history)

        verdict = judge(goal, transcript)
        print(f"[turn {turn}/{max_turns}] judge={verdict}")

        if verdict["done"] or verdict["blocked"]:
            save_state({"history": history, "turn": turn, "status": "finished", "reason": verdict["reason"]})
            return verdict

        save_state({"history": history, "turn": turn, "status": "running"})
        time.sleep(1)  # 退避/速率限制卫生

    save_state({"history": history, "turn": turn, "status": "paused"})
    print(f"⏸ Goal paused — {turn}/{max_turns} turns used. Call run_goal(..., resume=True) to continue.")
    return {"done": False, "blocked": False, "reason": "turn_budget_exhausted"}
```

关于每个部分对你的上下文重要性的说明：

- **判断模型 ≠ 执行模型。** 使用更强/更便宜的模型作为判断模型而非执行模型（Sonnet 执行 + Opus 判断，或者如果成本重要的话用便宜快速的模型作为判断模型——这正是 Hermes 文档在推荐“Sonnet 4.8 Review——我推荐的判断模型”时所说的）。
- **失败开放是强制性的。** 判断模型异常绝不应静默地杀死一个长时间运行的任务。这是人们自己实现时遇到的最大错误。
- **回合预算迫使你提前编写“完成”规范**——这更多是纪律问题，而非代码问题。如果你不能用一句话说明“完成”的样子，那么无论使用什么框架，你的目标都太模糊，无法生效。
- **持久化状态（这里用 JSON 磁盘，生产环境用 Redis/SQLite）是使其成为“长时间任务”而非单一长上下文窗口的原因**——你是在用上下文长度换取检查点迭代，这也避免了在 100 多回合任务中上下文衰退。

## 3. 深入方向（符合你的 MoE/智能体架构方向）

- 使用显式子图进行子目标分解，而非隐式判断模型调用：智能体在执行过程中随着新信息到来而失去方向，缺乏清晰的适应路径到达最终目标——这在 RL 微调期间更加严重，因为稀疏、延迟的奖励使得难以识别哪些动作导致成功。如果你要训练/RL 自己的智能体（符合你的 GRPO 兴趣），在围绕判断模型构建奖励模型之前请阅读此内容。
- 如果你希望判断模型本身是一个*训练过的*规划器而非提示式规划器：EAGLET 引入了一个即插即用、特定任务的规划器模型，其唯一职责是生成全局计划，采用计划与执行框架，其中全局规划器和执行器清晰分离——这是在你上面提示式判断/执行器分离稳定后，希望将其蒸馏为更便宜的规模化运行时的自然下一步（比仅使用 API 更符合你的 nanochat/DeepSeek MoE 轨迹）。

对于你的 CLI 工具具体而言：我会先将 `judge()` 失败开放模式和回合预算暂停/恢复机制接入 `zz` 或 `ww`，因为这只需约 80 行且与框架无关，然后再全面采用 Hermes——你就能获得相同的长期任务能力，而无需承担其生态系统（根据比较文章）比 OpenClaw 更小、更年轻，且安全性尚未在大规模下得到验证的依赖。

参考文献：

- [Hermes Agent from Nous Research](https://www.i-scoop.eu/hermes-agent-from-nous-research/)
- [Hermes Agent: What It Is, How It Works (2026)](https://openhosst.com/blog/hermes-agent)
- [Hermes Goal Mode — Set The Target. Walk Away.](https://agentos.guide/hermes-goals)
- [A Goal Without a Plan Is Just a Wish: EAGLET (arXiv)](https://arxiv.org/pdf/2510.05608)
- [A Subgoal-driven Framework for Improving Long-Horizon LLM Agents (Google DeepMind, arXiv)](https://arxiv.org/pdf/2603.19685)
- [C-World: A Computer Use Agent Environment Creator (arXiv)](https://arxiv.org/pdf/2601.06328)
