---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD MI300X 服务器 GPU 详情
translated: true
type: note
---

完成。以下是总结：

---

**服务器**：`ssh root@134.199.199.108`

**GPU**：AMD Instinct MI300X (Aqua Vanjaram) — 虚拟功能直通

| 项目 | 详情 |
| ------ | -------- |
| GPU | AMD Instinct MI300X VF (0x74b5) |
| PCIe | Gen 5.0 x16 (32 GT/s) |
| 内存 | 256 GB HBM3 |
| 驱动 | in-kernel amdgpu |
| 主机 | ubuntu-gpu-mi300x1-192gb-devcloud-atl1 |

**检查GPU的命令**（等同于 nvidia-smi）：

```
amd-smi
```

我已将其安装在服务器的 `/usr/local/bin/amd-smi` 路径下。由于该GPU是一个SR-IOV虚拟功能，且KFD（计算）接口未暴露，它直接读取sysfs/lspci — 同样原因下，`rocm-smi` 显示“未指定AMD GPU”。

要获得完整的计算访问权限（HIP、ROCm库等），你需要运行：

```
apt install rocm-hip-sdk
```

但这是一个较大的安装包 — 如果你打算走这条路，请告诉我。
