---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 查找Windows安装失败原因
translated: true
type: note
---

问题：检查新的 `setupact.log` 截图，并确定 Windows 安装失败点。

回答：

我检查了两张截图。它们实际上揭示了一些重要信息：

**你捕获的日志仍然不是失败点。**

可见部分显示的是正常的安装流程：

```
CInstallUI::SwitchToProgressPage
Next button clicked
LanguageSelection...
KeyboardSelection...
ProgressHandlerAction...
Task progress: [46%]
```

以及更早的：

```
Action progress: [100%]
Overall progress: [11%]
Setup Phase: [4]
Setup SubPhase: [54]
```

这意味着：

* USB 启动正常 ✅
* Windows PE 正常工作 ✅
* 安装界面正常 ✅
* 语言选择正常 ✅
* 安装过程已启动 ✅

失败发生在稍后的阶段，超出这部分内容。

这一行：

```
User has requested to launch the recovery environment
```

仍然只是**回滚/恢复路径**，而不是根本原因。

---

## 重要线索：安装阶段 [4]

Windows 安装阶段：

```
Phase 1: Downlevel
Phase 2: SafeOS
Phase 3: First boot
Phase 4: Second boot / OOBE transition
```

你的失败出现在大约：

```
Setup Phase: [4]
```

所以这很可能是在**映像应用之后**。

这使得以下可能性较低：

* ❌ 损坏的 ISO
* ❌ 缺少 install.wim
* ❌ USB 复制问题

因为安装程序已经进行了后续步骤。

更可能的原因：

1. 启动配置问题
2. 存储控制器 / VMD 驱动
3. 驱动冲突
4. 现有 EFI 分区问题

---

## 下一步检查：找到真正的错误

在命令提示符中：

```cmd
cd C:\$WINDOWS.~BT\Sources\Panther

findstr /i "error 0xc190 0x8007 failed" setuperr.log
```

然后：

```cmd
notepad setuperr.log
```

滚动到**第一个 Error**，而不是底部。

---

## 同时检查安装回滚日志

Windows 会在此处保留真正的原因：

```cmd
notepad C:\$WINDOWS.~BT\Sources\Rollback\setupact.log
```

这个文件通常更有用。

搜索：

```
Error
Failed
0x
```

---

## 我更新的猜测

基于截图：

### 最可能：旧磁盘布局 / EFI 问题

你之前遇到过：

```
partition is of an unrecognized type
volume is offline
```

我会建议进行完全干净的 GPT 安装：

启动 USB → Shift+F10：

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

返回安装程序 → 刷新 → 安装。

这会移除：

* 旧的 Lenovo 恢复分区
* 损坏的 EFI 条目
* 动态磁盘元数据
* 过时的 RAID 签名

---

在清空之前，请发送给我：

```
C:\$WINDOWS.~BT\Sources\Rollback\setupact.log
```

或执行以下命令的输出：

```cmd
findstr /i "error failed 0xc190" C:\$WINDOWS.~BT\Sources\Rollback\setupact.log
```

这应该包含真正的根本原因。
