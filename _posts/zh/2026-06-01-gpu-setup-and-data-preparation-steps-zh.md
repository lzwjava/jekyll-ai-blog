---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU设置和数据准备步骤
translated: true
type: note
---

完成。状态：

```
GPU Droplet:  关闭    (574422820 — 计费暂停)
Volume:      已分离  (100 GiB, llama-models 已使用 37G)
```

**准备数据时的后续步骤：**

```bash
# 1. 在 atl1 区域创建便宜的 CPU Droplet（约 $4-6/月）
doctl compute droplet create data-prep \
  --size s-2vcpu-4gb \
  --region atl1 \
  --image ubuntu-24-04-x64 \
  --ssh-keys <你的密钥指纹>

# 2. 将 Volume 附加到该 Droplet
doctl compute volume-action attach 52743aec-... <新 Droplet ID>

# 3. 通过 SSH 登录，挂载，下载数据集，进行分词、去重
# 4. 完成后：分离 Volume，销毁 CPU Droplet
# 5. 启动 GPU Droplet，附加 Volume，开始训练
```

需要我现在创建 CPU Droplet，还是你先决定数据集？