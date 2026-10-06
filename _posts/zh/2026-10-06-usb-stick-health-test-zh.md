---
audio: false
generated: true
image: false
lang: zh
layout: post
title: U盘健康测试
translated: true
type: note
---

该U盘被重新识别为 `/dev/disk12`（15.7 GB，USB，可移动）——它再次与总线通信，内核甚至重新读取了旧的GPT（分区4的Linux区域显示为空闲空间，因为dd在崩溃前已开始覆写该区域）。

现在进行健康测试——这会擦除U盘上的所有数据（反正你马上就要用ISO镜像覆写它）：

```bash
diskutil eraseDisk FAT32 TEST /dev/disk12
```

运行这条命令，然后告诉我它是完成还是卡住。如果完成，我们就重新刷写（换个端口，使用`bs=1m`）。如果卡住……这块U盘已经报废了。

如果你愿意，我也可以替你运行——说句话就行。