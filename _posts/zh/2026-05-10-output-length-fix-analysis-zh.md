---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 输出长度修复分析
translated: true
type: note
---

以下是我修复的完整回顾。

---

## 根本原因分析

错误：LLM 返回了 1518 个字符，而不是一个 6 个单词的标题。两个问题同时发生：

1. 模型忽略了“仅返回标题”的指令，生成了一篇包含分析和要点列表的长篇回复。
2. 代码将此视为致命错误——直接 `raise ValueError`，没有重试机制。

模型为何会跑题？有两个相互叠加的原因：

- **没有 `max_tokens` 限制。** 在 `generate_title` 中调用 API 时，通过 `_call_llm_or_exit` -> `call_openrouter_api`，`max_tokens=None`。模型在输出长度上没有硬性约束。有些模型（尤其是较弱或“话多”的模型）将“只回复 X”视为建议而非规则。
- **提示词结构不佳。** 旧提示词是一长句话：*"Generate a very short title in English (maximum six words, do not have single quote) for the following text and respond with only the title: {content}"*。这是一个命令式指令，嵌在与内容相同的文本块中。许多模型处理不好——它们看到内容后“受到启发”，在想起指令之前就开始生成分析。

---

## 我的修复步骤

### 步骤 1：在 API 调用中设置 `max_tokens` 上限（硬性防护）

**文件：** `create_note_utils.py`
**改动：** 通过 `_call_llm_or_exit` 向 `call_openrouter_api` 传递 `max_tokens=60`。

**原因：** 这是最可靠的修复。即使模型试图长篇大论，API 也会在大约 60 个 token 后截断输出。对于一个 6 个单词的标题，60 个 token 已经足够宽裕（6 个单词大约 8-10 个 token）。token 限制在 API 层面强制执行——任何模型都无法绕过。这是一个无论模型行为如何都能起作用的保障。

**我需要修改的地方：** `_call_llm_or_exit` 之前不接受 `max_tokens` 参数。我添加了 `max_tokens=None` 作为可选参数，并将其转发给 `call_openrouter_api`。这保持了向后兼容性——所有其他未传递 `max_tokens` 的调用者仍然得到 `None`（无限制）。

### 步骤 2：添加重试逻辑（弹性）

**文件：** `create_note_utils.py`
**改动：** 将标题生成包裹在重试循环中（3 次尝试）。如果标题长度 >= 100 个字符，则打印警告并重试。仅在 3 次失败后抛出 `ValueError`。

**原因：** 旧代码采用“快速失败”方法——一次不良的 LLM 响应就导致整个 `ww note` 命令崩溃。LLM 输出是非确定性的。重试成本很低（再多一次 API 调用，大约 $0.001），而且通常能成功，因为模型每次输出不同。警告消息也让用户知晓发生了异常。

**设计选择：** 我选择了 3 次重试。太少（1 次）就是现有情况。太多（10 次）会在提示词本身有问题的情形下默默浪费时间和金钱。3 次是瞬态故障的标准重试次数。

### 步骤 3：强化提示词（软性防护）

**文件：** `create_note_from_clipboard.py`
**改动：** 将提示词从：
```
Generate a very short title in English (maximum six words, do not have single quote)
for the following text and respond with only the title: {content}
```
改为：
```
Give a short English title (at most 6 words, no quotes, no explanation) for:
{content}

Title:
```

**这里改了两个地方：**

1. **明确要求“不要解释”。** 旧提示词说“仅返回标题”，但没有说明模型为何可能想添加额外文本。有些模型将“仅返回 X”理解为格式偏好而非禁止。“no explanation”更直接地指出不该做什么。

2. **末尾的 `\n\nTitle:` 引导。** 这是更大的改动。通过在提示词末尾添加 `Title:`，我采用了补全风格的引导。模型看到一个部分完成的响应，自然就会接着只输出标题文本。对于大多数模型，这比命令式指令效果好得多——它利用了下一个 token 预测的工作原理。模型不需要“决定”是否遵循指令，它只是完成模式。

---

## 我未修复的部分（及其原因）

- **未添加系统消息。** `call_openrouter_api` 函数只支持单条用户消息（没有 `system` 角色）。添加系统消息支持需要修改客户端接口，这个重构规模过大。`max_tokens` + 提示词修复已经足够。

- **未对 `generate_short_title` 做类似修复。** 该函数使用不同的提示词，且不太可能跑题（它从一个已有标题生成一个 4 个单词的文件名 slug，而非从原始内容生成）。如果将来出现问题，可应用相同的模式。

- **未做模型特定的变通。** 修复与模型无关。无论通过 `MODEL` 环境变量配置了什么模型，`max_tokens=60` 和引导式提示词都会起作用。

---

## 修复效果评估

**优势：**
- 纵深防御：提示词（软性）+ max_tokens（硬性）+ 重试（弹性）
- 向后兼容：`_call_llm_or_exit` 默认 `max_tokens=None`
- 代码改动量小：总共约 15 行

**剩余风险：**
- 如果模型输出了 60 个 token 的垃圾内容，且恰好少于 100 个字符，重试循环不会捕捉到（字符检查通过，但标题无意义）。这种情况概率较低，需要语义检查，但对当前用例来说过度设计。
