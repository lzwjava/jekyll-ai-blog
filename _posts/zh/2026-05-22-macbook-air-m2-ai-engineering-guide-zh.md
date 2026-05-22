---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MacBook Air M2 AI 工程指南
translated: true
type: note
---

以下是您的 MacBook Air M2（16 GB 统一内存）当前的状况：

**内存：极为紧张**
- 报告显示 48% 空闲——但其中有 6 GB 已被压缩（操作系统正在努力维持运行）
- 使用了 145 MB 交换内存（您已经溢出到磁盘）
- 可用磁盘 54 GB——目前还有足够的缓冲
- 微信 265 MB，WebKit 标签页约 250 MB 每个，GitHub Desktop 236 MB，Python 188 MB，Zed 144 MB

这是搭载 **统一内存** 的 M2——没有独立的 VRAM。GPU 与系统其他部分共享同样的 16 GB。当您在此运行机器学习工作负载时，您正在与微信和 Chrome 竞争资源。

---

## 针对此设备的 AI 工程优化

**1. 量化——日常推理使用 GGUF 4-bit**

以支持 Metal 后端的 llama.cpp 为基础：

```bash
# 安装带 Metal 支持的 llama.cpp
brew install llama.cpp
llama-cli -m model.Q4_K_M.gguf -n 256 --mlock
```

对于 Q4_K_M 的 7B 模型：约 4.5 GB 内存。为系统留下约 11 GB。
Q8_0：质量更好，约 7 GB——如果关闭其他应用仍可运行。

**2. MLX——M2 的真正平台**

MLX 是 Apple 的原生框架。它智能地利用统一内存，并且可以使用独立的神经引擎（ANE）带宽：

```bash
pip install mlx mlx-lm
```

对于 16 GB 设备上的推理和微调，MLX 是目前最好的选择：

```python
from mlx_lm import load, generate
model, tokenizer = load("mlx-community/Llama-3.2-3B-4bit")
```

**3. 停止使用交换内存——关闭高占用应用**

| 进程 | 内存 | 解决方法 |
|---|---|---|
| 微信 | 265 MB | 如不需要则关闭 |
| WebKit 标签页 | 250 MB × N | 关闭多余标签页 |
| GitHub Desktop | 236 MB | 使用 CLI git 可节省 200+ MB |
| Zend (Zed) | 144 MB | 已经很轻量 |

将 GitHub Desktop 替换为 `gh` CLI。Safari 的繁重标签页→关闭或挂起。

**4. ML 训练——不建议进行**

16 GB 的 M2 没有独立 GPU VRAM，不是训练机器。它适合用于：
- 推理（MLX 4-bit，3B - 8B 模型）
- 生成嵌入（MLX）
- 智能体编排（调用 OpenRouter、您的 RTX 4070、AMD 云的 API）
- 评估与数据工程脚本

实际的训练保留给：
- 192.168.1.36（RTX 4070 12 GB）——LoRA/QLoRA，nanoGPT
- AMD MI300X 云（192 GB HBM3）——全量微调，大规模 GRPO 运行

**5. 内存监控工具包**

```bash
# 快速检查
memory_pressure | grep "free percentage"
vm_stat | head -1
sysctl vm.swapusage

# 监控 GPU 压力
sudo powermetrics --samplers gpu_power -n 1 -i 2000
```

**6. 针对您的工作流（AI 工程师、API 优先、智能体构建者）**

您实际的工作流根本不需要本地 GPU——您将请求路由到 OpenRouter、RTX 4070 和 AMD 云。在这台 MacBook 上：
- 终端 + 编辑器 + 浏览器本身就是工作流
- MLX 用于快速本地推理/嵌入
- 关闭微信和多余的 Safari/Chrome 标签页→立即回收 1 GB 以上
- 这可以释放 6 GB 的压缩开销——系统将停止交换

需要我帮您配置以上任何一项——关闭内存大户、终止交换、或在这台机器上搭建您理想的 AI 开发环境吗？