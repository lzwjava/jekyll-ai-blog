---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD开发云卷管理步骤
translated: true
type: note
---

## 综合总结：AMD 开发云（DigitalOcean）上的卷管理

### 1. 调查“200 is not ok”卷大小调整错误

**检查 doctl CLI 代码** 位于 `/Users/lzwjava/projects/doctl/commands/volumes.go`：
- `--size` 参数要求单位后缀（例如 `200GiB`），裸写 `200` = 200 字节 → 0 GiB
- 但 UI 错误不同 —— HTML 显示 `min="101" max="16384"`，当前卷大小为 100 GiB

**通过 API 测试调整大小** —— 每次大小均失败：
```bash
doctl compute volume-action resize 52743aec-... --size 101 --region atl1  # 422
doctl compute volume-action resize 52743aec-... --size 200 --region atl1  # 422
doctl compute volume-action resize 52743aec-... --size 500 --region atl1  # 422
```

也通过 Python (curl) 测试，先分离卷，不同区域 —— 均为 `422 "invalid size specified"`。

**结论：** AMD 开发云合作伙伴（GPU）卷不支持调整大小 API。

---

### 2. 将数据迁移到卷 (129.212.178.103)

**检查磁盘使用情况：**
```bash
ssh root@129.212.178.103 'df -h && du -sh /root/ /var/ /opt/'
```
结果：`/root/` 37G（llama 模型），`/var/` 60G（containerd），`/opt/` 22G（ROCm）

**挂载并迁移 llama 模型 (37G)：**
```bash
ssh root@129.212.178.103 'mount /dev/sda /mnt/volume_atl1_1780280110689'
ssh root@129.212.178.103 'rsync -a --progress /root/llama.cpp/models/ /mnt/volume_atl1_1780280110689/llama-models/'
ssh root@129.212.178.103 'rm -rf /root/llama.cpp/models && ln -s /mnt/volume_atl1_1780280110689/llama-models /root/llama.cpp/models'
```

**调查 containerd (59G)：**
```bash
ssh root@129.212.178.103 'docker images -a && docker ps -a && docker system df'
```
发现：`rocm:latest`（36GB），`ubuntu:24.04`（119MB），已退出的 `rocm` 容器（Jupyter Lab），36GB 构建缓存。

**清理 Docker 工件：**
```bash
ssh root@129.212.178.103 'docker rm rocm'
ssh root@129.212.178.103 'docker rmi rocm:latest ubuntu:24.04'
ssh root@129.212.178.103 'docker builder prune --all -f'
ssh root@129.212.178.103 'docker system prune --all -f'
```

**使挂载持久化：**
```bash
ssh root@129.212.178.103 'echo "/dev/sda /mnt/volume_atl1_1780280110689 ext4 defaults,nofail 0 2" >> /etc/fstab'
```

**结果：** 根磁盘释放了 95G（从 124G 使用量降至 29G）。

---

### 3. 分离卷并销毁 GPU Droplet

**卸载卷：**
```bash
ssh root@129.212.178.103 'umount /mnt/volume_atl1_1780280110689'
```

**分离卷：**
```bash
doctl compute volume-action detach 52743aec-5d63-11f1-a928-0a58ac126378 574422820 --wait
```

**启动 droplet（创建快照需要）：**
```bash
doctl compute droplet-action power-on 574422820 --wait
```

**创建快照：**
```bash
doctl compute droplet-action snapshot 574422820 --snapshot-name "gpu-mi300x-snapshot-20260601" --wait
```

**销毁 GPU droplet：**
```bash
doctl compute droplet delete 574422820 --force
```

**验证：**
```bash
doctl compute snapshot list --resource droplet
doctl compute volume list
```

---

### 最终状态

| 资源          | ID           | 状态          | 月费用     |
|---------------|--------------|---------------|------------|
| GPU Droplet   | 574422820    | DESTROYED     | $0         |
| 快照          | 230979911    | gpu-mi300x-snapshot-20260601 (30.6 GiB) | ~$1.53     |
| 卷            | 52743aec-... | DETACHED (100 GiB, 37G llama-models) | ~$10       |
| **总计**      |              |               | **~$11.50/月** |

之前：~$2+/小时 = 如果一直运行则 ~$1,460/月。

---

### 4. 额外快照（可清理）

```bash
doctl compute snapshot list --resource droplet
```

| 快照          | 大小         | 月费用 | 可安全删除？ |
|---------------|--------------|--------|--------------|
| `7.2-gpu-mi300x1-...-1779256307024` | 132.77 GiB | $6.64 | 是（原始 AMD 镜像，可重新下载） |
| `snap-snapshots-gpu-mi300x1-...-0530-2331` | 6.58 GiB | $0.33 | 是 |
| `gpu-mi300x-snapshot-20260601` | 30.62 GiB | $1.53 | 否（你的快照） |

```bash
# 删除旧快照可节省约 $7/月：
doctl compute snapshot delete 229365612 --force
doctl compute snapshot delete 230740400 --force
```

---

### 5. 后续步骤（准备就绪时）

```bash
# 创建廉价 CPU droplet 用于数据准备
doctl compute droplet create data-prep \
  --size s-2vcpu-4gb \
  --region atl1 \
  --image ubuntu-24-04-x64 \
  --ssh-keys <fingerprint>

# 附加卷
doctl compute volume-action attach 52743aec-... <new-droplet-id>

# SSH 登录，挂载，下载数据集，分词
ssh root@<new-ip>
mount /dev/sda /mnt/volume_atl1_1780280110689

# 数据就绪后：分离卷，销毁 CPU droplet
doctl compute volume-action detach 52743aec-... <new-droplet-id>
doctl compute droplet delete <new-id> --force

# 从快照重新创建 GPU droplet
doctl compute droplet create gpu-train \
  --size gpu-mi300x1-192gb \
  --region atl1 \
  --image 230979911 \
  --ssh-keys <fingerprint>

# 附加卷，开始训练
doctl compute volume-action attach 52743aec-... <gpu-droplet-id>
```
