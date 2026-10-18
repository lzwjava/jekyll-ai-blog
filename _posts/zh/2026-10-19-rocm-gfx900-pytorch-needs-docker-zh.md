---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ROCm gfx900 PyTorch 需要 Docker
translated: true
type: note
---

## 完成 — ROCm userspace 已安装并验证

以下是最终状态：

### 已安装且正常运行

| 组件 | 包 | 验证 |
|-----------|---------|----------|
| GPU enumeration | `rocminfo` | ✅ `gfx900`, `AMD Radeon Pro WX 9100`, 64 CUs, 16 GB |
| Monitoring | `rocm-smi` | ✅ Device `0x6861`, GFX `gfx900` |
| Kernel thunk | `libhsakmt1` | ✅ |
| HSA runtime | `libhsa-runtime64-1` | ✅ (ROCk module loaded) |
| HIP runtime + compiler | `libamdhip64-7`, `hipcc` (clang-21) | ✅ compiled & **ran a real vec-add kernel on GPU** |
| OpenCL | `rocm-opencl-icd` | ✅ `clinfo`: gfx900, OpenCL 2.0, 64 CUs |

我还将您的用户添加到了 `render` 和 `video` 组（ACLs 已允许访问；重新登录以使组成员身份生效）。

### 已确认的限制（已验证，非假设）

ROCm **7.1 的 rocBLAS 没有 gfx900 内核**，因此任何基于 rocBLAS 的工作负载都会失败：

```
Device ID 0 : AMD Radeon Pro WX 9100 gfx900:xnack-
rocBLAS error: Cannot read .../TensileLibrary.dat ... for GPU arch : gfx900
```

这意味着 **来自 Ubuntu 仓库的 PyTorch（`python3-torch-rocm`）将无法在此 GPU 上运行。** 自定义 HIP 内核和 OpenCL 可以工作。

### 为了在此卡上实际训练 nanoGPT

gfx900 需要 **ROCm 5.7** 栈（最后一个完全支持 Vega 10 的版本）。最干净的方式是使用容器，因为主机内核驱动 + `/dev/kfd` 就是所需的全部：

```bash
docker run -it --device=/dev/kfd --device=/dev/dri \
  --group-add video --group-add render \
  rocm/pytorch:rocm5.7_ubuntu22.04_py3.10_pytorch_2.0.1
```

您的系统 **既没有 docker 也没有 podman**，并且系统 Python 是 **3.14**（对于 ROCm 5.7 PyTorch 轮子来说太新了），因此容器路线是实际可行的。

---

下一步 — 我应该：

1. **安装 docker（或 podman）并拉取 `rocm/pytorch` ROCm 5.7 镜像**，然后验证 `torch.cuda` 是否能看到 GPU 并运行一个快速的 nanoGPT smoke test？*（推荐）*
2. 保持原样 — 您将自行处理 PyTorch 设置？
3. 同时**移除**我仅为验证测试安装的 `librocblas5`/`librocblas5-bench` 包？（它们无害但未使用。）

您想要哪一个？