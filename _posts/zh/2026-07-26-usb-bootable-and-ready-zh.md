---
audio: false
generated: true
image: false
lang: zh
layout: post
title: USB可启动并就绪
translated: true
type: note
---

### ✅ EFI Boot Confirmed

```
/media/lzw/WIN11/efi/boot/bootx64.efi → PE32+ executable (EFI application) x86-64
```

**UEFI bootloader 存在且有效。** 此 USB 已准备就绪，可以启动。

### 总结

| 问题 | 回答 |
|---|---|
| **USB 是否已 bootable？** | ✅ **是** — 已通过手动 FAT32 + wimsplit 准备完成 |
| **是否需要使用其他工具重新 flash？** | ❌ **不需要** — 它已经是正确的 |
| **改用 Ventoy？** | 仅当当前 USB 在您的 Lenovo Xiaoxin 上 boot 失败时 |
| **在 Lenovo Xiaoxin 上可能出什么问题？** | Intel VMD/RST — SSD 不会显示，除非加载 driver |

**建议：** 只需插入并尝试 boot。您可以直接使用。如果 Windows installer 在 Xiaoxin 上找不到 SSD，请从 Intel 官网下载 Intel RST driver (F6 driver)，放入单独的 USB，然后在安装期间通过 `Load Driver` 加载 — 这是 Lenovo Xiaoxin 机器上最常见的问题。