---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MiMo代币快速使用指南
translated: true
type: note
---

**问题：** 我的 Pro 月付计划还有 2 天到期，如何在到期前有效使用小米 MiMo 平台令牌？

**回答：**

你的计划已使用 **106M 令牌，总配额 38B** —— 几乎没怎么消耗。还剩 2 天，以下方法能帮你快速完成有价值的工作：

## 现在值得做的高价值事项

### 1. 批量调用 LLM API 处理现有项目

将你的 CLI 代理（`ww`、`iclaw`、`zz`）指向 MiMo 端点，替代 Anthropic/OpenAI。查看其文档中的基础 URL：

**回答：**

已查看文档。API 兼容 OpenAI，因此可立即接入任何工具。

## 快速配置

```bash
export MIMO_API_KEY="your_key_here"
```

基础 URL：`https://api.xiaomimimo.com/v1`
最新模型：`mimo-v2.5-pro`

## 2 天内高效消耗令牌的方法

根据你的背景（CLI 代理、博客、笔记处理管道），以下是实际可做的事：

### 1. 将其接入现有 CLI 代理，作为廉价后端

由于兼容 OpenAI，只需替换 `base_url`：

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MIMO_API_KEY"],
    base_url="https://api.xiaomimimo.com/v1"
)
```

将 `ww`/`zz`/`iclaw` 指向此处而非 OpenAI。若你已使用 OpenAI SDK，无需改动代码。

### 2. 批量处理你的博客文章或笔记

你约有 400 篇博客和 8000 条笔记。可对其批量进行 LLM 处理：

```python
import os, glob
from openai import OpenAI

client = OpenAI(api_key=os.environ["MIMO_API_KEY"], base_url="https://api.xiaomimimo.com/v1")

for post in glob.glob("~/blog/_posts/*.md"):
    with open(post) as f:
        content = f.read()
    resp = client.chat.completions.create(
        model="mimo-v2.5-pro",
        messages=[
            {"role": "user", "content": f"提取关键技术概念并生成 5 道测验题：\n\n{content}"}
        ],
        max_completion_tokens=1024
    )
    print(resp.choices[0].message.content)
```

想法：生成闪卡、提取概念图谱、创建摘要、发现笔记中的空白处。

### 3. 将其用作数学/代码问题的推理模型

MiMo-V2.5-Pro 具备推理能力（`reasoning_content` 字段）。适用于：算法推导、证明检查、你正在学习的 Transformer 数学。

```bash
curl -s -X POST 'https://api.xiaomimimo.com/v1/chat/completions' \
  -H "api-key: $MIMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [{"role":"user","content":"逐步推导交叉熵损失对 logits 的梯度"}],
    "max_completion_tokens": 2048,
    "temperature": 1.0
  }' | jq '.choices[0].message'
```

### 4. 将其接入 Claude Code / Cline / OpenCode

文档中提供了专门的 Claude Code 集成页面。你可将 MiMo 用作代理编程会话的后端——大规模免费消耗令牌。

在 Claude Code 配置中设置：

```json
{
  "api_url": "https://api.xiaomimimo.com/anthropic",
  "api_key": "your_mimo_key",
  "model": "mimo-v2.5-pro"
}
```

### 5. 多模态/音频（如有相关内容）

它支持图像、音频和视频理解。如果你有录制的演讲、代码截图或图表需要处理，现在是时候了。

## TL;DR 优先级排序

1. **在现有代理中替换 base_url** → 在真实工作中立即消耗令牌
2. **通过摘要/问答生成管道批量处理笔记/博客**
3. **运行偏重推理的任务**（数学、架构设计），这些任务通常每令牌费用更高
4. **在 Claude Code/Cline 中配置为后端**，用于代理编程

你还有约 **37.9B 令牌剩余**——即使高强度使用 API，2 天内也消耗不了多少，因此专注于能产生实际价值的任务，而不是为消耗而消耗。

**参考文献：**

- [MiMo API 快速入门](https://platform.xiaomimimo.com/docs/zh-CN/quick-start/first-api-call)
- [MiMo Claude Code 集成](https://platform.xiaomimimo.com/docs/zh-CN/integration/claudecode)
