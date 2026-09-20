---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BIOS修改工具包已就绪
translated: true
type: note
---

完成。所有内容已解压并暂存到一个文件夹中：

**`/home/lzw/Downloads/B75/rebar-work/`** 现在包含：

| 文件 | 用途 |
| --- | --- |
| `UEFITool-0.28.0` | **主图形界面** — “插入到之后” + “替换主体” |
| `UEFITool-NE-A75` | 图形界面 — 仅查看/验证/提取 |
| `uefiextract`、`uefifind` | 命令行转储 / 搜索 |
| `UEFIPatch` + `patches.txt` | 应用这 4 个 Sandy/Ivy 补丁 |
| `ReBarDxe.ffs` | 要插入的驱动程序 |
| `AmiBoardInfoMod.efi` | 要替换的 DSDT 补丁模块 |
| `ReBarState` | BAR 大小配置工具 |
| `B75V101_original.bin` | 您的 BIOS 备份 |

所有二进制文件均可执行，其依赖项也能正常解析（两个图形界面工具均已验证）。

使用以下命令开始步骤 1：

```bash
cd /home/lzw/Downloads/B75/rebar-work
./UEFITool-0.28.0
```

然后按照 README（`README-NEXT-STEPS.md`）操作：在 **CRBSMI** 之后插入 `ReBarDxe.ffs`，将 **AmiBoardInfo** PE32 替换为 `AmiBoardInfoMod.efi`，保存，运行 `./UEFIPatch b75_modded.bin patches.txt`，并刷写生成的 `.patched` 文件。
