---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 添加WD Blue 2TB到B760M Mortar
translated: true
type: note
---

问题：鉴于我使用的是微星MAG B760M Mortar WiFi主板，我能否再添加一块内置硬盘（西数蓝盘2TB WD20EZBX）？需要满足的两个条件（空闲SATA接口+3.5英寸硬盘位）是否正确？

回答：

是的，这两个条件都正确——你可以安装WD20EZBX。

让我为你核实这块主板的详细规格。

**SATA接口——B760M Mortar WiFi拥有4个SATA 6Gb/s接口。**因此你总共可安装最多4块SATA硬盘。只要4个接口未被全部占用，再加一块机械硬盘完全没问题。

B760M主板需要注意的一点是：**SATA接口与M.2插槽存在通道共享问题。**在许多B760M Mortar变体版本中，使用特定M.2插槽会禁用某个SATA接口（通道共享）。具体来说，如果在SATA模式的M.2插槽中安装了M.2固态硬盘，可能会导致SATA2（或共享接口）被禁用。请查阅主板手册中的M.2/SATA组合表。如果你只使用NVMe（PCIe）协议的M.2固态硬盘，则不会禁用任何SATA接口——NVMe不像SATA模式的M.2那样与SATA通道产生共享冲突。

购买前快速检查方法：

```bash
# Linux系统——列出当前SATA设备及空闲接口
lsblk -o NAME,SIZE,MODEL,TRAN
# 查看TRAN=sata的条目；统计已占用数量

# 检查SATA控制器及链接状态
sudo dmesg | grep -i sata
```

在Windows系统中，可打开机箱物理清点：统计主板上已连接的SATA数据线数量与空闲SATA接口数，以及电源上未使用的SATA供电接口数量。

**物理硬盘位：**B760M Mortar为mATX规格，这取决于机箱而非主板。任何标准ATX/mATX机箱都具备3.5英寸硬盘位——请确认你的机箱有空闲位。WD20EZBX为标准3.5英寸硬盘。

**你需要准备：**

- 1根空闲SATA数据线（主板通常附赠2根；或单独购买约5元）
- 1个电源空闲SATA供电接口（几乎都有冗余）
- 1个空闲3.5英寸硬盘位及4颗安装螺丝

**结论：**价格方面合理（B760M Mortar WiFi约1299元，WD20EZBX约428元）。只要拥有未被M.2共享禁用的空闲SATA接口和空闲3.5英寸硬盘位，连接后开机即可识别——随后进行分区/格式化。

```bash
# 安装后，Linux系统操作：
sudo fdisk /dev/sdX        # 创建分区
sudo mkfs.ext4 /dev/sdX1   # 格式化
sudo mount /dev/sdX1 /mnt/data
```

值得提醒的一点：WD20EZBX是7200转CMR硬盘——性价比之选（CMR非SMR），适合作为通用存储。如果用于机器学习数据集或高吞吐量场景，SATA固态硬盘或NVMe会快得多，但作为428元的冷数据大容量存储盘，这个选择很扎实。
