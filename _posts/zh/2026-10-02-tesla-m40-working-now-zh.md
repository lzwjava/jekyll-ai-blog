---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla M40 现已工作
translated: true
type: note
---

现在可以正常工作了。🎉

```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.178.04             Driver Version: 580.178.04     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|=========================================+========================+======================|
|   0  Tesla M40                      Off |   00000000:01:00.0 Off |                    0 |
| N/A   28C    P8             15W /  250W |       4MiB /  11520MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
```

**Tesla M40 现在已完全初始化：**
- ✅ `nvidia-smi` 正常工作，退出码为 0
- ✅ 显卡已识别：`Tesla M40`，UUID `GPU-9d2f8eda-4ad8-2f53-2959-da07ed35e311`
- ✅ 功耗：空闲 15W / 上限 250W —— 电源线问题已解决
- ✅ 温度：28°C，P8 空闲状态，健康
- ✅ 11520 MiB 显存（12 GB 的 M40），CUDA 13.0

上面只运行了 `gnome-shell`（占用 1 MiB）—— 显卡其余时间处于空闲状态，随时可以进行计算。你做了什么，重新连接了 EPS 8 针电源线？