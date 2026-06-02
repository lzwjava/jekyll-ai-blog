---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 改为在 GPU Droplet 上准备数据
translated: true
type: note
---

完全正确——您当前的 VPS 拥有 **10GB disk + 512MB RAM**，无法处理 61GB 输入 + ~30GB 输出 = **~91GB 总计**。

但是这里有一个更好的方法：**完全不在 VPS 上准备。**

## 推荐：在 GPU Droplet 上准备

```
┌─────────────────┐    just transfer raw     ┌─────────────────┐
│   VPS (current) │  ─── 61GB text file ───  │  GPU Droplet    │
│  1 vCPU, 512MB  │      (rsync/scp)        │  (has GPU + big │
│   10GB disk     │                          │   disk + RAM)   │
└─────────────────┘                          └────────┬────────┘
                                                     │
                                            run prepare.py here
                                                     │
                                            ~30GB .bin files
                                            ready for training
```

### 在 GPU Droplet 上（大磁盘，快速 CPU）

```bash
# 传输原始文本文件
rsync -avz --progress root@159.89.216.20:/root/zz/datasets/fineweb_extracted_all.txt ./

# 链接并准备（使用 GPU Droplet 的资源）
ln -sf fineweb_extracted_all.txt ./data/fineweb/train_fineweb.txt
python data/fineweb/prepare_fineweb.py

# 然后在同一机器上立即训练
python train.py config/train_fineweb.py
```

### 为什么这样做有道理

| 任务 | VPS | GPU Droplet |
|------|-----|-------------|
| **准备数据** | ❌ 太弱 | ✅ 强大的 CPU + 大磁盘 |
| **训练模型** | ❌ 无 GPU | ✅ 有 GPU |
| **托管代码** | ✅ 可以 | ✅ 可以 |

**VPS 只存储原始的 61GB 文件。GPU Droplet 执行所有繁重工作。**

您的 GPU Droplet 有什么规格？
