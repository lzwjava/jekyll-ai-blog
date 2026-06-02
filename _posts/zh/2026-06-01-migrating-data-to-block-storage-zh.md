---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将数据迁移至块存储
translated: true
type: note
---

**问题：** 如何设置一个 DigitalOcean 块存储卷，并将我当前的 GPU 云主机上的 130GB 模型/数据文件移动到该卷上？

**回答：**

## 第一步：创建卷

在创建云主机时，在 DigitalOcean 界面中，选择**“Add a Volume”**下的 **“Create new”**：
- 大小：**150GB**（留出余量）
- 将在创建时附加

如果云主机已存在，也可以通过 `doctl` 创建：
```bash
doctl compute volume create my-ml-data \
  --region sfo3 \
  --size 150 \
  --fs-type ext4
```

## 第二步：格式化并挂载（仅首次）

SSH 进入云主机：

```bash
# 检查卷的设备名称（通常是 /dev/sda 或 /dev/disk/by-id/...）
lsblk

# 格式化（仅首次执行一次）
mkfs.ext4 /dev/sda

# 创建挂载点
mkdir -p /mnt/data

# 挂载
mount /dev/sda /mnt/data

# 验证
df -h /mnt/data
```

## 第三步：将 130GB 数据移动到卷上

```bash
# 如果数据当前在根磁盘上
rsync -avh --progress /root/data/ /mnt/data/
# 或者
cp -r /your/model/weights /mnt/data/

# 确认复制无误后，从根磁盘删除
rm -rf /root/data/
```

如果数据在**本地机器或工作站**（192.168.1.36）上，可以直接推送到卷：
```bash
# 从工作站执行
rsync -avh --progress --compress \
  /local/path/to/data/ \
  root@<云主机IP>:/mnt/data/
```

## 第四步：使挂载持久化（同一云主机会话内）

若要在同一云主机重启时自动挂载：
```bash
# 获取 UUID
blkid /dev/sda

# 添加到 fstab
echo "UUID=<你的UUID>  /mnt/data  ext4  defaults,nofail  0  2" >> /etc/fstab
```

## 第五步：会话结束——分离卷，不要快照

```bash
# 卸载前先分离
umount /mnt/data

# 通过 doctl 分离
doctl compute volume-action detach <卷ID> <云主机ID>

# 现在可以安全销毁云主机
doctl compute droplet delete <云主机ID> --force
```

## 第六步：下一次会话——附加并挂载

```bash
# 创建新云主机（从精简的 OS 快照）
doctl compute droplet create ...

# 附加卷
doctl compute volume-action attach <卷ID> <新云主机ID>

# SSH 进入，挂载
mount /dev/sda /mnt/data

# 你的 130GB 数据就在那里，无需等待加载
ls /mnt/data
```

## 你的新工作流程总结

```
旧方式：创建快照（20分钟）→ 恢复（快，但延迟加载）
新方式：卷持久化 → 附加（瞬间）→ 挂载（2秒）→ 开始工作
```

130GB 数据无需移动。它始终保留在卷上，分离状态，闲置时每月约花费 $15，随时可在数秒内附加到任何新的 GPU 云主机上。
