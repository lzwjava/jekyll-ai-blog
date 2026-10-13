---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 切换到Nouveau并测试
translated: true
type: note
---

已推送为 **`muda 0.8.0`**（`71e1f55`）。原生后端已就位——现在需要你动手，因为我没有非交互式 root 权限。

## 我需要你运行的一件事

首先停止任何使用 M40 的程序（ComfyUI、`llama-server` 等），然后：

```sh
cd ~/projects/muda

# 查看当前状态（无需 root）
tools/muda-gpu-mode.sh status

# 切换到 nouveau（需要 root）
sudo tools/muda-gpu-mode.sh nouveau
```

然后测试原生路径：

```sh
MUDA_DRIVER=nouveau ./build/mudainfo
MUDA_DRIVER=nouveau ./build/test_memory
```

**把输出贴回给我。** 如需随时撤销：

```sh
sudo tools/muda-gpu-mode.sh nvidia     # 或直接重启
```

重启后总是恢复 `nvidia`，因为 `nouveau` 仍被 NVIDIA 软件包列入黑名单——该切换仅对本次运行生效。

## 我已经构建好的内容（已通过编译测试）

- **`src/driver_nouveau.c`** — 直接通过 `/dev/dri/renderD*` 与 nouveau 内核驱动通信，使用手写的 DRM ioctl ABI（不需要 libdrm 头文件）：
  - `DRM_IOCTL_VERSION` + `DRM_IOCTL_NOUVEAU_GETPARAM` → 芯片组、PCI ID、帧缓冲大小
  - `DRM_IOCTL_NOUVEAU_GEM_NEW` + `mmap` → 用于 `mudaMalloc` 的真实 GEM 分配
  - 完整的 stream/event 接口；`launch` 目前返回 `mudaErrorNotSupported`
- **`tools/muda-gpu-mode.sh`** — `status` / `nouveau` / `nvidia`，可逆
- `MUDA_DRIVER=nouveau` 已接入 `mudaInit`

当前已验证状态没有变化：**77 项检查 + 4 个 mudac 程序**，在 OpenCL 驱动上全部通过；在 nvidia 驱动绑定时，`MUDA_DRIVER=nouveau` 会干净地报告“no nouveau DRM device found”。

## 你把输出贴回来之后

一旦 nouveau 被绑定，并且我能以普通用户身份打开它的 render node，我就能**真正在真实硬件上开发和测试**原生驱动（GEM 分配、`GETPARAM`，然后是计算通道）。如果你的内核上 `GETPARAM`/GEM 需要不同的常量，我会在你的输出中看到并修复。

如果你现在不想切换，告诉我，我就会转向支持 `__constant__`/`cudaMemcpyToSymbol`，或者实现更快的 SGEMM。