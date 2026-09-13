---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2GB显存AI实验指南
translated: true
type: note
---

**问题：** 在拥有 2 GB VRAM 的显卡上，可以进行哪些 LLM 和 AI 实验？

**答案：**

是的 —— 2 GB VRAM 确实紧张，但你仍然可以进行有意义的实验。以下是实际可行的方案：

---

### ✅ 你可以做的事情

**1. 小型 / 量化 LLM（推理）**

- **Phi-2、Phi-3 Mini**（微软）—— 非常强大的小模型，可通过 4-bit 量化以 GGUF 格式运行（使用 `llama.cpp`）
- **TinyLlama 1.1B** —— 专为在极低配置硬件上运行而设计
- **Qwen 0.5B / 1.5B** —— 轻量级多语言模型
- **Gemma 2B**（量化版）—— 可能在 Q4 量化下适配
- 使用 **llama.cpp** 或 **Ollama** —— 当 VRAM 满时，这些工具会将部分层卸载到 CPU

**2. 嵌入模型**

- `sentence-transformers`（例如 `all-MiniLM-L6-v2`）—— 几乎完全在 CPU 上运行，VRAM 不会成为瓶颈
- 非常适合 RAG（检索增强生成）流程

**3. 视觉 / 多模态（小型）**

- **CLIP**（图像-文本嵌入）—— 非常节省 VRAM
- **ViT-tiny / ViT-small** 用于图像分类

**4. 经典机器学习 / 深度学习**

- CNN、RNN、小型 Transformer 从零训练 —— 对于小批量大小，2 GB 足够
- `scikit-learn`、`XGBoost`、`LightGBM` —— 基于 CPU，完全不需要 VRAM

**5. 微调（需谨慎）**

- 在 tiny 模型（如 GPT-2、DistilBERT）上使用 **LoRA / QLoRA** —— 结合梯度检查点和小批量大小是可行的

---

### ❌ 会遇到困难的情况

- 以全精度运行 7B+ 模型（需要约 14 GB 以上）
- 即使使用 LoRA 微调大型模型（舒适需要至少 6–8 GB）
- Stable Diffusion（SD 1.5 需要约 4–6 GB VRAM）

---

### 🛠 推荐工具栈

| 工具 | 用途 |
| ------ | --------- |
| `llama.cpp` / `Ollama` | 本地运行量化 LLM |
| `Hugging Face Transformers` | 实验 BERT、GPT-2 等模型 |
| `sentence-transformers` | 嵌入与语义搜索 |
| `LangChain` / `LlamaIndex` | 构建 RAG 应用 |
| `PyTorch` | 自定义模型训练 |

---

### 💡 专业建议

将你的 2 GB GPU 与 `llama.cpp` 中的 **CPU 卸载**功能结合使用。像 TinyLlama 或 Phi-3-mini 这样的模型可以将层拆分到 GPU 和 RAM 之间 —— 你既获得 GPU 加速，又无需所有内容都塞进 VRAM。

---

**参考链接：**

- [llama.cpp - 本地运行 LLM](https://github.com/ggerganov/llama.cpp)
- [Ollama - 本地运行模型](https://ollama.com)
- [TinyLlama 模型](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
- [微软 Phi-3 Mini](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct)
- [Sentence Transformers](https://www.sbert.net/)
- [Hugging Face - 量化指南](https://huggingface.co/docs/transformers/main/en/quantization/overview)
