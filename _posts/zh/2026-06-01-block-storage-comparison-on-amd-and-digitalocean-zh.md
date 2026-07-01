---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在AMD和DigitalOcean上的块存储比较
translated: true
type: note
---

**问题：** 块存储/卷在 AMD Dev Cloud 和 DigitalOcean 上是如何工作的——其机制是什么，以及如何使用？

**回答：**

## 块存储：实际工作原理

在基础设施层面，**网络块存储**（通过数据中心网络的 NVMe-oF 或 iSCSI）将远程磁盘暴露为本地块设备。Hypervisor/驱动程序将远程卷映射到 VM 内部的 `/dev/sdX` 或 `/dev/vdX` 设备节点。从操作系统的角度看，它与本地磁盘无异——你可以对其进行分区、格式化、挂载和使用。

```
你的 Droplet/实例
  ↕ virtio-blk / NVMe-oF 驱动
存储节点（独立的物理硬件）
  ↕ 高带宽数据中心网络
  原始块设备暴露为 /dev/sda、/dev/vda 等
```

"分离与重新附加"的特性之所以有效，是因为存储节点独立保存数据——你的计算实例相对于卷是无状态的。

---

## DigitalOcean Volumes

### 概念

- NVMe SSD，通过网络连接
- 每个卷最大 16 TB，每个 Droplet 最多 10 个卷
- 按 GB/月计费，独立于 Droplet 生命周期持久存在
- 可在**同一区域**内的 Droplet 之间迁移

### CLI 工作流 (doctl)

```bash
# 安装 doctl
brew install doctl
doctl auth init

# 创建卷
doctl compute volume create my-data \
  --region sfo3 \
  --size 100GiB \
  --fs-type ext4

# 附加到正在运行的 Droplet
doctl compute volume-action attach <volume-id> <droplet-id>

# 在 Droplet 内部——找到设备
lsblk
# 通常显示为 /dev/sda 或 /dev/disk/by-id/scsi-...

# 挂载
sudo mkdir -p /mnt/data
sudo mount -o discard,defaults /dev/sda /mnt/data

# 重启后持久化
echo '/dev/sda /mnt/data ext4 discard,defaults 0 0' | sudo tee -a /etc/fstab
```

### 在 Droplet 之间迁移卷

```bash
# 从旧 Droplet 分离
doctl compute volume-action detach <volume-id> <droplet-id-old>

# 附加到新 Droplet（GPU Droplet 等）
doctl compute volume-action attach <volume-id> <droplet-id-new>
```

这是关键用例——你的数据集或模型权重保存在卷上，你可以启动一个便宜的 CPU Droplet 进行预处理工作，然后重新附加到 GPU Droplet 进行训练。仅在需要时才为计算付费。

---

## AMD Dev Cloud (devcloud.amd.com)

AMD Dev Cloud 使用略有不同的模型——它更像是一个**带有项目级存储的托管云**，而不是原始的 IaaS 块设备市场。以下是实际的工作方式：

### AMD Dev Cloud 上的存储层级

| 类型 | 位置 | 用途 |
| ------ | -------- | ---------- |
| 实例本地存储 | MI300X 节点上的 NVMe | 快速临时存储，临时数据 |
| 持久化项目存储 | 网络附加，按账户 | 数据集，检查点 |
| 对象存储（如启用） | S3 兼容端点 | 大型数据集暂存 |

他们 UI 中的"Volumes"概念映射到**在实例终止后仍持久存在的块设备**——类似于 DO Volumes，但范围限定在你的 AMD Dev Cloud 项目内。

### 实际工作流

```bash
# SSH 进入你的 AMD Dev Cloud 实例
ssh user@<amd-instance-ip>

# 检查附加了哪些块设备
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE

# 如果卷已附加但未挂载
sudo mkfs.ext4 /dev/sdb          # 仅在第一次！
sudo mkdir -p /mnt/volume
sudo mount /dev/sdb /mnt/volume

# 持久化
echo '/dev/sdb /mnt/volume ext4 defaults 0 0' | sudo tee -a /etc/fstab
```

具体针对 AMD Dev Cloud——由于你使用的是 MI300X（$2/小时），关键模式是：

```bash
# 停止实例前——干净地卸载
sudo umount /mnt/volume

# 通过 UI 或 CLI 分离，然后重新附加到新实例
# 在新实例上：
sudo mount /dev/sdb /mnt/volume
# 你的数据在那里
```

---

## 你的 ML 工作流的关键模式

由于你在 AMD Dev Cloud 上进行模型训练：

```
[卷：500GB]
  ├── /datasets/         ← HuggingFace 数据集，预处理
  ├── /checkpoints/      ← model.pt 每 N 步保存
  └── /runs/             ← wandb 本地日志，指标

工作流：
1. 启动 MI300X 实例（$2/小时）
2. 附加卷 → 挂载到 /mnt/vol
3. 训练 → 检查点保存到 /mnt/vol/checkpoints/
4. 停止实例（计费停止）
5. 卷持久存在 → 下次会话重新附加
```

这可以避免在实例终止或切换机器时重新下载数据集或丢失检查点。

---

## 注意事项

- **区域锁定**：卷只能附加到同一区域的实例——创建前请检查
- **一次只能附加到一个实例**：一个卷同时只能附加到一个实例（它是块设备，而非共享文件系统——如需共享使用，需要在其上搭建 NFS 或使用对象存储）
- **`discard` 挂载标志**：对 NVMe 卷使用它——启用 TRIM，可防止性能下降
- **XFS 与 ext4**：XFS 处理大文件（模型检查点、数据集分片）更好；ext4 适合一般用途
- **不要两次运行 `mkfs`**：格式化会销毁数据——仅首次使用时格式化
