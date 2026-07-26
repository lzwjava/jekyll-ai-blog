---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows 11 75% 失败原因
translated: true
type: note
---

问题：**如果Windows 11安装到75%然后失败，Pro版和Home版的不同可能是原因吗？**

答案：**不是。如果安装到75%，Windows版本选择绝对不是原因。**

在约75%时，Windows安装程序已经通过了以下阶段：

```
USB启动
→ WinPE加载
→ SSD检测
→ 分区创建
→ install.wim解压
→ 文件复制
→ 应用Windows镜像
```

失败通常发生在以下阶段：

```
应用镜像
→ 配置驱动程序
→ 安装设备
→ 首次重启准备
→ Windows OOBE设置
```

对于联想小新，可能的原因如下：

## 1. 存储驱动 / Intel VMD-RST问题（仍然可能）

即使安装程序能够识别SSD，Windows在从WinPE驱动切换到已安装系统时仍可能失败。

尝试：

BIOS设置：

```
Intel VMD Controller → 禁用
Storage Mode → AHCI
```

然后重新安装。

---

## 2. 损坏的USB介质 / ISO文件损坏

在75%时，Windows正在读取和展开大量文件。损坏的ISO或U盘通常在此处失败。

验证ISO文件：

```bash
sha256sum Win11_25H2_English_x64_v2.iso
```

如果有的话，与微软的SHA256值进行比对。

或者使用Ventoy重新创建U盘：

```bash
sudo ./Ventoy2Disk.sh -i /dev/sdX
```

然后只需将文件复制到U盘：

```
Win11_25H2_English_x64_v2.iso
```

---

## 3. SSD问题

由于你之前看到：

```
Disk 0 512 GB
```

SSD已被检测到，但仍可能发生写入失败。

在Windows安装程序中：

```
Shift + F10
```

运行：

```cmd
diskpart

select disk 0

clean

create partition primary

format fs=ntfs quick

exit
```

然后重试。

---

## 4. 内存不稳定

Windows安装对内存故障异常敏感。

如果总是在大致相同的百分比失败：

* 70–80% → 通常是存储/USB问题
* 随机百分比 → 通常是内存问题

如果可能，运行：

```
memtest86+
```

---

有用的线索是**75%之后的确切错误信息**。

你能拍下失败屏幕的照片吗？尤其是如果出现类似以下内容：

* `Windows cannot install required files`
* `0x8007025D`
* `0x80070002`
* `0xC1900101`
* `The installation failed in the SAFE_OS phase`

错误代码将能立即缩小范围。
