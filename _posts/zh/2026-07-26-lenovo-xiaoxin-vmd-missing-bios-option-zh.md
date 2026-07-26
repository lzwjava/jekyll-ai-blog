---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想小新VMD缺少BIOS选项
translated: true
type: note
---

Question: 联想小新BIOS中没有Intel VMD/RST选项。接下来该怎么办？

Answer:

这很常见。许多**联想小新**型号在消费级BIOS中完全隐藏了VMD/RST开关。缺少该选项**并不**排除VMD的存在，但我们需要验证而非猜测。

其他代理的理论仍有可能，但让我们收集证据。

---

## 1. 检查Windows PE是否通过VMD识别SSD

你当前位于Windows安装界面。按下：

```
Shift + F10
```

运行：

```cmd
diskpart

list disk
```

告诉我输出结果。

示例：

### 情况 A — 标准NVMe

```
Disk 0    512 GB
```

### 情况 B — VMD/RST

有时你能看到磁盘，但Windows安装程序需要Intel RST驱动。

---

## 2. 检查存储控制器名称

在同一命令提示符下：

```cmd
wmic path Win32_PnPEntity get Name
```

查找：

```
Intel(R) Volume Management Device
Intel RST
VMD
```

或：

```
Standard NVM Express Controller
```

如果看到：

```
Intel(R) Volume Management Device
```

则VMD处于激活状态。

---

## 3. 联想隐藏BIOS菜单

部分联想BIOS版本隐藏了该选项。尝试：

进入BIOS：

```
F2
```

然后：

```
Configuration
```

查找：

```
Storage
SATA Controller Mode
```

或：

```
Intel Rapid Storage Technology
```

如果不存在，不必浪费时间寻找。

---

## 4. 另一个可能原因：Windows已安装，但引导条目失败

你的日志显示：

```
Setup Phase: [4]
Overall progress: [11%]
```

这很有意思。

失败发生在“安装模式”转换的早期阶段。

失败后检查：

按下：

```
Shift + F10
```

运行：

```cmd
diskpart

list vol
```

查找：

```
EFI
FAT32
100-300MB
```

如果缺少，则磁盘分区错误。

---

## 5. 我更新的概率

已知：

* USB正确 ✅
* 联想BIOS隐藏VMD选项 ✅

我会修改为：

| 原因 | 概率 |
| ----------------------- | ---: |
| EFI/GPT分区问题 | 40% |
| Intel VMD/RST | 35% |
| 驱动问题 | 15% |
| USB | <5% |

之前的“VMD 60%”在没有BIOS证据的情况下过于激进。

---

## 最快的测试

既然你正在进行全新安装，我会建议：

1. 启动安装程序
2. 在磁盘选择界面按下：

```
Shift + F10
```

3. 运行：

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

4. 重新安装。

这将删除所有联想恢复分区和旧元数据。

在执行之前，请发送以下命令的输出：

```cmd
diskpart
list disk
list vol
```

这将告诉我们这是VMD问题还是分区元数据问题。
