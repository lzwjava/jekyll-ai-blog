---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 防止Rsync损坏Containerd数据
translated: true
type: note
---

```
containerd:    已停止（6分钟前死亡）
rsync:         活跃中，正在复制59G的containerd数据到卷
根磁盘:        697G，已用88G（剩余610G）——空间充足
卷:             100G，已用60G（剩余35G）——空间不足！
```

**立即停止 rsync。** 存在两个问题：

1. **卷仅有35G空闲，而containerd数据为59G** —— 数据会填满卷并在中途崩溃。
2. **`rsync -a` 会破坏硬链接** —— containerd快照内部使用硬链接。经过rsync后，数据会被损坏。

```bash
# 终止 rsync
kill 6595 6602 6603

# 清理部分复制的内容
rm -rf /mnt/volume_atl1_1780280110689/containerd-data/

# 重启 containerd 以使 Docker 恢复工作
systemctl start containerd
```

**实际解决方案：你根本不需要移动它。** 你的根磁盘有 **610G 空闲空间**。59G 的 containerd 数据留在原处完全没问题。卷较小（100G）且已使用了60%——它根本不是合适的迁移目标。

如果你后续确实需要空间，只需执行 `docker system prune -af` 来清理未使用的镜像。需要我帮你终止那个 rsync 并重启 containerd 吗？