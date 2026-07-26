---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Diagerr.xml 安装失败分析
translated: true
type: note
---

问题：分析Windows安装失败中的`diagerr.xml`。

答案：

我检查了截图。`diagerr.xml`确认了相同的情况，但**它并不包含根本原因**。

重要的条目如下：

```xml
CUnattendManager::Initialize(90):
Result = 0x80070490

CMOSetupOneSettingsHelper::InitializeSettings(324):
Result = 0x80072EE7

CSetupHost::InitializeOneSettings(1606):
Result = 0x80072EE7

CSetupManager::OnFinishLaunchChoiceAction(8149):
Result = 0xC19001F4
```

解释：

| 代码         | 含义                                | 重要性   |
| ------------ | ----------------------------------- | -------- |
| `0x80070490` | Element/not found                   | 次要     |
| `0x80072EE7` | Name resolution/network lookup failure | 次要     |
| `0xC19001F4` | Setup failure wrapper               | 最终结果 |

`diagerr.xml`基本上是一个**失败摘要**，而不是详细的失败日志。

真正的错误应该位于：

```
C:\$WINDOWS.~BT\Sources\Panther\setuperr.log
```

或者更重要的：

```
C:\$WINDOWS.~BT\Sources\Rollback\setupact.log
```

---

从你的截图中得到一条线索：

```xml
Exe="X:\Sources\SetupHost.exe"
```

这仍在从WinPE（`X:`）运行，并且失败发生在SetupHost初始化的非常早期。

因此我现在怀疑：

### 可能性1：无人值守/设置问题（比以前更高）

日志提到了：

```
CUnattendManager
CMOSetupOneSettingsHelper
```

检查你的USB是否包含：

```
\autounattend.xml
```

或者：

```
\sources\PID.txt
```

运行：

```cmd
dir D:\autounattend.xml
dir D:\sources\PID.txt
```

如果存在，移除它们并重试。

---

### 可能性2：Windows ISO/USB创建问题

因为SetupHost无法正确初始化设置。

检查USB：

```cmd
dir D:\sources
```

预期应包含：

```
boot.wim
install.wim
```

或者：

```
install.swm
install2.swm
```

---

### 可能性3：现有磁盘元数据

由于你之前遇到的离线/无法识别卷问题，仍有可能。

全新安装测试：

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

接下来，请捕获：

```
C:\$WINDOWS.~BT\Sources\Panther\setuperr.log
```

特别是**前30行**。

`diagerr.xml`只告诉我们“安装失败”；`setuperr.log`则告诉我们“为什么”。