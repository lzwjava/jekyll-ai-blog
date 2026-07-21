---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD Radeon 云实例恢复
translated: true
type: note
---

## 完整摘要 — AMD Radeon 云实例

### 1. 初始问题：SSH 连接失败

您尝试连接到 `36.150.116.206:31094` — 返回 **连接被拒绝**。

**诊断结果：**

- ✅ 主机 **可达**（通过 DMIT 跳板机 ping 延迟 39ms）
- ❌ 端口 31094 **未开放**
- ✅ 附近**其他端口**开放：**31090, 31091, 31092, 31095, 31098, 31099, 31100**
- 在 **31090, 31098, 31100** 上发现 SSH 但 **密钥未授权**
- 您的 `~/.ssh/config` 包含全局 SOCKS5 代理，因此 SSH 通过代理路由 — 我们使用 `ProxyCommand=none` 绕过了代理

### 2. 发现 API 端点

您测试了 API：

```bash
curl https://radeon-global.anruicloud.com/spaces/u-9758-811746f0/8000/v1/chat/completions
```

✅ **Qwen3-8B** 通过 **AMD Radeon 云代理** 成功响应。

### 3. SSH 端口 31154 工作正常

您通过 `ssh -p 31154` 连接 — 使用您的密钥成功登录。

**服务器规格：**

| 组件 | 数值 |
| ----------- | ------- |
| **操作系统** | Ubuntu 24.04 LTS |
| **CPU** | 2× AMD EPYC 9334（128 线程） |
| **内存** | 503 GiB |
| **GPU** | AMD Radeon Graphics（gfx1100，RDNA 3）— **48 GB 显存** |
| **ROCm** | 7.2.1，驱动 6.16.13 |
| **PyTorch** | 2.9.1（ROCm 构建，位于 `/opt/venv`） |
| **磁盘** | `/` = 3.5TB 覆盖层，`/workspace` = 98GB 循环设备 |

GPU 计算测试：✅ **通过**（HIP 向量加法，48GB 可访问，96 个 CU）

### 4. 尝试 FLUX.2-dev — 太大（崩溃）

- 模型：**32B 参数**，总计 **166GB**
- 通过 `hf-mirror.com` 使用 `hf_transfer` 下载 — **252 秒**（约 660MB/s）
- 尝试使用 CPU 卸载进行推理：**OOM 崩溃** ❌
  - **仅 Transformer 就需要 60GB**（BF16 精度）
  - 仅有 48GB 显存可用
  - 容器被 OOM 杀死时 **SSH 守护进程停止运行**

### 5. 实例重启 — SSH 损坏

OOM 崩溃后，容器重启但 SSH **未在内部运行**（它是云代理的，而非真实 SSH）。您通过 **Jupyter Lab 终端** 获得了访问权限：

- `https://radeon-global.anruicloud.com/spaces/u-9758-811746f0/`（端口 8888，令牌：`amd-oneclick`）

### 6. 当前状态（在 Jupyter 终端中）

| 项目 | 状态 |
| ------ | -------- |
| Jupyter 终端 | ✅ **您已进入** |
| SSH 服务器 | ❌ 未安装（我们尝试了 `apt install openssh-server` + `mkdir -p /run/sshd`，但云代理端口映射已过期） |
| FLUX.2-dev | 仍存储在磁盘上 `/FLUX.2-dev`（166GB） |
| `/workspace` 磁盘 | 98GB（19GB 可用）— 太小 |
| `/` 磁盘 | 3.5TB（2.8TB 可用）✅ |

### 7. 下一步：FLUX.1-dev

由于您已进入 Jupyter 终端，我仍可以帮助您运行 FLUX.1-dev — 它有 **12B 参数**（总计约 35GB，FP16 下需要约 24GB 显存），将**轻松适配**您 48GB 的 GPU。

**在 Jupyter 终端中粘贴：**

```bash
rm -rf /FLUX.2-dev && export PATH=/opt/venv/bin:$PATH && export HF_ENDPOINT=https://hf-mirror.com && export HF_HUB_ENABLE_HF_TRANSFER=1 && python3 -c "
from huggingface_hub import snapshot_download
print('正在下载 FLUX.1-dev...')
snapshot_download('black-forest-labs/FLUX.1-dev', local_dir='/FLUX.1-dev')
print('下载完成！')
"
```

下载完成后，运行：

```bash
export PATH=/opt/venv/bin:$PATH && cd /workspace && python3 -c "
import torch
from diffusers import FluxPipeline
pipe = FluxPipeline.from_pretrained('/FLUX.1-dev', torch_dtype=torch.bfloat16)
pipe.enable_sequential_cpu_offload()
image = pipe('火星上的一只可爱猫', num_inference_steps=28).images[0]
image.save('flux_output.png')
print('已保存！')
"
```
