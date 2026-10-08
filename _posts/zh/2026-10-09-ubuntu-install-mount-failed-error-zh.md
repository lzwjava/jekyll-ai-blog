---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu 安装挂载失败错误
translated: true
type: note
---

**问题：** Ubuntu 安装失败并显示此错误，原因是什么？

**回答：**

关键错误是：

```
RuntimeError: Mount failed: /dev/sda2 @ /target/ with options defaults
```

这意味着 Ubuntu 安装程序（Subiquity/Curtin）在安装的分区/格式化步骤中**无法将分区 `/dev/sda2` 挂载到 `/target/`**。常见原因：

**1. 磁盘已被使用 / 忙**

- 分区 `/dev/sda2` 可能已被挂载到其他位置，或被其他进程锁定。

**2. 文件系统损坏或文件系统类型错误**

- 该分区可能包含不兼容或已损坏的文件系统，导致无法挂载。

**3. 驱动器故障或不兼容**

- 坏道或即将损坏的 SSD/HDD 可能导致挂载失败。

**4. RAID / LVM 冲突**

- 如果该磁盘之前是 RAID 阵列或 LVM 组的一部分，残留的元数据可能会阻止挂载。

**5. 安全启动 / 驱动问题**

- 某些 NVMe 或 SATA 控制器需要特定驱动程序。

---

**如何修复：**

1. **尝试“擦除磁盘并安装 Ubuntu”** — 让安装程序从头擦除并重新分区。
2. **打开终端**（安装过程中按 Ctrl+Alt+T）并运行：

   ```bash
   sudo wipefs -a /dev/sda
   sudo fdisk /dev/sda  # 重新创建分区表
   ```

3. **检查磁盘健康状态：**

   ```bash
   sudo smartctl -a /dev/sda
   ```

4. **停用旧的 LVM/RAID：**

   ```bash
   sudo dmsetup remove_all
   sudo vgchange -an
   ```

5. **尝试不同的 USB 启动盘** — ISO 镜像可能已损坏。

---

**参考资料：**

- [Ubuntu 安装错误 – Ask Ubuntu](https://askubuntu.com/questions/tagged/installation)
- [Curtin block_meta.py 源码 – GitHub](https://github.com/canonical/curtin)
- [Ubuntu 安装过程中挂载失败 – Ubuntu Forums](https://ubuntuforums.org/forumdisplay.php?f=335)
