---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM否决计划的三个软肋
translated: true
type: note
---

**问题：** 你对这个计划的评估如何——保持交易机器人的信号机械化，但增加每小时一次的 LLM 新闻读取作为否决层，并生成报告？

**回答：**

分析的方向是正确的——纯否决，绝不发起，是合理的架构。但它有三个薄弱点，在构建之前值得修复。

**1. 否决同样是不可回测的——分析对其自身的批评应用得不均**

它说“LLM 决定”版本失败，因为你无法回测它。这是对的。但“LLM 在三月会否决什么”同样无法回答。否决是*有界风险*的不可回测，而非无界，这更好一些，但你仍然不知道它是否有帮助。修复方法很简单：先以影子模式发布。

```python
# bot/llm_veto.py
import re, json, time

VETO_RE = re.compile(r"^\s*(SAFE|VETO)\b", re.I)

def check_news_veto(symbol: str, shadow: bool = True) -> dict:
    prompt = (
        f"过去24小时内是否有任何关于{symbol}的重大公司特定新闻——"
        "财报、业绩指引下调、诉讼、降级、欺诈？"
        "回复的第一个词必须是 SAFE 或 VETO，然后给出一个简短理由。"
    )
    try:
        text = "".join(stream_openrouter_api(prompt, model=MODEL, max_tokens=100))
        m = VETO_RE.match(text)
        decision = m.group(1).upper() if m else "VETO"  # 无法解析 -> 保守处理
    except Exception as e:
        text, decision = f"ERROR: {e}", "VETO"           # API 宕机 -> 跳过入场

    record = {"ts": time.time(), "symbol": symbol, "decision": decision,
              "raw": text, "shadow": shadow}
    with open("veto_log.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")

    return {"veto": (decision == "VETO") and not shadow, "record": record}
```

使用 `shadow=True` 运行 4-6 周：机器人像 LLM 不存在一样进行交易，但记录每次决策。然后将 `veto_log.jsonl` 与实际交易盈亏关联，并问一个问题：*被否决的入场是否跑输了未被否决的？* 如果是，翻转标志。如果否，你就避免了一个有损的过滤器。这会将信念转化为可衡量的组件——与你应用于任何评估的纪律相同。

**2. “错误答案只会使其更保守”对风险成立，但对优势不成立**

均值回归的利润*就是*买入恐惧。一个 2 西格玛的下跌通常伴随着一个吓人的标题——这就是价格下跌的原因。一个否决所有耸人听闻标题的 LLM 会优先否决那些定价了最多恐惧的交易，而这些交易可能正是盈利的。过度否决不会炸毁账户；它会悄悄将优势消耗为零，同时看起来非常审慎。影子模式的数据能凭经验回答这个问题，但也要收紧提示词：你希望它否决*体制性*新闻（财报不及预期、业绩指引下调、欺诈、退市风险），而不是*情绪性*新闻（“分析师担忧……”）。在提示词中明确列出否决类别，并告诉它其他所有情况都是 SAFE。

**3. 财报过滤器根本不应该使用 LLM**

财报日期是结构化、预定、公开的数据。日历查询是确定性的、免费的、可回测的，并且永远不会产生幻觉——LLM 调用在这个任务上绝对更差。Alpaca 的 API 公布了公司行为，Finnhub/FMP 有免费的财报日历端点：

```python
import requests, datetime as dt

def has_earnings_today(symbol: str, api_key: str) -> bool:
    today = dt.date.today().isoformat()
    r = requests.get("https://finnhub.io/api/v1/calendar/earnings",
                     params={"from": today, "to": today, "symbol": symbol,
                             "token": api_key}, timeout=10)
    return bool(r.json().get("earningsCalendar"))
```

将 LLM 用于真正非结构化的部分（突发新闻解读），使用无聊的查找来处理结构化事实。每个层级使用正确的工具。

**另外两个加固要点**

- **提示注入面。** 使用 `:online` 模型时，LLM 会摄入可能包含指令的任意网络文本。上面严格的输出约定（第一个 token 是 `SAFE|VETO`，其他一律视为 VETO）意味着注入页面能造成的最坏结果是跳过交易——绝不会触发交易。保持这样：否决函数必须返回布尔值，下游任何逻辑都不应解析理由文本来执行操作。
- **固定并记录一切。** 固定模型字符串，设置 `temperature: 0`，记录原始响应。当三周后否决看起来有问题时，你需要能重放精确的输入/输出，而不是猜测。

所以：否决加报告是可行的，但影子模式是强制性的第一阶段；不采用基于 LLM 的财报检查。分析中的硬规则仍然成立——LLM 可以说否，永远不能说是——影子日志最终会告诉你这些“否”是否值得其误报成本。
