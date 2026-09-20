---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UEFITool 修改指南
translated: true
type: note
---

打开 **`UEFITool-0.28.0`**（非 NE 版本）。

NE-A75 **没有**“在后面插入”功能——该功能在 NE 分支中缺失，而插入 `ReBarDxe.ffs` 正是你首先要做的。

运行：

```bash
cd /home/lzw/Downloads/B75/rebar-work
./UEFITool-0.28.0
```

然后在 GUI 中：

1. `File → Open image file…` → `B75V101_original.bin`
2. `File → Search…` → **Header only** → **GUID** → `3C1DE39F-D207-408A-AACC-731CFB7F1DD7` → 双击结果
3. 在树中，滚动到该卷的底部 → 最后一个模块 **CRBSMI** → 右键 → **Insert after…** → `ReBarDxe.ffs`
4. 然后搜索 GUID `9F3A0016-AE55-4288-829D-D22FD344C347`（AmiBoardInfo）→ 打开 **Compressed section → PE32 image section** → 右键点击 PE32 区域 → **Replace body…** → `AmiBoardInfoMod.efi`
5. `File → Save image file…` → `b75_modded.bin`

保留 NE-A75 仅供后续查看/验证时使用（例如检查填充文件）。
