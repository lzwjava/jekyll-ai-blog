---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD开发者云是白标DigitalOcean
translated: true
type: note
---

**问题：** AMD Developer Cloud 与 DigitalOcean 是如何协作的？观察这个使用 `api.digitalocean.com` 的快照删除脚本，似乎只有网页门户（UI）不同，而 API 端点及后端/数据库都是相同的——这样理解正确吗？

**回答：**

是的，你的推断正确。**AMD Developer Cloud 是 DigitalOcean 的白标/OEM 化部署**。具体分析如下：

## 实际运作方式

AMD Developer Cloud 构建于 **DigitalOcean 的基础设施平台之上**，并在 DO 的数据中心集群中加入了 AMD 专属的 GPU 硬件（MI300X 等）。其关系结构为：

```
AMD Developer Cloud 门户 (amd.com/en/developer/...)
        ↓  (仅前端主题不同)
DigitalOcean 控制平面 API  ← api.digitalocean.com
        ↓
DigitalOcean 后端/数据库（相同的 Droplet/快照/卷基础设施）
        ↓
位于 DO 亚特兰大数据中心的 AMD GPU 硬件节点
```

## 来自您脚本的证据

您的脚本使用 `AMD_DEV_CLOUD_API_KEY`（通过 AMD 门户发放的 DigitalOcean 个人访问令牌）访问 `https://api.digitalocean.com/v2`。这证实了以下几点：

- **API 是 100% 标准的 DigitalOcean v2 API**——不含 AMD 专属端点
- 该令牌是真实的 DO PAT，权限限定在 AMD 预配置的 DO 账户/项目中
- 快照、Droplet、卷均存储在 **DigitalOcean 的后端数据库中**——AMD 仅为您预配置了一个 DO 账户

## AMD 提供的部分

| 层 | 归属方 |
|---|---|
| 网页门户 UI | AMD（定制主题，与 cloud.digitalocean.com 不同） |
| GPU Droplet SKU（MI300X） | AMD（硬件 + BIOS/驱动配置） |
| API 端点 | DigitalOcean（未修改） |
| 账户/计费 | AMD（转售 DO 容量） |
| 快照/卷/网络数据库 | DigitalOcean |
| 支持层级 | AMD 负责 GPU 问题，DO 负责底层基础设施 |

## 实际影响

由于 API 完全相同，**任何 DigitalOcean 的 SDK 或工具都能直接用于 AMD Dev Cloud，无需修改**——仅需更换令牌即可：

```python
import digitalocean  # pydo 或 python-digitalocean

manager = digitalocean.Manager(token=os.environ["AMD_DEV_CLOUD_API_KEY"])
snapshots = manager.get_all_snapshots()
droplets = manager.get_all_droplets()  # 列出您的 MI300X Droplet
```

`doctl` 同样适用：
```bash
doctl auth init --access-token $AMD_DEV_CLOUD_API_KEY
doctl compute droplet list
doctl compute snapshot list
```

您的快照删除脚本是一个简洁、正确的实现——唯一“AMD 专属”的部分就是令牌来源，其余均为标准的 DO API。
