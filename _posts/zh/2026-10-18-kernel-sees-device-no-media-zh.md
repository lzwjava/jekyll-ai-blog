---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内核检测到设备，无介质
translated: true
type: note
---

内核*确实*看到了设备——但闪存控制器报告**无介质**。以下是 `dmesg` 中发生的事情：

## 日志显示的内容

该 U 盘在约 40 秒内**以三个不同的身份枚举了三次**，然后丢失了介质：

```
1-4.3: idVendor=... General UDisk      → [sdb] 7864320 blocks (4 GB), sdb1
       → sdb: detected capacity change from 7864320 to 0   ← 容量消失
       → USB disconnect

1-4.3: idVendor=346d, idProduct=5678  Product: "Disk 2.0"
       VendorCo ProductCode → [sdb] 30720000 blocks (15 GB), sdb1 sdb2
       FAT-fs: Volume was not properly unmounted...
       → USB disconnect  (+ lost async page writes, device offline errors)

1-4.3 / then 1-4.1: idVendor=ffff, idProduct=1201
       NAND USB2DISK 0.00
       sd 8:0:0:0: [sdb] Media removed, stopped polling   ← 当前状态
```

这就是为什么 `lsblk` 显示 `sdb 0B`，`/sys/block/sdb/size` 为 `0`，`fdisk` 提示**`No medium found`**：
- `/dev/sdb` 存在（USB 设备枚举正常）
- 但控制器报告"介质已移除"，因此没有容量，也没有 `/dev/sdb1`。

## 诊断

1. **最可能的原因：U 盘本身已损坏，或者是扩容盘。** 证据：
   - 每次重新插拔都报告*不同*的厂商/产品/容量（`4 GB` → `16 GB` → `ffff:1201`，且无序列号）。
   - `ffff:1201`、`bcdDevice=0.00`、`Mfr=0, Product=0` = 虚假的 USB 描述符（典型的山寨/损坏控制器特征）。
   - 每次连接约 8 秒后自动断开。
   - 之前的会话在它消失时还在写入 → `device offline error ... lost async page write`。

2. **可能的促成因素：它接在 hub 上。** `1-4.3` = hub 端口 3（总线上有 Genesys `05e3:0610`、Terminus `1a40:0101` hub，以及 Realtek 网卡）。廉价 U 盘对 hub 供电敏感。

## 可以尝试的操作

```bash
# 1. 直接插入主板后部 USB 接口（不要经过 hub 或前置面板），
#    最好使用 USB 2.0，然后实时查看日志：
sudo dmesg -w

# 2. 重新插拔后对比：
lsblk -o NAME,SIZE,TRAN
sudo fdisk -l /dev/sdb
```

- 如果直连端口仍然显示 `Media removed` / `ffff:1201` / 容量为 0 → **U 盘已损坏**，只能通过专业工具进行数据恢复（而且它很可能从未拥有所宣传的容量）。
- 如果恢复为真实容量，请在拔除前先干净卸载：
  ```bash
  sudo fsck.vfat -a /dev/sdb1   # 它之前"未正确卸载"
  sudo umount /dev/sdb1
  ```
- 在另一台机器上交叉验证——如果那里也显示 `ffff:1201` / 无介质，即可最终确认问题在 U 盘而不是你的电脑。

另外需要注意的是：该磁盘之前曾发生过写入丢失（sdb1 和 sdb2 上的 `lost async page write`），因此请将其上的任何数据视为可疑。