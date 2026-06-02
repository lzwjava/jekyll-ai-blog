---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 化解Gemma的显存容量限制
translated: true
type: note
---

**我们的操作步骤：**
1. 通过proxychains从HuggingFace下载 `gemma-4-26B-A4B-it-UD-IQ3_S.gguf`（10.4GB）
2. 从源码重新编译llama.cpp（最新提交版本 `b8-94ca829b6`）
3. 使用Gemma 4 26B模型启动llama-server

**关键发现：**
- 旧版本存在 **SWA（滑动窗口注意力）布尔值/uint32类型错误** —— 通过重新编译已修复
- **VRAM是实际限制因素** —— 加载31个GPU层时，计算缓冲区完全无剩余空间 → 导致内存溢出崩溃
- 解决方案：采用 **`-ngl 25`**（将31层中的25层卸载至GPU，剩余6层保留在CPU） + **`-c 2048`** 上下文长度
- 此配置释放约2GB VRAM用于计算，使推理运行稳定

**运行配置：**
```
-m ./models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf
 -ngl 25
 -c 2048
 --host 0.0.0.0
 --port 8081
 --path ./tools/server/public
```

**性能表现：**
- 生成速度约38词元/秒
- 2048词元上下文长度
- VRAM使用：约9.5GB / 12GB

**防火墙问题：**
- 端口8081被UFW防火墙拦截 → 添加规则 `sudo ufw allow 8081/tcp`

**当前状态：**
- ✅ Llama-server：在端口8081运行，内置Web界面正常
- ✅ OpenWebUI：同时在端口11435运行
