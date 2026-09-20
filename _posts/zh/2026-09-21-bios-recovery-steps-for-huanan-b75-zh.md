---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华南B75的BIOS恢复步骤
translated: true
type: note
---

问：你的华南B75现在能通电启动，风扇转动，但刷BIOS后没有视频输出；键盘短暂亮灯。

答：

这种症状强烈表明CPU/电源不是直接问题。**首先将其视为BIOS初始化失败。** 不要反复刷写修改过的镜像。

### 1. 先做最简单的POST测试

完全断电并拔掉电源插头。

断开/移除：

* SSD
* 独立显卡
* 除键盘外的所有USB设备
* 任何额外的PCIe卡

只保留：

* B75主板
* CPU + 散热器
* **一根DDR3内存条**
* 电源
* 连接到主板视频输出的显示器

你的CPU型号在此很重要：主板VGA/DVI输出仅当CPU具有可用的Intel集成显卡时才工作。

然后清除CMOS：

1. 关闭电源开关。
2. 拔掉交流电源。
3. 取出CMOS电池。
4. 按住机箱电源按钮约10秒。
5. 等待几分钟。
6. 重新安装电池。
7. 启动电源。

逐一尝试每根内存条，必要时尝试不同的DIMM插槽。

### 2. 然后尝试AMI恢复

既然你有未修改的 `B75V101_original.bin`，这是**在购买编程器之前**我会尝试的方法。

AMI的文档化恢复机制使用启动块加载BIOS镜像，通常命名为 `AMIBOOT.ROM`，而 `Ctrl+Home` 是标准的恢复热键。某些AMI实现支持USB恢复，但此特定华南主板是否暴露该功能取决于其固件实现。（[Futura Sciences论坛][1]）

尽可能简化USB：

```text
USB
└── AMIBOOT.ROM
```

其中：

```text
AMIBOOT.ROM = B75V101_original.bin
```

首次尝试时，我**不会**在其上放置多个BIOS文件。如果可能，请使用小的FAT32格式U盘。

然后：

```text
1. 电脑关机
2. 插入U盘
3. 按住 Ctrl + Home
4. 按下电源按钮
5. 保持按住 Ctrl + Home 约10–15秒
6. 松开
7. 等待
```

**一旦恢复开始，不要重置或断电。**

AMI文档指出，恢复过程可以在没有显示器的情况下运行，并通过蜂鸣声/访问活动指示ROM正在加载/写入。（[Futura Sciences论坛][1]）

### 3. 重要的诊断：插入U盘后它有何表现？

仔细听。

| 行为                              | 含义                                            |
| --------------------------------- | ----------------------------------------------- |
| USB指示灯闪烁/有访问活动         | 很有希望——启动块可能还活着                      |
| 几声蜂鸣                          | 恢复例程可能已启动                              |
| 大约4次恢复蜂鸣                   | 强烈表明在此使用该代码的实现中ROM写入已完成    |
| 完全没有USB活动，无蜂鸣声         | 恢复路径可能未启用，或启动块本身可能已损坏      |
| 风扇永远转，键盘短暂闪，之后完全无反应 | 符合BIOS无法达到正常POST的状态                  |

**不要以为“无显示=主板坏了”**。即使正常BIOS无法POST，一个功能正常的恢复启动块也可能存在。

### 4. 在采取任何其他操作前，我希望你检查一件事

你说：

> 键盘会短暂亮一下

这很有用。

请准确告诉我按下电源按钮后发生的情况：

```text
风扇：         保持转动 / 转动后停止
键盘：         闪一次 / 保持亮 / 完全熄灭
U盘：          LED闪烁？是/否
蜂鸣：         0 / 1 / 2 / 4 / 持续
显示器：      立即“无信号” / 亮起后无信号
显卡：         已安装 / 已移除
CPU型号：     确切型号
```

另外，**暂时不要再刷写放大/自定义的镜像**。首先尝试恢复已知完好的原始 `B75V101_original.bin`。

如果 `Ctrl+Home` 导致**零USB活动和零蜂鸣**，那么我会考虑直接用CH341A/SOIC8夹子读取SPI芯片。这为我们提供了比反复猜测键盘恢复组合更确定的恢复路径。

### 参考文献：

* [AMI AMIBIOS8 Flash Update & BIOS Recovery Methods](https://forums.futura-sciences.com/attachments/materiel-hardware/58894d1225034379-flash-bios-rate-amibios8_flash_recovery_whitepaper_v10.pdf)（[Futura Sciences论坛][1]）
* [BIOSTAR: How to recover AMI BIOS if update fails](https://www.biostar-usa.com/app/en-us/support/faq.php?page=12&searchfaq=bios)（[Biostar USA][2]）

如果Ctrl+Home恢复没有响应，我也可以指导你完成**CH341A读取→验证→备份→写入→验证**的步骤。

[1]: https://forums.futura-sciences.com/attachments/materiel-hardware/58894d1225034379-flash-bios-rate-amibios8_flash_recovery_whitepaper_v10.pdf?utm_source=chatgpt.com "AMIBIOS白皮书"
[2]: https://www.biostar-usa.com/app/en-us/support/faq.php?page=12&searchfaq=bios&utm_source=chatgpt.com "BIOSTAR技术支持与常见问题 | 主板与IPC的专业解决方案"