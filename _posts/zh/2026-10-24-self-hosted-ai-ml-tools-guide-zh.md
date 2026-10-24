---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自托管AI与ML工具指南
translated: true
type: note
---

问：关于自托管开源人工智能和机器学习工具的详细内容有哪些？

---

回答：

以下是按子类别的详细细分：

---

### 🧠 1. LLM 运行器与模型推理
*在您自己的硬件上运行开放权重模型（Llama, Mistral, DeepSeek, Qwen）。*

| Tool | Description |
|---|---|
| **Ollama** | 在本地运行 LLM 的最简单方式 —— 单命令拉取并运行，MIT 许可，无使用限制 |
| **LocalAI** | 在本地运行的 OpenAI 兼容 API 服务器；支持 GPU 和 CPU；每月 0 美元，无限制使用 |
| **LM Studio** | 最精致的 GUI，在 Apple Silicon 上表现最佳 *（注：桌面应用为闭源）* |

Meta 的 **Llama 4 Scout** 在 2025-2026 年间将 1000 万 token 的上下文窗口带到了开源领域，而 **Tabby** (Apache 2.0) 则为受知识产权限制的团队提供了自托管的 GitHub Copilot 替代方案。

---

### 💬 2. AI 聊天界面
*连接到你本地或远程 LLM 的 ChatGPT 风格前端。*

| Tool | GitHub ⭐ | Description |
|---|---|---|
| **Open WebUI** | 150k+ | 功能丰富的自托管 AI 界面，集成了 Ollama 和 OpenAI 兼容 API，支持 RAG、向量数据库、图像工具、RBAC 和可观测性。 |
| **LibreChat** | — | 自托管 AI 聊天平台，支持多种 LLM 提供商、自定义端点、智能体/工具、文件和图像聊天、对话搜索和预设。 |
| **AnythingLLM** | 65k+ | 一体化的桌面和 Docker 应用，用于使用 RAG 与文档聊天、运行 AI 智能体，并连接到本地或托管式 LLM 及向量数据库。 |
| **Perplexica** | — | 可自托管的个人 AI “第二大脑”，用于聊天、语义搜索、自定义智能体、自动化以及与本地或云端 LLM 的集成。 |

---

### 📚 3. RAG 与知识库（与你的文档对话）
*构建管道，针对你自己的文档进行提问。*

一个完整的自托管 RAG 堆栈使用开源组件运行：对象存储保存源文档，一个小的 API 服务协调检索和生成 —— 整个管道可以在普通基础设施上运行，而无需依赖受管理的 AI 平台。

| Tool | Description |
|---|---|
| **Dify** | 开源 LLM 应用平台，拥有最完整的内置 RAG 引擎之一，具有用于链接检索→重排序→LLM 生成的视觉工作流构建器。通过 Docker 免费提供自托管的社区版。 |
| **Flowise** | 基于 LangChain 的 RAG 管道的开源可视化构建器。通过 Docker 自托管部署，拥有完全的数据主权。 |
| **LangChain** | 支持几乎所有 LLM 提供商、所有向量数据库和所有检索模式 —— 与 100 多个 LLM 提供商、50 多个向量数据库和 50 多个文档加载器集成。 |

---

### 🗄️ 4. 向量数据库
*RAG 系统中嵌入（embedding）的存储层。*

对于 RAG，向量数据库作为知识存储，将 LLM 的回复基于你的特定数据 —— 当用户提出问题时，系统将查询转换为向量，找到最相似的文档，并将该上下文提供给 LLM。

| Tool | Best For | License |
|---|---|---|
| **Chroma** | 原型开发 | 开源 / 免费 |
| **Qdrant** | 生产自托管 | 开源 / 免费 |
| **Weaviate** | 混合搜索（结合向量相似性与关键词匹配） | 开源 / 免费 |
| **Milvus** | 大规模企业级，亚 10 毫秒延迟 | 开源 / 免费 |
| **pgvector** | 已在使用 PostgreSQL 的团队 | 开源 / 免费 |

---

### 🎨 5. AI 图像生成
*根据文本提示生成图像，完全在本地完成。*

Stable Diffusion 是一个开源 AI 模型，可根据文本描述生成逼真的图像、插画、概念艺术和设计。在本地运行它可以带来以下好处：免费（无需订阅）、私密（提示和图像保留在你的机器上）且无限制生成 —— 在现代 GPU 上每张图像只需 2–10 秒。

| Tool | Best For |
|---|---|
| **AUTOMATIC1111 WebUI** | 初学者和扩展用户 —— 最简单的设置 |
| **ComfyUI** | 使用可视化节点图编辑器构建高级 AI 图像工作流程，支持 ControlNet、LoRA、自定义节点和 FLUX |
| **InvokeAI** | 想要精致现代界面的团队 |
| **Fooocus** | 为内容创作者提供最快速、最省心的图像生成 |

---

### 🤖 6. AI 智能体与工作流程自动化

| Tool | Description |
|---|---|
| **n8n** | 一个强大的 Zapier 和 Make 自托管替代方案，带有 AI 智能体节点 |
| **Activepieces** | 开源 Zapier 替代方案，具备 AI 能力，免费自托管 |

---

### 🔬 7. LLM 可观测性与 MLOps
*监控、调试和改进你的 AI 应用。*

| Tool | Description |
|---|---|
| **Langfuse** | 开源 LLM 可观测性 —— 追踪提示、成本和评估指标 |
| **Label Studio** | 领先的开源 ML 数据标注工具，包括 LLM RLHF 工作流程 |

---

### 💻 8. AI 编码助手

| Tool | Description |
|---|---|
| **Tabby** | 为受 IP 限制的团队提供的自托管 GitHub Copilot 替代方案 (Apache 2.0) |
| **Continue** | 开源智能体编码助手，适用于 VS Code，安装量超过 4M (Apache 2.0) |

---

### 🐦 9. 专业化 / 细分 AI 工具

| Tool | Description |
|---|---|
| **Frigate** | 具有本地物体检测功能的 AI 摄像头监控 |
| **Immich** | 自托管照片和视频管理器，使用本地 AI（人脸识别、OpenCLIP 语义搜索、重复检测）来组织和探索媒体 |
| **BirdNET** | 用于分析音频中鸟类叫声的机器学习工具 —— 使用本地 ML 模型从录音中识别鸟类物种 |

---

> 💡 **快速入门提示：** 最常见的堆栈是 **Ollama**（模型运行器） + **Open WebUI**（聊天界面） + **Qdrant**（向量数据库） + **Dify 或 Flowise**（RAG 管道构建器）。这四种工具都可以在 Docker 上运行，并且可以在 GPU 服务器上在一小时内启动并运行。

---

**参考：**
- [2026 年最佳自托管 AI 工具 – Elest.io](https://landing.elest.io/best-self-hosted-ai-tools)
- [最佳自托管 AI 与 ML 工具 – SelfHostYourself](https://selfhostyourself.com/categories/ai-machine-learning)
- [2026 年构建 AI RAG 应用的 7 个最佳工具 – Momen](https://momen.app/blogs/7-best-tools-to-build-ai-rag-applications-in-2026/)
- [2026 年 LLM 应用十大向量数据库 – SecondTalent](https://www.secondtalent.com/resources/top-vector-databases-for-llm-applications/)
- [自托管 101：部署 Stable Diffusion – Stability AI](https://kb.stability.ai/knowledge-base/self-hosting-101-deploying-stable-diffusion-models)
- [2026 年最佳开源 AI 工具 – Fast.io](https://fast.io/resources/best-open-source-ai-tools-2026/)