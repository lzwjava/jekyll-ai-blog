---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows 11 在联想小新上安装失败
translated: true
type: note
---

**问题：** 到目前为止整个故障排查过程的总结。

**答案：**

**设置：** 联想小新，之前是 Linux Mint，全新安装 Windows 11。磁盘 0 = 476GB UMIS NVMe（主 SSD），磁盘 1 = 约 14GB 小驱动器（忽略，不相关）。

**我们已经解决的问题：**

1. 原始错误 ——“分区类型无法识别/卷脱机” —— 由磁盘 0 上残留的 Linux Mint 分区签名（LVM/RAID）引起。
2. 通过 `diskpart` 修复：在磁盘 0 上执行 `clean` → `convert gpt`（每次通过 `detail disk` 确认正确的磁盘）。
3. 确认 BIOS 为纯 UEFI 模式（此型号无需切换 Legacy/CSM）。
4. 在安装程序中正确选择了磁盘 0 的未分配空间，点击“下一步”——分区选择本身不再是问题。

**当前障碍：**
安装现在在“正在安装 Windows”进度阶段失败，并显示一个通用的“Windows 11 安装失败”对话框。日志分析（`setupact.log` / `setuperr.log`）显示：

- 早期错误（`0x80070490`、`0x80072EE7`、`0x80070002`）= 无害，仅表示 WinPE 中无网络连接——忽略这些。
- 实际致命链：`CSetupManager::OnFinishLaunchChoiceAction(8149): Result = 0xC19001F4` —— 安装程序收到“启动恢复环境”请求并自行中止。
- 这**在同一位置连续发生了两次**，排除了意外按键作为唯一原因。

**尚未尝试（后续步骤）：**

1. 从 Microsoft 重新下载全新的 Windows 11 ISO。
2. 使用 Rufus（GPT + UEFI 目标）重新写入**不同的** U 盘 —— 当前 U 盘介质现在是头号嫌疑对象。
3. 从进度条到 OOBE 完全无操作（不触碰键盘/触摸板）运行安装。
4. 如果使用全新 ISO + 全新 U 盘 + 不触碰的情况下第三次以相同方式失败 → 很可能是硬件问题（内存或 NVMe 控制器），而非介质/软件问题 —— 届时需要运行内存测试（Windows 内存诊断或 MemTest86）和 NVMe 健康检查（`nvme-cli` 或制造商工具）。

**不需要：** 扩展/手动创建分区 —— 安装程序对未分配空间的自动分区是正确的，并非问题所在。
