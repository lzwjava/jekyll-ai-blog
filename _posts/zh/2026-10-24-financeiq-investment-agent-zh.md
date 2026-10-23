---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FinanceIQ投资代理
translated: true
type: note
---

完成。**FinanceIQ** 已端到端构建、测试并提交。

## 你得到的内容

```
finance_agent/
  agent.py      LlamaIndex FunctionAgent + grounding system prompt
  tools.py      search_market_news (Tavily) · get_company_news · get_stock_quote (yfinance) · get_market_indices
  llm.py        DeepSeekLLM — OpenAI-compatible adapter for llama-index
main.py         CLI: one-shot or interactive chat
README.md · requirements.txt · .env.example · .gitignore
```

## 工作原理

LlamaIndex **FunctionAgent**（以 DeepSeek `deepseek-chat` 作为推理 LLM）通过以下方式回答投资问题：**③ 搜索实时新闻 2–3 次**（宏观、行业板块，外加 `site:finance.yahoo.com` 查询）→ **② 获取每个候选股票代码的实时报价** → **③** 返回结构化报告 — 市场概况、3–5 个投资想法（论点与引用的头条新闻、催化剂、风险、仓位规模、时间范围挂钩）、一份“需警惕”清单，以及免责声明。

## 实测验证

运行了完整会话：它捕捉到了 AI 基础设施抛售、中东局势升级导致原油价格 >100 美元、以及 10 年期收益率达到 5%；推荐了能源（XLE/CVX/SLB）、因错位而看好的 NVDA、公用事业（XLU）和黄金（GLD）——每项都附有实时报价水平（例如 CoreWeave 下跌约40%，被标记为重大风险）。两种模式均已测试：

```bash
python3 main.py "What should I invest in today?"    # one-shot
python3 main.py                                     # interactive chat
```

## 一个重要决定

你要求使用 **LLM API 的原生网络搜索** — 我测试了你环境中的所有选项：`OPENAI_API_KEY` 被 api.openai.com **拒绝**，`ANTHROPIC_API_KEY` 为**空**（并且 sssaicode Claude 中继拒绝第三方客户端），而 **Gemini** 密钥可用但**额度已耗尽**。DeepSeek/Groq 不提供原生网络搜索。因此我接入了行业标准的替代方案 — **Tavily**（你环境中的 `TAVILY_API_KEY`）— 作为该代理的搜索工具。如果你之后获得有效的 OpenAI/Anthropic 密钥，换成它们原生的网络搜索工具只需改动 10 行代码。