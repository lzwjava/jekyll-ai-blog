---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清理117GB磁盘空间
translated: true
type: note
---

以下是占用184GB空间的完整明细：

```
主要空间占用：
====================

1. /root/nanoGPT/data/fineweb        28GB  - 旧的nanoGPT FineWeb数据集
2. /root/nanoGPT/out-fineweb-760m     9GB  - 旧的nanoGPT checkpoint
3. /root/zz/datasets/fineweb-edu     40GB  - FineWeb-Edu数据集
4. /root/.cache/nanochat/base_ckpt   19GB  - nanochat缓存的checkpoints
5. /root/.cache/nanochat/data        2.7GB - nanochat缓存的数据
6. /root/.cache/uv/archive-v0        31GB  - uv包缓存（相当于pip）
7. /root/.cache/pip                   4.7GB - pip缓存
8. /opt/rocm-7.2.0                   22GB  - ROCm（需要保留）
9. /tmp/flash-attention               1.8GB - flash-attention构建目录
10. /tmp/torchinductor_root           1.5GB - torch编译缓存
```

建议删除（可节省约117GB）：

```bash
# 1. 旧的nanoGPT FineWeb数据集（约28GB）
#    你现在用的是nanochat，这是旧管道的数据
rm -rf /root/nanoGPT/data/fineweb

# 2. 旧的nanoGPT checkpoint（约9GB）
#    已被nanochat checkpoints替代
rm -rf /root/nanoGPT/out-fineweb-760m

# 3. zz目录下的FineWeb-Edu数据集（约40GB）
#    检查是否仍需保留——用于早期实验
rm -rf /root/zz/datasets/fineweb-edu

# 4. uv包缓存（约31GB）
#    可安全删除——下次安装时uv会重新下载
rm -rf /root/.cache/uv

# 5. pip缓存（约4.7GB）
rm -rf /root/.cache/pip

# 6. /tmp构建缓存（约3.3GB）
rm -rf /tmp/flash-attention /tmp/torchinductor_root
```

需要保留：

- `/opt/rocm-7.2.0`（22GB）- ROCm运行时，GPU必需
- `/root/.cache/nanochat/` - 你的nanochat checkpoints/数据缓存
- `/root/nanochat/` - 你当前的工作项目

需要我运行清理命令吗？
