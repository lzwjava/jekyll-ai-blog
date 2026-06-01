---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在MI300X上训练GPT-3 6.7B
translated: true
type: note
---

**问题：** 假设 nanoGPT 具备相应能力，如何在 MI300X 上使用 nanoGPT 端到端训练 GPT-3 6.7B？

**答案：**

## 完整分步指南

### 步骤 1：配置存储卷

```bash
# SSH 进入新创建的实例
ssh root@<new-ip>

# 挂载持久化存储卷
lsblk  # 找到你的卷，例如 /dev/sda
mkdir -p /mnt/data
mount /dev/sda /mnt/data

ls /mnt/data
# raw/  tokens/  checkpoints/
```

### 步骤 2：配置环境

```bash
# ROCm 已预装在 AMD GPU 实例上
rocm-smi  # 确认 MI300X 可见

pip install torch torchvision --index-url https://download.pytorch.org/whl/rocm6.1
pip install numpy tiktoken datasets tqdm wandb

# 克隆 nanoGPT
cd /mnt/data
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
```

### 步骤 3：准备数据（The Pile 或 OpenWebText）

```bash
# OpenWebText（约 40GB，GPT-2 风格）—— 规模较小，适合入门
python data/openwebtext/prepare.py

# 输出：
# /mnt/data/tokens/train.bin  （约 17GB）
# /mnt/data/tokens/val.bin    （约 8MB）
```

要达到 GPT-3 规模，你需要更多数据 —— 使用 The Pile：
```python
# data/pile/prepare.py —— 自行编写
from datasets import load_dataset
import numpy as np
import tiktoken

enc = tiktoken.get_encoding('gpt2')

def tokenize(example):
    ids = enc.encode_ordinary(example['text'])
    ids.append(enc.eot_token)
    return {'ids': ids, 'len': len(ids)}

dataset = load_dataset('EleutherAI/pile', split='train', streaming=True)

# 写入二进制文件
arr = np.memmap('/mnt/data/tokens/train.bin', dtype=np.uint16, mode='w+', shape=(400_000_000_000,))
# 流式处理并填充...
```

### 步骤 4：修改 nanoGPT 以支持 6.7B 模型

两个关键修改：

**修改 1 —— 梯度检查点：**
```python
# model.py —— 在 GPT.forward() 中
from torch.utils.checkpoint import checkpoint

# 替换这一部分：
for block in self.transformer.h:
    x = block(x)

# 改为：
for block in self.transformer.h:
    x = checkpoint(block, x, use_reentrant=False)
```

**修改 2 —— 修复数据路径配置：**
```python
# 在 train.py 中，更新 data_dir 默认值
data_dir = os.path.join('/mnt/data/tokens', dataset)
```

### 步骤 5：编写 6.7B 配置文件

```python
# config/train_gpt3_6b.py

# 模型
n_layer = 32
n_head  = 32
n_embd  = 4096
block_size = 2048
bias = False
dropout = 0.0

# 数据
dataset = 'pile'  # 指向 /mnt/data/tokens/pile
data_dir = '/mnt/data/tokens'

# 训练
batch_size = 4
gradient_accumulation_steps = 160  # 有效批量大小 = 640
max_iters = 600_000
warmup_iters = 2_000
lr_decay_iters = 600_000

# 优化器
learning_rate = 1e-4
min_lr = 1e-5
beta1 = 0.9
beta2 = 0.95
weight_decay = 0.1
grad_clip = 1.0

# 精度 —— 对 MI300X 至关重要
dtype = 'bfloat16'

# 检查点
out_dir = '/mnt/data/checkpoints'
eval_interval = 1000
save_checkpoint_interval = 1000  # nanoGPT 使用 eval_interval 实现此功能
keep_last_n = 3  # 需要手动添加此修改，见下方

# 日志
wandb_log = True
wandb_project = 'gpt3-6b'
wandb_run_name = 'mi300x-run1'

# 系统
device = 'cuda'  # ROCm 以 cuda 形式暴露
compile = False  # torch.compile 在 ROCm 上的支持不稳定，可先尝试 True
```

### 步骤 6：添加检查点轮换（保留最近 N 个）

nanoGPT 默认保存一个 `ckpt.pt` 并覆盖。修改为保留最近 3 个：

```python
# 在 train.py 中，找到保存检查点的位置
# 替换：
torch.save(checkpoint, os.path.join(out_dir, 'ckpt.pt'))

# 改为：
ckpt_path = os.path.join(out_dir, f'ckpt_{iter_num}.pt')
torch.save(checkpoint, ckpt_path)

# 轮换：删除超出最近 3 个的旧检查点
import glob
ckpts = sorted(glob.glob(os.path.join(out_dir, 'ckpt_*.pt')))
for old in ckpts[:-3]:
    os.remove(old)
    print(f"deleted old checkpoint: {old}")
```

### 步骤 7：启动训练

```bash
cd /mnt/data/nanoGPT

# 单 GPU（MI300X 拥有 192GB，足以运行 6.7B 模型 + 梯度检查点）
python train.py config/train_gpt3_6b.py

# 为安全起见，在 tmux 中运行
tmux new -s train
python train.py config/train_gpt3_6b.py 2>&1 | tee /mnt/data/logs/train.log
# Ctrl+B D 分离会话
```

### 步骤 8：监控

```bash
# GPU 利用率
watch -n 1 rocm-smi

# 训练日志
tail -f /mnt/data/logs/train.log

# wandb —— 在浏览器中打开
# https://wandb.ai/your-project/gpt3-6b
```

预期输出：
```
iter 0:    loss 11.07, time 4200ms, mfu 0.12%
iter 100:  loss 7.43,  time 3800ms, mfu 38.2%
iter 1000: loss 4.21,  time 3750ms, mfu 39.1%
```

### 步骤 9：会话结束 —— 安全关机

```bash
# 在 tmux 中，检查点会按 eval_interval 保存
# 按 Ctrl+C 安全退出，nanoGPT 退出时会保存吗？不会 —— 因此请等待一次检查点保存后再按 Ctrl+C

# 卸载存储卷
umount /mnt/data

# 从你的 MacBook 通过 doctl 分离卷
doctl compute volume-action detach <volume-id> <droplet-id>

# 删除实例
doctl compute droplet delete <droplet-id> --force
```

### 步骤 10：下一次会话恢复

```bash
# 新建实例，挂载卷
mount /dev/sda /mnt/data

# nanoGPT 会自动从最新的检查点恢复
python train.py config/train_gpt3_6b.py
# 它会在 out_dir 中找到 ckpt_*.pt 并自动恢复
```

## 预期训练时间（粗略估计）

GPT-3 6.7B，300B tokens（Pile 的子集）：
```
MI300X 理论性能：约 200 TFLOPS bf16
实际 MFU 约 40%：约 80 TFLOPS 有效性能

6.7B 参数 × 6 FLOPs/token × 300B tokens
= 总计算量 1.2 × 10^22 FLOPs

1.2e22 / 80e12 = 150,000 秒
= 约 42 天连续运行
```

按 $2/小时 计费：
```
42 天 × 24 小时 × $2 = 约 $2,016
```

这是真金白银 —— 因此 **先在一个子集上训练**（10B tokens，约 3 天，约 $144）以验证 loss 正常下降，然后再投入完整训练。

## 最终检查清单

```
✅ 挂载 /mnt/data 存储卷
✅ pip 安装依赖（torch ROCm, tiktoken）
✅ 准备数据 → /mnt/data/tokens/
✅ 修改 model.py 添加梯度检查点
✅ 修改 train.py 添加检查点轮换
✅ 编写 config/train_gpt3_6b.py
✅ tmux + 启动训练
✅ 监控 rocm-smi + wandb
✅ 安全关机 → 分离存储卷 → 删除实例
✅ 下一次会话通过挂载卷恢复
```