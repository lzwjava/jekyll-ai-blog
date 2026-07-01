---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 比较DeepSeek-V4-Pro与GLM-5.1上下文窗口
translated: true
type: note
---

**问题：** DeepSeek-V4-Pro 的上下文窗口（100万 token）是否比 GLM-5.1 的上下文窗口（约22万 token）更大？

**回答：**

是的，**DeepSeek-V4-Pro 的上下文窗口明显大于 GLM-5.1**，但你对 GLM-5.1 的估计的数字略有偏差——它约是20万 token，而非约22万 token。

---

### DeepSeek-V4-Pro 上下文窗口

DeepSeek-V4-Pro 是一种混合专家模型，总参数量为1.6万亿（激活参数490亿），支持**100万 token** 的上下文长度。

此前 DeepSeek 模型（V3 和 V3.1）的上限为12.8万 token——V4 的100万 token 窗口是一项重大飞跃。

---

### GLM-5.1 上下文窗口

GLM-5.1 支持 **20万 token** 的上下文窗口，约相当于400页文本。单次回复可生成多达12.8万 token。

更精确地说，GLM-5.1 的确切上下文窗口为 **202,752 token**，因此你估算的约22万略高——它更接近约20万。

---

### 直接对比

| 模型 | 上下文窗口 | 参数量（总参数 / 激活参数） |
| --- | --- | --- |
| **DeepSeek-V4-Pro** | **1,000,000 token（100万）** | 1.6T / 49B |
| **GLM-5.1** | **~202,752 token（约20万）** | 754B / 40B |

DeepSeek-V4-Pro 的上下文大约是 GLM-5.1 的 **5 倍**。

---

### 你在界面中看到的显示

你看到的 `27K/1M` 表示当前对话已使用约2.7万 token，而 DeepSeek-V4-Pro 的可用上下文为100万 token。这仅使用了3%（如进度条所示），与100万 token 的限制完全一致。

**参考资料：**

- [Hugging Face 上的 DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)
- [DeepSeek V4 上下文窗口详解](https://framia.pro/page/en-US/news/deepseek-v4-context-window)
- [GLM-5.1 规格 – Puter Developer](https://developer.puter.com/ai/z-ai/glm-5.1/)
- [OpenRouter 上的 GLM-5.1](https://openrouter.ai/z-ai/glm-5.1)
