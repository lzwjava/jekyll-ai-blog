---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash-Attn构建调试与修复
translated: true
type: note
---

## 我在 lzw@192.168.1.36 上做的事

### 1. 诊断构建失败

- 检查是否有正在运行的 flash-attn 构建 — 没有运行，之前的尝试已终止
- 在 /tmp 中发现 104 个来自失败构建的孤立 CUDA 临时文件 (`tmpxft_*`)
- 根本原因：**磁盘已满 98%**（916GB 中仅剩 19GB 可用）
- 仅 pip 缓存就占用了 15GB

### 2. 释放磁盘空间

- `pip cache purge` — 移除了 3,530 个缓存文件（约 16GB）
- 清理了 /tmp 中的 CUDA 工件和 pip 安装目录
- 结果：可用空间从 19GB 增加到 35GB

### 3. 第一次构建尝试（失败的方法）

- 在 tmux 会话 `flash-build` 中开始构建
- 设置 `TORCH_CUDA_ARCH_LIST="8.9"` — flash-attn **忽略了它**
- 构建为所有 4 种架构编译（sm80/sm90/sm100/sm120）= 4 倍浪费
- 还发现 **未安装 ninja** — PyTorch 回退到 `make`，逐个编译 .cu 文件

### 4. 第二次构建尝试（正确的方法）

- 终止了第一次构建
- 安装 ninja：`pip install ninja`
- 设置 `FLASH_ATTN_CUDA_ARCHS="8.9"`（flash-attn 自己的环境变量 — 被尊重）
- 设置 `MAX_JOBS=32`
- 结果：仅编译了单个架构 `compute_89,code=sm_89`，但 flash-attn 的构建仍然按顺序编译 .cu 文件（一次一个 nvcc 进程）
- 构建完成耗时约 45 分钟

### 5. 验证安装

- `flash_attn 2.8.3` 已安装在 nanochat venv 中
- `HAS_FA2 = True`，`USE_FA2 = True` — 被 nanochat 自动检测到

### 6. 烟雾测试

- 运行 `scripts.base_train`，迭代次数设为 5
- 无需修改脚本 — nanochat 在导入时自动检测 flash-attn
- 首次运行较慢，因为 `torch.compile` / inductor kernel 编译
- GPU 利用率 98%，显存占用 2.5GB
- 输出被缓冲（通过 tee 管道），因此日志目前只显示 3 行
- 进程仍在运行（torch.compile 仍在工作）

### 主要收获

- `TORCH_CUDA_ARCH_LIST` — 被 flash-attn 的构建系统忽略
- `FLASH_ATTN_CUDA_ARCHS` — flash-attn 正确的环境变量
- `MAX_JOBS` — 需要先安装 ninja
- flash-attn 无论 `MAX_JOBS` 如何设置，都按顺序编译 .cu 文件
- nanochat 有一个清晰的 `flash_attention.py` 抽象，带有 FA3 → FA2 → SDPA 回退机制
