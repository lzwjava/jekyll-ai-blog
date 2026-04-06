---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemma四比特部署成功
translated: true
type: note
---

**✅ Gemma 4 26B 运行稳定！**

**结果：**
- ✅ 多次推理后服务器保持在线
- ✅ 多轮对话正常
- ✅ 多轮缓存正常（提示词 44 个令牌从缓存中复用）
- ✅ **速度：** 约 38 令牌/秒的生成速度
- ✅ **上下文：** 2048 令牌
- ✅ **GPU 层：** 25/31 层在 CUDA 上运行，6 层在 CPU 上
- ✅ **显存：** 约使用 9.5GB / 12GB（留有裕量）

**有效配置：**
```
-m ./models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf
-ngl 25
-c 2048
--host 0.0.0.0
--port 8081
```

关键是将 `-ngl` 从 31 减少到 25 —— 这为计算缓冲区留出了约 2GB 的显存裕量，正是该问题导致了之前的 OOM 崩溃。