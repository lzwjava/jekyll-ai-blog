---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重启AMD实例以修复FLUX
translated: true
type: note
---

仍然宕机。需要从 **AMD Radeon 云控制台**重启实例——OOM 崩溃杀死了 31154 端口上的 SSH 守护进程。

重启后，我将：

1. **通过 SSH 登录**，使用修复后的脚本（无 `.to("cuda")`，改用 `enable_sequential_cpu_offload()`）
2. **删除 FLUX.2-dev**（166GB，对于 48GB 显存来说过大）
3. **下载 FLUX.1-dev**（约 35GB，12B 参数——适合 48GB 显存）
4. **生成**图像，使用正确的内存设置

恢复后请告知！