---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Chinchilla训练脚本命令
translated: true
type: note
---

第10,000步的检查点已存在。脚本已就绪：

```
/mnt/data/nanochat/run_rtx4070_chinchilla.sh
```

从第0步开始全新运行：

```
bash /mnt/data/nanochat/run_rtx4070_chinchilla.sh
```

从已存在的第10k步检查点恢复运行：

```
bash /mnt/data/nanochat/run_rtx4070_chinchilla.sh --resume-from-step=10000
```

功能说明：

```
  87,000步 x 65,536批次 = 57亿token（Chinchilla最优）
  每10k步保存检查点（防崩溃）
  每2k步评估，每5k步采样
  在RTX 4070上约需28.5小时
  数据：磁盘上1426亿token，仅需57亿token
```

运行？或者想先调整任何参数（评估频率、保存频率等）？
