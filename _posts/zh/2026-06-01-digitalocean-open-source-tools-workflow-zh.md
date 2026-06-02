---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DigitalOcean 开源工具工作流
translated: true
type: note
---

是的，DigitalOcean 的所有内容都是开源的。以下是与你相关的全部信息：

## 主仓库

**`digitalocean/doctl`** — DigitalOcean API 的官方命令行工具，使用 Go 语言编写。

```
https://github.com/digitalocean/doctl
```

在 GitHub 上的 `digitalocean/doctl` 仓库中可以找到源代码或提交问题。另有一篇专门教程："How To Work with DigitalOcean Block Storage Using doctl"。

## 卷相关源代码

卷命令位于 GitHub 上的 `doctl/commands/volumes.go` 文件中 — 你可以直接查看 `volume create`、`volume delete`、挂载/卸载等命令的具体实现。块存储卷的容量范围从 1GiB 到 16TiB，并且可以在同一区域内的云主机之间迁移。

## 在你的 MacBook 上安装

```bash
# macOS
brew install doctl

# 认证
doctl auth init
# 粘贴你的 DO API token
```

## 关键卷命令（适用于你的工作流程）

```bash
# 列出所有卷
doctl compute volume list

# 创建 200GB 卷
doctl compute volume create ml-data \
  --region sfo3 \
  --size 200GiB \
  --fs-type ext4

# 挂载到云主机
doctl compute volume-action attach <volume-id> <droplet-id>

# 卸载卷（销毁前执行）
doctl compute volume-action detach <volume-id> <droplet-id>

# 销毁云主机（卷保留）
doctl compute droplet delete <droplet-id> --force

# 列出快照
doctl compute snapshot list
```

## 其他实用资源 — DigitalOcean 的其他开源仓库

```
github.com/digitalocean/godo        # Go SDK（doctl 内部使用的库）
github.com/digitalocean/terraform-provider-digitalocean  # Terraform 提供商
```

**`godo`** 适合需要自行构建 Go 自动化脚本的场景 — 提供与 doctl 相同的 API 接口，但以库的形式使用。

## 针对你的工作流程 — 编写完整的会话脚本

由于你自己编写 CLI 工具（`ww`、`zz`、`iclaw`），可以将上述操作封装为 shell 脚本：

```bash
#!/bin/bash
# ml-session.sh

VOLUME_ID="your-volume-id"
SNAPSHOT_ID="your-os-snapshot-id"
REGION="sfo3"
SIZE="g-8vcpu-32gb-nvidia-l40s-1"  # 或你的 MI300X 标识

case $1 in
  start)
    # 从快照创建云主机
    DROPLET_ID=$(doctl compute droplet create amd-gpu \
      --image $SNAPSHOT_ID \
      --size $SIZE \
      --region $REGION \
      --ssh-keys $(doctl compute ssh-key list --no-header --format ID) \
      --wait \
      --format ID --no-header)

    # 挂载卷
    doctl compute volume-action attach $VOLUME_ID $DROPLET_ID --wait

    # 获取 IP
    IP=$(doctl compute droplet get $DROPLET_ID --format PublicIPv4 --no-header)
    echo "已就绪：ssh root@$IP"
    ;;

  stop)
    DROPLET_ID=$(doctl compute droplet list --format ID,Name --no-header | grep amd-gpu | awk '{print $1}')
    doctl compute volume-action detach $VOLUME_ID $DROPLET_ID --wait
    doctl compute droplet delete $DROPLET_ID --force
    echo "云主机已销毁，卷保留。"
    ;;
esac
```

```bash
./ml-session.sh start   # 启动环境，挂载卷，显示 IP
./ml-session.sh stop    # 卸载卷，销毁云主机
```

一个命令启动训练会话，一个命令干净地结束。完美适应你的终端优先工作流程。
