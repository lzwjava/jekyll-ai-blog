---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UEFITool 验证版 0.28.0 插入版
translated: true
type: note
---

已下载并验证。现在位于 `/tmp/ueefitool/ueefitool`（UEFITool NE A75，Linux x64，约 4.8 MB），运行正常（GUI 已打开，Qt 库全部解析）。

⚠️ **重要提示：** UEFITool **NE**（A75）**不支持**插入新模块——NE 分支中没有“Insert after”功能。对于 ReBarDxe 插入步骤，你仍然需要之前已下载的**非 NE 版 UEFITool 0.28.0**，位于：

- `/tmp/ueefitool/UEFITool.zip` → 包含 `UEFITool`（0.28.0，非 NE）

所以你的工具现在齐全了：

| 工具 | 用途 | 位置 |
| --- | --- | --- |
| **UEFITool 0.28.0（非 NE）** | 插入 `ReBarDxe.ffs` + 替换 DSDT PE32 | `/tmp/ueefitool/UEFITool.zip` |
| UEFITool NE A75 | 查看/验证、提取（不插入） | `/tmp/ueefitool/ueefitool` |
| UEFIExtract NE A75 | 命令行解包（已使用） | `/tmp/ueefitool/ueefiextract` |
| UEFIFind NE A75 | 命令行搜索 | `/tmp/ueefitool/ueefifind` |
| UEFIPatch 0.28.0 | 应用 4 个 Sandy/Ivy 补丁 | `/home/lzw/Downloads/B75/rebar-work/UEFIPatch` |

解压 0.28.0 版本，并使用**那个**版本执行指南中的第 1 步：

```bash
cd /tmp/ueefitool && unzip -o UEFITool.zip && ./UEFITool
```

需要我现在就解压，还是把两个工具都复制到你的 `~/Downloads/B75/rebar-work/` 文件夹中，方便集中管理？
