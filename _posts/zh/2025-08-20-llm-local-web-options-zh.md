---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 轻量级本地大语言模型网页客户端选择
translated: true
type: note
---

如果你正在寻找比 Open WebUI 更轻量、依赖更少的本地运行 LLM 的开源网页客户端，以下是一些优秀替代方案：

**1. Lobe Chat**

- 轻量可扩展的聊天客户端，支持本地与远程 LLM。具备插件系统和简洁界面，可通过 Docker 或直接运行。以简单配置和与 Ollama 等后端良好兼容著称。

**2. LM Studio**

- 支持 GGUF 格式模型（如 Mistral、Phi 3、Gemma）的桌面应用程序，提供直观易用的界面。适合快速本地推理，无需复杂配置或大量依赖。

**3. text-generation-webui (Oobabooga)**

- 基于 Gradio 的多功能网页界面，支持多种后端（transformers、GPTQ、AWQ、EXL2、llama.cpp）。虽配置稍复杂，但高度可定制，被广泛使用。

**4. AnythingLLM**

- 多功能自托管聊天界面，兼容本地与云端模型。提供桌面版应用，兼具灵活性与相对轻量的特性。

**5. Jan**

- 跨平台离线聊天界面，支持拖拽定制与预制模板。针对性能优化且兼容多 LLM API，适合注重隐私的用户。

**6. Ollama UI**

- 专为 Ollama 设计的极简界面，部署简便，适合已使用 Ollama 进行模型服务的用户。

**7. Open-LLM-WebUI**

- 简洁开源网页界面，专为本地运行轻量 LLM 设计。以开箱即用和最小化配置为特色。

**对比表格：**

| 客户端                 | 核心特性                              | 配置复杂度        | 适用场景               |
|------------------------|---------------------------------------|-------------------|------------------------|
| Lobe Chat              | 插件系统、Docker 支持、简洁界面       | 低                | 通用场景、Ollama 用户  |
| LM Studio              | 桌面应用、GGUF 支持、直观界面         | 极低              | 快速本地推理           |
| text-generation-webui  | 多后端支持、高度可定制                | 中等              | 进阶用户               |
| AnythingLLM            | 桌面应用、灵活通用                    | 低                | 本地/云端混合部署      |
| Jan                    | 离线功能、拖拽定制、模板库            | 低                | 隐私保护、个性化需求   |
| Ollama UI              | 极简设计、Ollama 专属                 | 极低              | Ollama 生态用户        |
| Open-LLM-WebUI         | 轻量简洁                              | 低                | 轻量级 LLM 运行        |

若追求极致轻量，**LM Studio** 或 **Ollama UI** 是最佳起点；如需更丰富功能，**Lobe Chat** 或 **text-generation-webui** 是理想选择。

需要了解具体配置方案或特定使用场景的详细指导吗？
