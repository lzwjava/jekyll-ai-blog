---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek 流水线现已正常工作
translated: true
type: note
---

## 总结

### ✅ DeepSeek LLM 路径现已端到端可用

试验完成：**50个智能体回合，112万输入token，8分钟运行时间**——智能体循环、Docker容器、终端会话和结果收集均与DeepSeek正常协作。任务本身未解决（属"困难"任务，专家预估约240分钟，上限20分钟——用15亿参数级别的聊天模型运行8分钟本就不期望完成），但这属于模型能力问题，而非管道问题。

### 本轮修复内容

**你看到的`BadRequestError`**：DeepSeek的API拒绝litellm的JSON模式`response_format`（"该response_format类型当前不可用"）——仅支持`{"type": "json_object"}`。测试框架误认为DeepSeek支持模式，且从未启用内置回退机制。

**仓库修复内容**（尚未提交）：

| 文件 | 变更 |
|---|---|
| `terminal_bench/llms/lite_llm.py` | 当`BadRequestError`提及`response_format`时，自动使用提示模板回退（模式嵌入提示中）重试 |
| `terminal_bench/utils/parsing.py` | 新增：在JSON解析前移除markdown代码围栏 |
| `terminal_bench/agents/terminus_1.py` + `naive_agent.py` | 通过围栏剥离器解析 |

**已完成**：从修补后的仓库重新安装`tb`工具（`uv tool install --force .`），确保你已安装的`tb`命令包含修复内容。

### 完整会话回顾

1. **基准测试框架已验证**——网络修复后，预言机运行通过（100%）
2. **网络修复**——容器现通过你的mihomo代理路由（`host.docker.internal:7890`，速度提升约30倍）：修补了全部241个任务compose文件，为Docker子网添加ufw规则，修复daemon.json
3. **已推送至你的分支**——`lzwjava/terminal-bench`的`main`分支现包含compose代理提交（`932e446`）
4. **DeepSeek集成**——测试框架现能为拒绝基于模式的`response_format`的提供商优雅回退

### 后续步骤（请指示）
- **提交并推送DeepSeek修复**至你的分支（4个文件）
- **用DeepSeek运行更多任务**——例如用简单任务查看实际通过情况，或小批量测试
- **提高智能体上限**（`--global-agent-timeout-sec`）以延长单任务尝试时间——注意每个困难任务可能消耗100万以上token

需要我现在提交/推送DeepSeek修复吗？