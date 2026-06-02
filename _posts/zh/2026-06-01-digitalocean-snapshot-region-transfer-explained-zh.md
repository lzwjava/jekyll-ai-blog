---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DigitalOcean快照区域传输详解
translated: true
type: note
---

**问题：** DigitalOcean 中的 "Add snapshot to additional regions" 是什么意思？另外，volume 快照能否跨区域传输？

**回答：**

## DigitalOcean 中的快照跨区域传输

### 含义

当你创建 **Droplet 快照**时，它最初仅存储在该 Droplet 所在的数据中心区域（在你的例子中是 `ATL1`）。

"Add snapshot to additional regions" 的意思是：**将该快照镜像复制到其他 DO 数据中心**，以便你可以在不同区域启动一个完全相同的 Droplet（包含相同的 OS、软件包、配置、数据）。

```
gpu-mi300x-snapshot-20260601 (ATL1, 30.62 GB)
       │
       ├──► ATL1  ✓ (已存在)
       ├──► NYC1  ← 你可以添加此区域
       ├──► SFO3  ← 或者此区域
       └──► SGP1  ← 或者此区域
```

复制完成后，你可以进入目标区域的 **Create Droplet → From Snapshot** 页面，从该快照启动一个新的 Droplet。这就是在需要时将你的 **MI300X 环境克隆**到其他区域的方法。

**要点：**
- 跨区域复制快照不产生额外费用（你只需为快照本身支付存储费用）
- 复制是完整的副本——不是增量或指针
- 传输时间与快照大小成正比（你的 30.62 GB 可能需要几分钟）

---

### Volume 快照 — 概念相同，范围不同

| | Droplet 快照 | Volume 快照 |
|---|---|---|
| 捕获内容 | 整个 Droplet 磁盘（OS + 数据） | 仅 Block Storage 卷 |
| 区域传输 | ✅ 支持 | ✅ 支持（相同 UI） |
| 恢复方式 | 在任意区域创建新 Droplet | 在目标区域创建新 Volume |
| 用途 | 克隆整台机器 | 单独迁移持久化数据盘 |

Volume 快照的工作方式相同——你可以将它们复制到其他区域，然后在那里创建新的 Block Storage 卷。当你的数据卷与 Droplet 分离，并且你只想迁移或复制数据时，这非常有用。

---

### 针对你的 AMD Dev Cloud 环境的实用工作流程

如果你希望在第二个区域启动你的 MI300X 环境（例如为了降低延迟或实现冗余）：

```bash
# 1. 从 DO UI 或 CLI：将快照复制到新区域
doctl compute snapshot get <snapshot-id>
doctl compute droplet create \
  --region sfo3 \
  --image <snapshot-id> \
  --size gpu-mi300x-192gb \
  --ssh-keys <your-key-id> \
  my-mi300x-sfo3
```

新的 Droplet 将使用你完全相同的环境启动——相同的 conda 环境、相同的模型权重、相同的 dotfiles——只是位于不同的地理区域。

**总结：** 这是一种区域复制机制，用于灾难恢复、延迟优化或在多个区域并行启动相同的 GPU 环境。
