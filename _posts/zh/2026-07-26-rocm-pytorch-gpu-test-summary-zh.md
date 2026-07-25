---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ROCm PyTorch GPU 测试总结
translated: true
type: note
---

现在我已掌握全部情况。以下是摘要：

---

## ✅ PyTorch + ROCm — 测试结果

| 测试项 | 结果 |
|------|--------|
| `torch.cuda.is_available()` | ✅ **True** |
| `torch.cuda.device_count()` | ✅ **1**（已分配至本 Pod） |
| GPU 张量运算（矩阵乘法） | ✅ **正常**（结果 6.25） |
| `torch.version.hip` | ✅ **7.2.53211** |
| GPU 架构支持 | `gfx1100`、`gfx90a`、`gfx942`、`gfx950`…… |
| 4096×4096 矩阵乘法基准测试 | 每次运算 **24.8ms**（约 5.5 TFLOPS） |
| vLLM | ✅ **0.16.1.dev0**（基于 ROCm 7.2.1 构建） |

### 🖥️ GPU 硬件

```
GPU：AMD Radeon Graphics（gfx1100 / RDNA3）
显存：48 GiB（51,522,830,336 字节）
PCI：0000:23:00.0
节点 ID：3
温度：27°C（空闲）
功耗：14W（空闲），上限 241W
```

### 🔍 为何仅显示 1 块 GPU？

该服务器在 PCI 总线上一共挂载了 **8 块物理 GPU**，但**只有 1 块分配给了本 Pod**——其余均分配给了其他租户：

```
PCI 总线上的 GPU： 03:00.0  23:00.0*  43:00.0  63:00.0  83:00.0  a3:00.0  c3:00.0  e3:00.0
DRM 渲染节点：     D128     D129*     D130     D131     D132     D133     D134     D135
/dev/dri 访问权限： ❌      ✅        ❌       ❌       ❌       ❌       ❌       ❌
                              ↑ 此为当前 Pod 所用节点
```

该平台采用 **GPU 分区**机制——每个 Pod 通过 `/dev/kfd` 和专属渲染节点独占 1 块 GPU。您可独享全部 48GiB 显存。

### 🚀 快速使用

```bash
source /opt/venv/bin/activate
python -c "import torch; print(torch.cuda.device_count(), torch.cuda.get_device_name(0))"
# → 1, AMD Radeon Graphics
```