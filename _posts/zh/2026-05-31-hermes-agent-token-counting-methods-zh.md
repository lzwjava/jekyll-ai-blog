---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes代理令牌计数方法
translated: true
type: note
---

好问题。由于您通过 Anthropic 兼容端点搭配 Claude Code / 代理工具使用 MiMo，令牌计数会像标准 Anthropic API 一样返回在 API 响应的 `usage` 字段中。

**问：** 在 Hermes Agent 中，如何查看输入和输出令牌计数？

**答：**
有几种方式，从内置到自行操作：

---

## 1. 内置功能：`/analytics` 页面

Hermes 的 Analytics 页面位于 `/analytics`，会显示每日令牌使用量图表，包含输入和输出令牌计数。在 Hermes Web UI 中导航至此页面即可。注意：存在一个已知 bug，输入计数远小于输出计数——输入/输出计数在洞察报告中可能显示为颠倒或低估。

---

## 2. 会话文件：`~/.hermes/sessions/`

Hermes 将请求转储存储在 `~/.hermes/sessions/` 中。您可以直接检查它们：

```bash
# 列出所有会话
ls ~/.hermes/sessions/

# 在所有会话中搜索令牌使用情况
grep -r "input_tokens\|output_tokens" ~/.hermes/sessions/ | tail -50

# 以美化格式查看特定会话
cat ~/.hermes/sessions/<session_id>.json | python3 -m json.tool | grep -A5 "usage"
```

每个 API 响应中的 `usage` 对象遵循标准 Anthropic 格式：
```json
{
  "input_tokens": 14200,
  "output_tokens": 843,
  "cache_read_input_tokens": 11500,
  "cache_creation_input_tokens": 0
}
```

---

## 3. 令牌计数对 MiMo Credits 的实际含义

根据文档中的 MiMo 定价表，您可以自行计算 Credits 消耗。以 `mimo-v2.5` 为例：

```python
def credits_used(input_tokens, output_tokens, cache_hit_tokens=0):
    cache_miss = input_tokens - cache_hit_tokens
    credits = (
        cache_hit_tokens   * 2      +   # 2 Credits/token cache hit
        cache_miss         * 100    +   # 100 Credits/token cache miss
        output_tokens      * 200        # 200 Credits/token output
    )
    return credits

# 示例：一次典型的 Hermes 调用
print(credits_used(14000, 800, cache_hit_tokens=11500))
# cache hit: 11500*2=23000, miss: 2500*100=250000, out: 800*200=160000
# Total: 433,000 Credits per call
```

使用 Lite 计划（41 亿 Credits），这意味着约 9,470 次调用后会耗尽配额。这与官方文档中“约 200 个中等复杂度任务”的估算相符（每个任务包含多次调用）。

---

## 4. 关于 Hermes 开销的现实检查

一次典型的 Hermes API 调用的输入主要由以下内容构成：工具定义（约 8K 令牌）、系统提示（约 2–3K 令牌）、SOUL/MEMORY/USER.md（约 1–5K 令牌），以及已加载的技能（约 0–2K 令牌）。对于一个全新的、未激活任何技能的对话，在发送第一条消息之前，输入成本约为 12K–14K 令牌。

因此，对于 MiMo Credits 的计算：假设第一次调用时约 13K 输入令牌主要为缓存未命中，随后在相同会话中的后续轮次则主要为缓存命中。

---

**参考资料：**

- [Hermes Issue #1091 — CLI 中的令牌可见性](https://github.com/NousResearch/hermes-agent/issues/1091)
- [Hermes Issue #4379 — 令牌开销分析](https://github.com/NousResearch/hermes-agent/issues/4379)
- [Hermes Issue #18615 — 输入/输出计数颠倒的 Bug](https://github.com/NousResearch/hermes-agent/issues/18615)
- [减少 Hermes 令牌费用 — LumaDock](https://lumadock.com/tutorials/cut-hermes-token-costs)
