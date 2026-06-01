---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X GPU 状态报告
translated: true
type: note
---

以下是快速 GPU 状态：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MI300X GPU 状态 — rocm-smi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GPU 利用率：  100%       ← 完全饱和
VRAM 使用量：        63.5 GB / 192 GB  (33%)
功耗：            747W / 750W 上限    ← 运行在极限
结温：    75°C
显存温度：      50°C
SCLK（GPU）：       1351 MHz
MCLK（显存）：    900 MHz
风扇：              0%（被动/服务器散热）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

后续可用的关键命令：

  rocm-smi                              # 快速概览（类似 nvidia-smi）
  rocm-smi -a                           # 所有详细信息
  rocm-smi --showuse --showmeminfo vram # GPU 利用率 + VRAM
  rocm-smi --showtemp --showpower       # 温度 + 功耗
  rocm-smi --showclocks                 # 时钟频率
  watch -n1 rocm-smi                    # 实时监控

GPU 利用率 100%，功耗 747W（接近 750W 上限），结温 75°C —— 对于持续的训练负载来说一切正常。VRAM 仅使用了 33%，因此如果需要，您有充足的空间来扩大批量大小或模型规模。