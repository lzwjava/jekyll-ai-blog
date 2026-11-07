---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 移除大型仓库以释放空间
translated: true
type: note
---

现在一切都清楚了。当前情况总结：

- **磁盘已100%满** — 460 GB空间中仅剩 **217 MB**
- `~/projects` 目录下 **167个已配置仓库中的166个** 共占用 **75 GB**
- 删除目录对 `ww projects update` 来说是安全的（缺失的目录会被跳过），但 `ww projects init` 会从 `repos.json` 重新克隆——因此我也应从配置中移除相关条目以永久释放空间。

以下是占用空间最大的仓库（已排序，均超过700 MB）：

| 仓库 | 大小 |
|---|---|
| Qwen2.5-Coder | 3.5 GB |
| TensorRT-LLM | 3.0 GB |
| openai-cookbook | 1.8 GB |
| evals | 1.6 GB |
| greptimedb | 1.5 GB |
| litellm | 1.2 GB |
| bun | 1.2 GB |
| claw-code | 1.2 GB |
| weaviate | 1.2 GB |
| nanochat | 1.0 GB |
| llama_index | 911 MB |
| llama.cpp | 872 MB |
| Telegram-iOS | 833 MB |
| crewAI | 826 MB |
| pytorch | 823 MB |
| AutoGPT | 797 MB |
| warp | 752 MB |
| LibreChat | 747 MB |
| mlflow | 740 MB |
| vortex | 670 MB |
| hermes-agent | 664 MB |
| open-webui | 577 MB |

我的计划：删除这些 **前约22个仓库（超过500 MB）从磁盘，并从 `repos.json` 中移除**——可释放约27 GB。注意这包括占用较大的 `pytorch` 和 `llama.cpp` 等；如果你希望保留它们请告知。

请确认要移除哪些？回复：
- **`yes`** → 移除所有超过500 MB的仓库（释放约27 GB）
- **`top10`** → 仅移除最大的10个（释放约16.5 GB）
- 或告诉我需要保留/排除的名称