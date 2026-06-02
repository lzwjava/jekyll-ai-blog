---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU内存问题与训练选项
translated: true
type: note
---

健康检查完成。概要：

**良好迹象 ✓**

- 配置加载正常，数据加载正常
- 模型参数规模 = **1.2359 亿参数**（确认符合 GPT-2 124M 架构）
- 每轮迭代处理 524,288 个标记（批次大小 8 × 序列长度 1024 × 梯度累积步数 64）

**问题 ✗** — 反向传播时出现内存溢出：

- GPU：RTX 4070，总计 12 GB 显存
- `llama-server`（进程号 2202）当前占用 **5.9 GB**
- 仅剩约 5.7 GB 可用空间 → 不足以支持批次大小 8 × 序列长度 1024 的 fp16 反向计算

原始 11,500 步检查点明显是在 GPU 空闲时训练的。如需重新训练，您有两个选择：

**方案 A — 先释放 GPU（推荐方案，符合原始训练配置）：**

```bash
kill 2202    # 停止 llama-server
nvidia-smi   # 确认 GPU 显存已清空
python3 train.py config/train_fineweb.py
```

**方案 B — 保持 llama-server 运行，采用更小的单步批次规模（通过增加梯度累积步数维持等效批次大小）：**

```bash
python3 train.py config/train_fineweb.py --batch_size=2 --gradient_accumulation_steps=256 --compile=False
```

无论采用哪种方案，请观察 `iter 0: loss ~10.9` 后损失值是否开始下降。随时可按 Ctrl+C 中断训练——您可以通过以下命令恢复已训练的检查点：

```bash
mkdir -p out-fineweb && cp out-fineweb-backup/ckpt.pt out-fineweb/ckpt.pt
```
