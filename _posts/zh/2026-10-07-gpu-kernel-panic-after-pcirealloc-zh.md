---
audio: false
generated: true
image: false
lang: zh
layout: post
title: pci=realloc 后 GPU 内核崩溃
translated: true
type: note
---

机器**无法恢复**了——在约 7 分钟后 100% 丢包且 “Host is down”。`pci=realloc` 的更改（或重启本身）导致它无法启动或处于关机状态，所以现在需要物理访问才能恢复。

## 发生了什么（摘要）

| 步骤 | 结果 |
| --- | --- |
| 将 `lzw` 添加到 sudo | ✅ |
| 安装了 `nvidia-driver` 550.163.01（DKMS 为 6.12 kernel 构建） | ✅ |
| 加载模块 | ✅（`nvidia`、`nvidia_uvm`） |
| `nvidia-smi` | ❌ “No devices were found” |
| 根本原因 | GPU 的大 BAR（BAR1–5）未分配 → `NVRM: This PCI I/O region ... is invalid` |
| 修复尝试 | 将 `pci=realloc` 添加到 GRUB + 重启 |
| 结果 | ❌ 主机现在无法访问 |

## 你需要在机器旁做什么

**1. 检查是否已通电** —— 查看风扇/LED/屏幕。如果处于关机状态，按下电源按钮。

**2. 从启动挂起中恢复**（极有可能）：

- 中断 GRUB：在 5 秒 GRUB 界面期间，或在启动时按下/反复按 **Shift**（或 **Esc**）以进入菜单。
- 高亮 Debian 条目 → 按 **`e`** 编辑。
- 找到以 `linux` 开头的行，并**删除 `pci=realloc`**。
- 按 **Ctrl+X**（或 F10）启动。

**3. 一旦它恢复正常**，告诉我，我会远程撤销 GRUB 更改，这样正常重启就能再次工作。

## 正确的修复方法（BIOS —— 反正需要你到机器旁）

`pci=realloc` 是“软件变通方案”。对于 24GB Tesla M40 的大 BAR，真正的修复在 BIOS 中：

- 在 **MSI Z170A GAMING M3** 上进入 BIOS（启动时按 DEL 键）
- **Settings → Advanced → PCI Subsystem Settings → “Above 4G Decoding” → Enabled**
- 保存并退出。

启用“Above 4G Decoding”后，主板将正确分配 M40 的 BAR，`nvidia-smi` 应该能检测到它。

---

**你现在能访问这台机器吗？** 如果可以，请尝试第 1–2 步，并告诉我屏幕上显示什么——我会从那里指导你。如果屏幕显示 GRUB 菜单或错误，请告诉我确切的文本。
