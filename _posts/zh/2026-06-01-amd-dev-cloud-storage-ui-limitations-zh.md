---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD开发云存储UI限制
translated: true
type: note
---

**问题：** 为什么在 AMD Dev Cloud 门户 UI 中看不到块存储/卷选项？是否需要改用 API？

**答案：**

AMD Dev Cloud 由 DigitalOcean 基础设施提供支持（您可以在其门户底部看到“Powered by DigitalOcean”）。不过，AMD 使用的是**定制/受限的门户**——他们仅在 UI 中暴露 DigitalOcean 的部分功能。块存储卷就是 AMD Dev Cloud 门户 UI 中未提供的功能之一。

您的可选方案：

## 方案 1：直接使用 DigitalOcean API

AMD Dev Cloud 为您提供 API 访问权限。前往 **设置 → API → Tokens** 生成一个令牌，然后使用标准的 DigitalOcean API：

```bash
# 创建卷
curl -X POST https://api.digitalocean.com/v2/volumes \
  -H "Authorization: Bearer $AMD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "size_gigabytes": 500,
    "name": "ml-data-vol",
    "region": "atl1",
    "filesystem_type": "ext4"
  }'

# 列出卷
curl -X GET https://api.digitalocean.com/v2/volumes \
  -H "Authorization: Bearer $AMD_API_TOKEN"

# 将卷挂载到 droplet 上
curl -X POST https://api.digitalocean.com/v2/volumes/actions \
  -H "Authorization: Bearer $AMD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "attach",
    "droplet_id": YOUR_DROPLET_ID,
    "region": "atl1"
  }'
```

## 方案 2：使用 `doctl` CLI

```bash
# 安装
brew install doctl  # 或在 Ubuntu 上使用 snap install doctl

# 使用您的 AMD 令牌进行认证
doctl auth init --access-token $AMD_API_TOKEN

# 在 atl1 区域创建卷
doctl compute volume create ml-data-vol \
  --size 500GiB \
  --region atl1 \
  --fs-type ext4

# 挂载到 droplet
doctl compute volume-action attach VOLUME_ID --droplet-id DROPLET_ID

# 挂载后，在 droplet 上：
# lsblk  → 找到新磁盘（例如 /dev/sda）
# mkfs.ext4 /dev/sda  （如果是新磁盘）
# mount /dev/sda /mnt/data
```

## 可能的限制

并非所有 DigitalOcean 区域都支持块存储，**ATL1 可能功能受限**，因为它是 AMD 的专用数据中心。先通过 API 检查：

```bash
curl -X GET "https://api.digitalocean.com/v2/regions" \
  -H "Authorization: Bearer $AMD_API_TOKEN" \
  | python3 -c "
import json, sys
regions = json.load(sys.stdin)['regions']
atl = [r for r in regions if 'atl' in r['slug']]
print(json.dumps(atl, indent=2))
"
```

查看 ATL1 区域响应中的 `features` 字段——如果包含 `private_networking` 但不包含 `storage`，则说明 ATL1 根本不支持块存储。

## ML 工作负载的实用替代方案

如果 ATL1 不支持块存储，存储大型数据集的最佳方案是：

```bash
# 使用 Spaces（兼容 S3 的对象存储）——始终可通过 API 使用
# 上传数据集
aws s3 cp ./dataset s3://your-space/ \
  --endpoint-url https://atl1.digitaloceanspaces.com

# 或从本地机器直接 rsync 到 droplet
rsync -avz --progress ./data/ root@<droplet-ip>:/mnt/data/
```

查看 AMD Dev Cloud 支持页面或提交支持工单——考虑到 ML 工作负载对存储的需求，他们可能会应请求为 MI300X droplet 启用卷功能。