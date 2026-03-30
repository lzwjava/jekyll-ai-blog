---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 DigitalOcean Droplet 之间传输数据
translated: true
type: note
---

Question: 我如何在 DigitalOcean 的普通 Droplet 和 GPU Droplet 之间传输 100GB 的数据？

Answer:

是的 —— 你 **可以在 DigitalOcean 的 Droplet 之间传输 100GB 数据**。针对你的使用场景，有 **4 种常用方法**，按推荐程度排序如下。

---

# ✅ 最佳方法 (推荐): Private Network + rsync/scp

如果两个 Droplet 位于 **同一区域 (Region)**，请使用 **private networking** —— 速度最快且免费。

### 步骤 1 — 获取私有 IP

在两个 Droplet 上分别运行：

```bash
ip a
```

你会看到类似以下内容：

```
10.124.0.5   (droplet A)
10.124.0.8   (GPU droplet)
```

---

### 步骤 2 — 使用 rsync 传输 100GB (效果最好)

在 GPU droplet 上运行：

```bash
rsync -avz --progress root@10.124.0.5:/data/ /data/
```

或者使用 `scp`：

```bash
scp -r root@10.124.0.5:/data /data
```

这是在 Droplet 之间通过 SSH 拷贝文件的标准方法。([DigitalOcean][1])

**为什么这种方法最好**

* 使用内部网络 (fast)
* 不占用公网 bandwidth
* 无需额外存储
* 轻松处理 100GB 数据

---

# ✅ 更好 (最快): 挂载 Volume

这是处理大型 dataset 的 **专业方法**。

工作流：

1. 创建 Volume (100GB)
2. 挂载到廉价的 Droplet
3. 下载 dataset
4. 卸载 Volume
5. 挂载到 GPU Droplet

DigitalOcean 允许在 **同一区域** 的 Droplet 之间移动 Volume。([DigitalOcean Docs][2])

这种方法完全避免了拷贝过程。

速度 = 瞬间完成 (无需传输时间)

---

# 方法 3 — Snapshot Droplet

如果你的整个 Droplet 都有数据：

1. 对 Droplet 制作 Snapshot
2. 从该 Snapshot 创建 GPU Droplet

这将一次性复制所有内容。([DigitalOcean][3])

---

# 方法 4 — 对象存储 (Spaces)

上传 → 下载

```
cheap droplet → DO Spaces → GPU droplet
```

较慢，但可以跨区域 (Region) 工作。

---

# 针对你的训练设置建议

你的计划：

> 廉价 Droplet 下载 100GB
> 然后启动 H100 GPU Droplet
> 进行内网传输

最佳架构：

### 方案 A (简单直接)

```
cheap droplet
    ↓ rsync (private IP)
GPU droplet
```

### 方案 B (专业方案)

```
cheap droplet
    ↓
volume (100GB)
    ↓
GPU droplet
```

方案 B 是 **严肃的训练流水线 (training pipelines) 所采用的方式**。

---

# 实际速度预期

在 DigitalOcean 内部私有网络中：

典型表现：

* 1–10 Gbps 内部带宽
* 100GB 传输时间：

| speed  | time    |
| ------ | ------- |
| 1 Gbps | ~15 min |
| 2 Gbps | ~7 min  |
| 5 Gbps | ~3 min  |

所以 **100GB 只是小意思**。

---

# 示例 (你的具体工作流)

cheap droplet:

```
/dataset/100gb
```

GPU droplet:

```
mkdir /dataset
```

运行：

```bash
rsync -avz --progress root@10.0.0.5:/dataset/ /dataset/
```

完成。

---

# 结论

是的 —— 你的想法是正确的：

廉价 Droplet 下载 → 传输 → 开始 GPU 训练

使用以下任一方式：

1. 基于 private IP 的 rsync (最简单)
2. 挂载 Volume (最佳)
3. Snapshot (完整克隆)

如果你经常操作，我推荐 **Volume 方法**。

References:

* [https://docs.digitalocean.com/products/volumes/how-to/move-between-droplets/](https://docs.digitalocean.com/products/volumes/how-to/move-between-droplets/)
* [https://docs.digitalocean.com/docs/droplets/how-to/transfer-files](https://docs.digitalocean.com/docs/droplets/how-to/transfer-files)
* [https://www.digitalocean.com/community/questions/how-do-i-copy-files-from-my-droplet-to-my-pc-for-backup](https://www.digitalocean.com/community/questions/how-do-i-copy-files-from-my-droplet-to-my-pc-for-backup)
* [https://docs.digitalocean.com/products/paperspace/machines/how-to/transfer-files/](https://docs.digitalocean.com/products/paperspace/machines/how-to/transfer-files/)

[1]: https://www.digitalocean.com/community/questions/how-do-i-copy-files-from-my-droplet-to-my-pc-for-backup?utm_source=chatgpt.com "How do I copy files from my droplet to my PC for backup | DigitalOcean"
[2]: https://docs.digitalocean.com/products/volumes/how-to/move-between-droplets/?utm_source=chatgpt.com "How to Move Volumes between Droplets | DigitalOcean Documentation"
[3]: https://www.digitalocean.com/community/questions/how-to-transfer-one-droplet-all-data-to-another-droplet?utm_source=chatgpt.com "how to transfer one droplet all data to another droplet | DigitalOcean"