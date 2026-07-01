---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Qwen 3.5服务器部署故障排除
translated: true
type: note
---

好的，这是翻译后的内容：

---

## 🦞 完整回顾：在服务器上运行 Qwen 3.5 9B

### 目标

在本地服务器 (RTX 4070, 62GB RAM) 上下载并运行 `aravhawk/qwen3.5-opus-4.6:9b`。

### 过程

**1. 模型下载 (~90 分钟)**

- 通过 Ollama 拉取：5.6 GB 主层 + 921 MB 次要层
- 速度极不稳定：开始为 3.5 MB/s，有时降至 90 KB/s
- 模型文件为 GGUF Q4_K-M 量化版，5.23 GB，架构为 `qwen35` (混合 SSM+Attention)

**2. Ollama 无法加载模型**

- 服务器 Ollama 版本 v0.18.2 — 对于 `qwen35` 架构来说太旧了
- 报错：`unknown model architecture: 'qwen35'`
- 需要 v0.20.2+ 版本
- 尝试更新 Ollama — 从该服务器访问 GitHub 下载速度约 30 KB/s。所有尝试均失败或超时
- 安装脚本 (`curl | sh`) 在 0.6% 时中断并被终止

**3. 转向 llama.cpp**

- 在 `~/projects/llama.cpp` 找到现有的 llama.cpp 构建，但其版本为 2025 年 10 月 — 同样不支持 `qwen35`
- 没有代理时，git fetch 速度也极其缓慢
- **关键突破：** 使用端口 7890 上的 Mihomo 代理 — 为 git 设置 `http.proxy`/`https.proxy` 后，拉取速度飞升
- 通过代理执行 `git fetch origin master`，然后 `git reset --hard origin/master`
- 新代码已支持 `qwen35` (在 `llama-arch.cpp` 第 42 行添加)
- 使用 CUDA 支持从源码重新构建 llama-server (`cmake .. -DGGML_CUDA=ON`)
- 构建成功完成

**4. 首次启动 — 仅限 CPU**

- CUDA 驱动 (535) 对于 CUDA 13.2 工具包来说太旧：`CUDA driver version is insufficient for CUDA runtime version`
- 回退至 CPU：32 线程，约 10 tok/s
- 模型加载正常，通过 OpenAI 兼容的 API `http://127.0.0.1:11435` 正确响应

**5. 驱动升级 (nvidia-driver-535 → 570)**

- 旧驱动：535.288.01 (支持至 CUDA 12.2)
- 新驱动：570.211.01 (支持 CUDA 13.2)
- DKMS 内核模块为 6.8.0-106 和 6.8.0-107 内核构建完成
- **需要重启** 以加载新的内核模块

### 当前状态

| 组件 | 状态 |
| ----------- | -------- |
| 模型文件 | ✅ 已下载 (5.23 GB GGUF) |
| llama.cpp | ✅ 已更新并重新构建 (最新 master) |
| llama-server | ⏸️ 驱动升级前已终止 |
| NVIDIA 驱动 | ✅ 已安装 570.211.01 (需要重启) |
| GPU 卸载 | 🔜 重启后启用 |

### 重启后

使用以下命令启动服务器：

```bash
LD_LIBRARY_PATH=~/projects/llama.cpp/build/bin \
  ~/projects/llama.cpp/build/bin/llama-server \
  -m /usr/share/ollama/.ollama/models/blobs/sha256-d0ecd80b0e45b0d9e49c8cd1527b7f7d52d8d3bde2c569ab36aac59bb78f53f7 \
  -ngl 99 -c 8192 --host 0.0.0.0 --port 11435
```

预期：RTX 4070 上所有 32 层卸载后，速度约 60-100+ tok/s。

### 经验教训

- **无代理情况下，从该服务器访问 GitHub 几乎不可用** — 裸连约 30 KB/s，使用 7890 端口上的 mihomo 代理则瞬间完成
- **Ollama 的版本管理是个痛点** — 每个新的模型架构都需要特定版本的 Ollama
- **llama.cpp 更稳健** — 只需从源码重新构建即可工作
- **CUDA 驱动/工具包版本不匹配** 是经典陷阱 — 务必检查 `nvidia-smi` 的 CUDA 版本与 `nvcc --version` 的版本

---

现在重启，让我们见证它起飞 🦞
