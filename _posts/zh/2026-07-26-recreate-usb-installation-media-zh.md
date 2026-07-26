---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重新创建USB安装介质
translated: true
type: note
---

问题：**回顾到目前为止的 Windows 11 安装故障排除过程——最可能的原因是什么，接下来应该做什么？**

回答：

你的诊断基本正确。故障排除路径已经排除了常见原因。我按可能性排序剩下的问题如下：

## 可能性排序

### 1. USB 安装介质问题 — 约 60%

这是可能性最高的原因。

关键线索：

> 分区成功后，在“安装 Windows”阶段失败。

这意味着：

* BIOS → USB 启动成功 ✅
* Windows PE 加载成功 ✅
* 磁盘被检测到 ✅
* GPT 分区成功 ✅
* 安装程序开始复制/应用映像 ❌

错误的 ISO 下载、错误的 USB 写入或质量差的 U 盘常常在这时失败。

常见原因：

* `install.wim` / `install.esd` 损坏
* Rufus 写入问题
* 廉价 U 盘控制器错误
* USB 端口不稳定

我不建议重复使用当前的 U 盘。

建议：

1. 下载官方 ISO：

   Microsoft Media Creation Tool 最安全。

2. 如果手动下载，验证 ISO 哈希值。

3. 重新制作 U 盘：

Rufus：

```
分区方案: GPT
目标系统: UEFI (非 CSM)
文件系统: NTFS
```

对于 Windows 11 ISO，Rufus 可能会显示绕过选项：

* 移除 TPM 要求
* 移除 Secure Boot 要求

在此 Lenovo 上不要选择不必要的绕过。保持标准设置。

---

### 2. NVMe SSD 问题 — 约 25%

SSD 之前用于 Linux，但 `clean` 移除了分区元数据。

然而，`clean` 不会测试物理驱动器。

可能的问题：

* NVMe 控制器固件 bug
* 坏 NAND 块
* SSD 过热
* 电源管理问题

模式：

```
分区成功
映像部署失败
```

在向故障 SSD 写入大量数据时也可能发生。

如果另一次全新安装尝试失败，则测试 SSD。

从 Linux 中：

```bash
sudo nvme list

sudo nvme smart-log /dev/nvme0
```

查看：

```
critical_warning
media_errors
num_err_log_entries
percentage_used
```

---

### 3. 内存问题 — 约 10%

内存通常导致：

* 随机蓝屏
* 解压错误
* 不同阶段的失败

因为 Windows 安装会解压数 GB 的压缩文件，坏内存可能触发：

```
0x80070002
0x8007000D
```

或随机损坏。

但你的失败点完全相同两次，这降低了内存的可能性。

然而，如果新 U 盘仍然失败：

运行：

```
memtest86+
```

至少一个完整循环。

---

### 4. Windows 恢复环境触发 — 有趣但可能是次要原因

你的日志：

```
CSetupManager::OnFinishLaunchChoiceAction
Result = 0xC19001F4
```

这很有趣。

这通常意味着安装程序认为：

“安装无法继续，提供恢复选项。”

但背后的原因更早出现。

链条可能是：

```
安装映像部署失败
        |
        v
安装程序判定安装失败
        |
        v
启动恢复环境
        |
        v
0xC19001F4
```

所以不要纠结于 WinRE。

---

## 我还想额外检查的一件事

在重新安装之前，进入 BIOS。

检查：

### 存储模式

某些 Lenovo 机器有：

```
Intel VMD Controller
```

或

```
RST 模式
```

如果启用：

Windows 安装程序有时会出现奇怪行为。

推荐：

```
存储:
AHCI
```

但是，既然你的安装程序已经能识别 NVMe 并分区，这可能不是问题。

---

## 我接下来要做的确切步骤

我会这样做：

### 第一步

制作新 U 盘。

建议：

* 使用不同的 U 盘
* 使用不同的 USB 端口
* 使用全新的 ISO

---

### 第二步

零交互安装。

点击：

```
磁盘 0 未分配空间
        |
        v
下一步
```

之后不要触碰任何东西。

不要：

* 鼠标
* 键盘
* 触摸板
* 电源按钮

等待直到 OOBE。

---

### 第三步

如果失败重复：

启动 Linux  live USB 并收集：

SSD：

```bash
sudo nvme smart-log /dev/nvme0
```

内存：

```
memtest86+
```

---

我的猜测：**你已经解决了 Linux/LVM 问题。剩下的失败很可能是 Windows 安装介质问题，而不是 Lenovo 硬件问题。** 机器能够进入 Windows 安装程序并始终到达同一阶段，这实际上是个好迹象。