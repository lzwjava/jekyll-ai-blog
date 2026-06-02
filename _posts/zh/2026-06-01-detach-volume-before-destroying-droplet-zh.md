---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 销毁液滴前分离卷
translated: true
type: note
---

是的，但要按正确的顺序操作：

## 销毁之前

**1. 检查是否仍有正在运行的程序：**

```bash
# 是否在训练中？
tmux ls

# 是否有进程正在写入卷？
lsof /mnt/data
```

**2. 干净地卸载卷：**

```bash
umount /mnt/data
```

**3. 确认已卸载：**

```bash
df -h  # /mnt/data 应该已消失
```

## 然后从你的 MacBook 执行

```bash
# 获取 droplet ID
doctl compute droplet list

# 先分离卷
doctl compute volume-action detach <volume-id> <droplet-id> --wait

# 再销毁
doctl compute droplet delete <droplet-id> --force
```

## 或者直接通过 DigitalOcean 界面

既然你已经在界面中了：

1. 进入你的 droplet → **Volumes** 标签页 → **Detach** 卷
2. 然后 **Destroy** droplet

---

**关键规则：** 始终先分离再销毁。在卷仍挂载的情况下销毁通常也能成功，但存在风险——可能导致卷的文件系统损坏，而卷里保存着你宝贵的 `train.bin` 和检查点。

卷保留，droplet 消失，$2/小时停止。 ✅
