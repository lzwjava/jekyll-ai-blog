---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 32GB交换文件已创建并激活
translated: true
type: note
---

已完成。交换分区现已激活，重启后仍将继续生效。

## 总结

**已创建并启用一个 32 GB 的交换文件：**

```
NAME       TYPE  SIZE  USED  PRIO
/swapfile  file   2G     0B    -2   (现有)
/swapfile2 file  32G     0B    -3   (新建)
Swap total: 33GiB
```

**具体操作：**

1. `sudo fallocate -l 32G /swapfile2` — 分配一个 32 GB 的交换文件（`/` 分区剩余约 115G，空间充足）
2. `sudo chmod 600 /swapfile2` — 设置正确权限（交换文件必须仅 root 可读写）
3. `sudo mkswap /swapfile2` + `sudo swapon /swapfile2` — 格式化并激活该交换文件
4. 在 `/etc/fstab` 中添加 `/swapfile2 none swap sw 0 0` — 确保**重启后自动生效**

**验证结果：**

- `swapon --show` 确认两个交换文件均已激活（总计 33GiB）
- `free -h` 显示 `Swap: 33Gi 0B used`
- `findmnt` 关于 `/swapfile2` 是*普通文件*的警告属于**预期且无害** — 交换文件本身即为普通文件，并非错误。

**后续建议（此前推荐仍然适用）：** 现在的交换分区起到了安全网的作用 —— 如果 `train_tokenizer.py` 再次超出内存，数据会写入磁盘（速度变慢，但不会导致系统冻结、OOM 被杀或强制重启）。不过，分词器训练在完整 11.5 GB 语料上仍会占用约 40 GB 内存，因此为了获得最佳效果，建议在随机样本（几百 MB 到 1 GB）而非整个文件上进行训练。无论如何，交换分区都能保护系统。
