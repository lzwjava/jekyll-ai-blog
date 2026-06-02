---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 成本高效的GPU数据工作流
translated: true
type: note
---

是的，完全正确。这是一种聪明的工作流程分离。

## 模式

```
CPU Droplet (便宜, ~$0.015/小时)            GPU Droplet (昂贵, ~$2/小时)
─────────────────────────────              ────────────────────────────────
下载原始文本数据
分词 (本来就是 CPU 密集型)
写入 train.bin, val.bin           ──►      挂载卷
分离卷                                       挂载 /mnt/data
销毁 CPU droplet                            训练 GPT
                                            分离卷
                                            销毁 GPU droplet
```

## 为什么这样做非常合理

使用 tiktoken 进行分词是**纯 CPU 工作**——完全不需要 GPU：

```python
# 这在 $0.015/小时的 CPU droplet 上运行良好
enc = tiktoken.get_encoding('gpt2')
ids = enc.encode_ordinary(text)  # 仅限 CPU
```

所以与其浪费 $2/小时的 GPU 时间去做：

- `wget` 下载 80GB 的文本
- `prepare.py` 对 300 亿个 token 进行分词（耗时数小时）
- 等待数据上传

不如在便宜的 CPU droplet 上完成所有这些工作，然后交接卷。

## 具体成本节省

```
数据准备：约 6 小时工作
在 GPU droplet 上：6 小时 × $2.00 = $12.00
在 CPU droplet 上：6 小时 × $0.015 = $0.09

仅数据准备就节省：约 $11.91
```

## 工作流程脚本

```bash
# 阶段 1：CPU droplet — 数据准备
doctl compute droplet create data-prep \
  --image ubuntu-24-04-x64 \
  --size s-4vcpu-8gb \        # 便宜，CPU/RAM 足够
  --region atl1 \
  --ssh-keys <your-key-id>

# 挂载你的卷
doctl compute volume-action attach <volume-id> <cpu-droplet-id> --wait

# SSH 登录，挂载，准备数据
ssh root@<cpu-ip>
mount /dev/sda /mnt/data
cd /mnt/data
pip install tiktoken datasets
python prepare.py   # 下载 + 分词 → 写入 train.bin, val.bin

# 完成 — 分离
umount /mnt/data
doctl compute volume-action detach <volume-id> <cpu-droplet-id> --wait
doctl compute droplet delete <cpu-droplet-id> --force

# 阶段 2：GPU droplet — 训练
doctl compute droplet create amd-gpu \
  --image <your-gpu-snapshot-id> \
  --size <gpu-slug> \
  --region atl1 \
  --ssh-keys <your-key-id>

doctl compute volume-action attach <volume-id> <gpu-droplet-id> --wait

ssh root@<gpu-ip>
mount /dev/sda /mnt/data
ls /mnt/data   # train.bin, val.bin 已经在 ✅
python train.py config/train_gpt3_1b.py
```

## 一个重要限制

**卷和 droplet 必须在同一区域。** 你的卷在 `ATL1` — 所以 CPU 和 GPU droplet 也必须在 `ATL1`。由于这是 AMD Dev Cloud 的区域，你已经有这个条件了。

## 总结

```
你的 volume-atl1-1780280110689 (100GB) 已经创建 ✅
下一步：在 ATL1 启动便宜的 CPU droplet
       挂载卷
       下载 + 分词数据
       分离
       在 ATL1 启动 GPU droplet
       挂载同一个卷
       训练
```

你思考的方向完全正确——CPU 处理数据，GPU 进行计算，卷作为交接机制。
