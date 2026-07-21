---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nvidia-smi 被安全启动阻止
translated: true
type: note
---

**概要：**

- **检测到 GPU：** RTX 4070 (AD104)
- **nvidia-smi 二进制文件：** ✅ 已安装
- **驱动程序：** ✅ nvidia-driver-580 (580.167.08) 已安装，DKMS 模块已为两个内核构建
- **nvidia-smi 运行失败原因：** ❌ 安全启动已**启用**，内核拒绝未签名的模块
- **需要修复：** 签署模块或禁用安全启动 → 之后 `nvidia-smi` 将正常工作

请您选择 — 选项 A（签署模块）还是选项 B（禁用安全启动）？
