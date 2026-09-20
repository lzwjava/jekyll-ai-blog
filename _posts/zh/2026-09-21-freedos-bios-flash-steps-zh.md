---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FreeDOS BIOS刷新步骤
translated: true
type: note
---

你已进入 FreeDOS 提示符——这正是你想要的界面。（"CD-ROM not configured" 无害，忽略即可。）

在 `C:\>` 提示符下：

**1. 确认文件存在：**
```
dir
```
你应该能看到 `FLASH.BAT`、`FPT.EXE`、`FPARTS.TXT`、`NEWBIOS.BIN`、`OLDBIOS.BIN`。

**2. 执行刷写：**
```
flash.bat
```

**3. 观察输出：**
- 它首先导出当前 BIOS → `BACKUP.BIN`
- 然后刷入 `NEWBIOS.BIN`

**4. 等待提示：**
```
FLASH OK. Power off, then power on.
```

---

如果 `flash.bat` 显示 `FLASH FAILED` — **不要断电**，只需再次运行 `fpt -f NEWBIOS.BIN`。

如果 `dir` **没有**列出文件（例如提示符位于错误的驱动器），也请检查 `A:` 和 `B:`：
```
dir a:\
dir b:\
```
如果文件在那里，运行 `a:\flash.bat`。

请告诉我 `flash.bat` 输出的内容。