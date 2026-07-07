---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 服务器状态与限制
translated: true
type: note
---

## 综合状态

### 服务器硬件

| 资源 | 规格 | 限制 |
| ---------- | ------ | ------------ |
| **GPU** | RTX 2000 Ada, 16 GB 显存, CC 8.9 | 可运行 7-8B FP16 或 30B-34B INT4 模型 |
| **CPU** | AMD EPYC 7443, 48 线程 | 良好 |
| **RAM** | 251 GB | 良好 |
| **/dev/shm** | 14 GB tmpfs | 有限制 — 在模型下载期间已填满 |
| **/workspace** | 2.1 PB MooseFS FUSE | **约 10 GB 配额** — 瓶颈 |

### 已安装软件

| 组件 | 版本 | 状态 |
| ----------- | --------- | -------- |
| **SGLang** | 0.5.14 | ✅ 已安装，支持 `gemma4_causal` |
| **SGLang 内核** | 0.4.4 | ✅ 运行正常（需要设置 `LD_LIBRARY_PATH` 以调用 CUDA 13 库） |
| **Python** | 3.11.10 | ✅ |
| **CUDA** | 12.4（驱动 580 — CUDA 13.0） | ✅ |
| **Node.js** | 22.23.1 | ✅ 已安装 |
| **MongoDB** | 7.0.37 | ✅ 在端口 27017 上运行 |
| **LibreChat** | 最新版 | ✅ 已克隆至 `/workspace/LibreChat/` |

### 模型下载状态：Gemma 4 26B A4B AWQ（cyankiwi）

| 分片 | 大小 | 状态 |
| ------- | ------ | -------- |
| `model-00001-of-00004.safetensors` | 5.1 GB | ✅ 完成 |
| `model-00002-of-00004.safetensors` | 2.1 / 5.1 GB | ❌ 部分 |
| `model-00003-of-00004.safetensors` | 1.5 / 5.1 GB | ❌ 部分 |
| `model-00004-of-00004.safetensors` | 0 / 1 GB | ❌ 缺失 |

**模型总大小：约 20 GB。工作区配额：约 10 GB。** — 不兼容。

### 真实限制

RunPod 网络卷（`/workspace`）具有**每个 pod 约 10 GB 的配额**。此配额由 MooseFS FUSE 服务器强制执行，并非文件系统本身（显示 328 TB 可用空间）。一旦写入量累积超过约 10 GB，所有新写入都会失败，并提示 `EDQUOT（超出磁盘配额）`。这是**服务器端配额**——我无法在 pod 内部覆盖该限制。

清理旧文件（SEC-EDGAR-GPT 模型、pip 缓存、llama.cpp 工件）释放了足够空间用于部分下载，但完整的 20 GB 模型根本无法容纳。

### 可行的方案

**目前可行的两种方法：**

1. **提供一个小型 AWQ 模型** — 可容纳在 10 GB 配额内。例如：
   - `Qwen2.5-7B-Instruct-AWQ`（约 4 GB）— 质量不错，有较大余量
   - `Qwen2.5-14B-Instruct-AWQ`（约 8 GB）— 质量更好，空间紧凑
   - 支持 128K 上下文，编程和推理能力强

2. **增加卷配额** — 如果您在 RunPod 仪表板中将配额提升至 20+ GB，我可以干净地重新下载 Gemma 4 26B A4B AWQ 并提供服务。

### 模型就绪后仍需完成的工作

无论选择哪种模型，后续设置步骤如下：

1. **启动 SGLang 服务器** — 在端口 30000 上提供模型，支持 OpenAI 兼容 API
2. **配置 LibreChat** — 编写 `.env` 文件，包含 `MONGO_URI`，并配置 `librechat.yaml`，将 SGLang 端点指向自定义 OpenAI 提供商
3. **构建 LibreChat** — 执行 `npm run frontend`
4. **启动 LibreChat** — 执行 `npm run backend`
5. **访问** — LibreChat 在端口 3080 上运行，配置为使用本地 SGLang 模型

选择哪条路径？选项 1（现在使用小模型）还是选项 2（增加配额以使用 Gemma 4）？
