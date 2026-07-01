---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA 13.2 升级与兼容性指南
translated: true
type: note
---

以下是翻译内容：

### 📊 CUDA 13.2 可用性

| Check | Result |
| ------- | -------- |
| `cuda-toolkit-13-2` 在 repo 中？ | ✅ **Yes** — 已提供 |
| Driver 580 是否支持？ | ✅ **Yes** — Driver 580 附带 CUDA 13.0 runtime，与 13.2 toolkit 兼容 |
| 当前已安装版本 | CUDA 12.8 (toolkit) + Driver 580.126.09 |

**Repo 中可用的 toolkit 版本：**

- 12.5, 12.6, 12.8, 12.9
- **13.0, 13.1, 13.2** ← 最新

### ✅ 是的，你可以升级到 13.2

Driver 580 支持该版本。安装命令为：

```bash
apt install cuda-toolkit-13-2
```

然后将 PATH 更新为 `/usr/local/cuda-13.2/bin`。你也可以保留 12.8 与其共存 —— CUDA toolkits 支持多版本并存（`/usr/local/cuda-12.8/` 和 `/usr/local/cuda-13.2/`），可以通过 symlink 或 PATH 进行切换。

### ⚠️ 注意事项

- **PyTorch/TensorFlow 兼容性** — 大多数 framework 目前以 CUDA 12.x 为目标。CUDA 13.x 的支持仍在逐步推出中。如果你计划运行 ML workloads，目前 12.8 是更稳妥的选择。
- **并存安装没有问题** — 无需删除 12.8，只需添加 13.2 并切换 PATH 即可。
- **Driver 无需变动** — 无需为了 CUDA 13.2 升级 Driver。

需要我安装 13.2（保留 12.8 共存），还是彻底替换 12.8？
