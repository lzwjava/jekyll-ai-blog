---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 由于BIOS设置导致的GPU初始化失败
translated: true
type: note
---

**问题：** 当 BIOS 中主显示器设置为集成 GPU 时，测试独立 GPU（GT 730）时出现 GPU 初始化错误是否属于预期？

**回答：**

**是的，这很可能是 MODS 初始化失败的根本原因。**

当 BIOS 配置为使用**集成 GPU 作为主显示器**时，系统会将显示资源（帧缓冲、IRQ、内存映射 I/O）分配给 iGPU。独立 GT 730 可能未经过系统固件正确初始化，导致 MODS 尝试直接访问 GPU 硬件时失败。

**正在发生的情况：**

```
FB Base : 0xe0000000   ← 帧缓冲未正确映射
IRQ     : 11           ← IRQ 已分配，但 GPU 未初始化
Error 229              ← 硬件从未完成初始化序列
Error 237              ← 无法设置显示模式（没有主显示器所有权）
```

**要正确使用 MODS 测试独立 GT 730：**

1. **进入 BIOS/UEFI** → 将**主显示器**从 `iGPU` 改为 `PCIe` 或 `PEG`
2. **保存并重启**，然后重新运行 MODS 测试
3. 或者，将显示器直接连接到 **GT 730 的输出接口**
4. 重新运行：

   ```bash
   ./mods gputest.js -skip_rm_state_init
   ```

**如果切换后测试通过** → GT 730 正常，无硬件问题。

**如果切换后测试仍然失败** → GT 730 可能存在硬件缺陷。

---

> 💡 你已在使用的 `-skip_rm_state_init` 标志对于绕过测试是正确的，但它无法克服 GPU 未被 BIOS 初始化的根本问题。
