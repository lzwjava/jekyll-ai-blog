---
audio: false
generated: true
image: true
lang: zh
layout: post
title: Qwen ROCm 推理设置进度
translated: true
type: note
---

以下是您当前服务器设置状态的简要总结：

**当前状态**：正在成功将 Qwen 模型下载到 DigitalOcean ROCm 云服务器上进行推理。

**关键要点**：

1. **基础设施**：DigitalOcean MI300X GPU 云服务器（支持 ROCm）已成功配置，并通过 SSH/UJupyter 访问。
2. **模型下载**：最初使用 `wget` 失败（404 错误），但现在通过 `huggingface-cli` 成功下载——目前 Qwen3.5-122B-UD-Q4_K.gguf 文件已完成 88%（35.8/40.4 GB）。
3. **后续步骤**：下载完成后，您需要：
   - 编译支持 ROCm 的推理引擎（很可能是 `llama.cpp`）
   - 验证下载的模型文件完整性
   - 使用 Qwen GGUF 模型配置并运行推理

**结果**：主要障碍（模型下载）已解决，进展顺利。完成后，您将在 AMD MI300X 硬件上进行推理设置。

---

**截图：**

![screenshot](../assets/screenshots/screenshot-20260520-132445.png)
![screenshot](../assets/screenshots/screenshot-20260520-132451.png)
![screenshot](../assets/screenshots/screenshot-20260520-132456.png)
