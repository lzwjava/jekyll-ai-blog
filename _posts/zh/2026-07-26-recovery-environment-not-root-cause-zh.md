---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 恢复环境非根本原因
translated: true
type: note
---

问题：分析这个 `setupact.log` 截图——“用户已请求启动恢复环境”是根本原因吗？

答案：

这张截图提供了更清晰的画面。关键序列如下：

```
CInstallUI::SwitchToProgressPage
CSetupResponseTemplate<class IDlpResponse>::ExecuteRoutine: 已点击下一步按钮。

...

用户已请求启动恢复环境

错误
CSetupManager::OnFinishLaunchChoiceAction(8149): 结果 = 0xC19001F4
```

关键点：

**“用户已请求启动恢复环境”并不是根本原因，而是 Windows 安装程序在安装失败后执行的操作。**

流程如下：

```
安装失败
    |
    v
安装程序显示失败/恢复选项
    |
    v
选择了恢复环境
    |
    v
记录 0xC19001F4
```

因此，我之前关于键盘/恢复触发的怀疑可能性较低。此日志实际显示的是：

```
已点击下一步按钮
```

这意味着安装程序 UI 正常向前推进。

实际失败发生在 **此部分之前**。

---

## 需要更早的错误信息

在 WinPE 命令提示符中运行以下命令：

```cmd
cd C:\$WINDOWS.~BT\Sources\Panther

findstr /i "error failed failure rollback 0xc190" setupact.log > errors.txt

notepad errors.txt
```

请发送 `errors.txt` 的内容。

---

## 同时检查这两个文件

### 1. 安装错误日志

```cmd
notepad C:\$WINDOWS.~BT\Sources\Panther\setuperr.log
```

查找 **第一个错误**，而不是最后一个。

---

### 2. 安装阶段

查找：

```cmd
findstr /i "InstallImage ApplyImage ApplyOS" setupact.log
```

这可以告诉我们失败发生在以下哪个阶段：

* 应用 Windows 映像
* 注入驱动程序
* 引导配置
* OOBE 阶段

---

## 根据你之前的历史，我目前的概率估算

已知：

* 联想小新
* Windows 11 25H2 ISO
* 在 Mac 上准备的 USB
* 之前出现“磁盘脱机/无法识别类型”问题

我的排序如下：

### 1. SSD 分区元数据问题 — 40%

解决方法：

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

然后重新安装。

---

### 2. USB 介质 / WIM 问题 — 35%

检查：

```cmd
dir D:\sources
```

需要存在以下文件之一：

```
install.wim
```

或：

```
install.swm
install2.swm
...
```

---

### 3. 驱动程序/存储控制器问题 — 20%

联想机型常使用 Intel VMD/RST。

BIOS 检查项：

```
Storage Controller Mode
```

如果启用：

* 要么在安装过程中加载 Intel RST 驱动程序
* 要么禁用 VMD 并使用 AHCI

---

### 4. 实际恢复环境触发 — <5%

这张截图基本排除了这个可能性。

下一个有用的截图是 **setupact.log 中第一个“Error”条目附近的前 50 行**，而不是结尾部分。那里面会包含真正的原因。
