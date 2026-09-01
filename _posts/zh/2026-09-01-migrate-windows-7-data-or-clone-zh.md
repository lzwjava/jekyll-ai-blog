---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 迁移 Windows 7 数据或克隆
translated: true
type: note
---

**问题：** 如何将带有 C、D、E、F 盘（每个约 60 GB）数据的 Windows 7 迁移到新计算机？

**回答：**

这里主要有两种情况——仅迁移**数据（文件）**，或迁移**完整的操作系统+数据**。以下是清晰的说明：

---

## 🗂️ 方案 A：新计算机已安装 Windows（推荐）

这是最简单也最实用的路径。您只需要将 C/D/E/F 盘中的**数据文件**移动过去。

### 方法 1 — 外部硬盘（最简单）

由于您总共有约 240 GB（4 个盘 × 60 GB），请准备一个 **500 GB 或 1 TB 的 USB 外部硬盘**。

以下是迁移所有内容的清晰分步流程：---

**问题：** 如何将带有 C/D/E/F 盘（每个约 60 GB）的 Windows 7 PC 迁移到新计算机？

**回答：**

您有两条主要路径，具体取决于新计算机是否已安装 Windows。

---

## ✅ 路径 A — 仅数据（新电脑已安装 Windows）

这是最简单的方法。您可以将外部硬盘连接到旧电脑，从每个盘（C、D、E、F）复制文件，弹出硬盘后插入新电脑，再将文件复制过去。由于总计约 240 GB，您至少需要一个 **500 GB 的 USB 外部硬盘**。

您会得到什么：您的所有**数据文件**（文档、照片、视频等）

您不会得到什么：已安装的程序——这些程序需要在新电脑上重新安装。

**步骤：**

1. 购买一个 500 GB 的 USB 外部硬盘
2. 在旧电脑上：在外部硬盘上创建名为 D_drive、E_drive、F_drive 的文件夹
3. 将 D:、E:、F: 中的所有内容复制到这些文件夹中
4. 对于 C:，仅复制个人数据（桌面、文档、下载、图片、音乐、视频）——不要复制系统文件
5. 将外部硬盘插入新电脑并复制所有内容

---

## 🖥️ 路径 B — 完整操作系统克隆（移动 Windows + 应用程序）

如果您想把 Windows 7 本身、所有已安装的程序以及所有数据都带到新计算机，则需要镜像软件。像 AOMEI Backupper 这样的工具允许您创建系统镜像备份，然后在新电脑上恢复时使用 Universal Restore，该功能可处理不兼容的硬件，使 Windows 能在不同的硬件上正常启动。

**推荐的免费工具：**

- **Macrium Reflect Free** — 可靠、简单明了
- **AOMEI Backupper Free** — 也支持 Universal Restore

**步骤：**

1. 在旧电脑上安装 Macrium Reflect 或 AOMEI
2. 为每个盘（C、D、E、F）创建完整磁盘镜像，并保存到外部硬盘
3. 在新电脑上，从救援 USB/CD（由同款软件创建）启动
4. 恢复时，启用“Universal Restore”以确保计算机在具有不同硬件的新电脑上恢复后能够启动
5. 在 BIOS 中调整启动顺序，以便从恢复的驱动器启动

---

## ⚠️ 关于 Windows 7 的重要警告

请注意，**Windows 7 已到生命周期终点**（支持于 2020 年 1 月结束），这意味着没有安全更新。如果新电脑性能足够强大，强烈建议升级到 Windows 10 或 11，并且只迁移您的数据（路径 A），而不是操作系统本身。

---

**参考资料：**

- [如何迁移到新的 Windows PC – Computerworld](https://www.computerworld.com/article/1638368/how-to-migrate-to-a-new-windows-pc.html)
- [将 Windows 7 迁移到新计算机 – AOMEI](https://www.ubackup.com/universal-restore/move-windows-7-installation-to-new-computer-0528.html)
- [将 Windows 7 传输到新硬盘 – ubackup.com](https://www.ubackup.com/windows-7/transfer-windows-7-to-new-hard-drive-without-cd-6988.html)
