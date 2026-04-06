---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemma 4 12GB显存服务器崩溃
translated: true
type: note
---

以下为完整摘要：

---

**模型下载 ✅**
- 通过proxychains从HuggingFace下载`gemma-4-26B-A4B-it-UD-IQ3_S.gguf`（10.4GB）
- 文件位置：`/home/lzw/projects/llama.cpp/models/`

**运行环境：**
- **GPU：** RTX 4070（12GB显存）
- **显存占用：** ~10.7GB（已卸载31/31层）
- **上下文长度：** 512个词元（受显存限制达到最大值）
- **量化方式：** IQ3（4位带质量优化）
- **llama.cpp版本：** b1-25eec6f32

**问题：**
服务器在每次推理后崩溃——处理完一个请求后即正常退出。这似乎是当前版本llama.cpp与Gemma 4架构配合时出现的内存管理或SWA（滑动窗口注意力）缺陷。在仅512词元的上下文长度下，简单提示能正常工作，但生成较长输出时会触发内存溢出或崩溃。

**现状：**
服务器目前处于停止状态。每次使用前需重启，或可尝试以下方案：
1. 换用其他GGUF变体（例如采用Q4_K_M替代IQ3_S）
2. 修补/更新llama.cpp至新版构建
3. 减少`-ngl`层数以释放更多显存用于计算缓冲

**API：** `http://localhost:8081`——支持OpenAI兼容的`/v1/chat/completions`端点。