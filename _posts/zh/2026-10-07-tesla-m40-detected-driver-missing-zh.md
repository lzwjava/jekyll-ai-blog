---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 检测到Tesla M40，缺少驱动程序
translated: true
type: note
---

## 结果：NVIDIA Tesla M40 GPU — **硬件存在**，但未安装驱动程序

### ✅ 硬件已识别（通过 `lspci` 检测到）

```
01:00.0 3D controller: NVIDIA Corporation GM200GL [Tesla M40] (rev a1)
```

Tesla M40（GM200/Maxwell 架构，12GB GDDR5，纯计算卡）物理安装在 PCIe x16 插槽中（`01:00.0`，位于 CPU 直连的 PCIe 桥 `00:01.0` 之后）。

### ❌ 但软件栈完全缺失

| 检查项 | 结果 |
| --- | --- |
| `nvidia-smi` | 未安装 |
| NVIDIA 内核模块（`nvidia`、`nvidia_modeset`） | 未加载 |
| NVIDIA 软件包（`dpkg -l \| grep nvidia`） | 无 |
| `/dev/nvidia*` 设备节点 | 无 |

因此，该显卡 **被系统检测到但无法使用** — 没有驱动意味着无法使用 CUDA，也无法进行计算。

> 📌 补充说明：在我之前的硬件扫描中，M40 并未出现（grep 只捕获了集成显卡），但上述完整的 `lspci` 输出是权威的 — 显卡确实存在。

### 在使其正常工作之前，有两件事值得了解

1. **`lzw` 不在 sudoers 列表中** — 安装 NVIDIA 驱动需要 root 权限。要么执行 `adduser lzw sudo` 并重启（需要物理/管理员访问权限或 root 密码），要么我可以准备好命令，由你以 root 身份运行。
2. **驱动选择**：M40 是 Maxwell 架构，因此在 Debian 13（trixie，内核 6.12）上需要安装 `nvidia-driver` 软件包或旧的 `nvidia-legacy-470xx-driver` — 另外，该显卡需要 8 针电源连接器（250W TDP），并且由于它是被动散热的，可能需要主动散热（需要气流冷却）。

需要我：

- **（a）** 准备完整的驱动安装命令序列（现在以 root 运行，或者在你将 lzw 加入 sudo 后运行），或者
- **（b）** 在你启用 sudo 后重启/检查显卡的驱动状态？
