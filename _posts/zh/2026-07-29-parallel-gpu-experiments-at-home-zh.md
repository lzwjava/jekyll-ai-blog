---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在家并行GPU实验
translated: true
type: note
---

问题：假设我们在本地家庭实验室中有两块 GPU。如何利用它们运行更多并行实验？

回答：

对于家庭 AI 实验室，**不要立刻想着“把两块 GPU 合并成一块大 GPU”**。最高 ROI 通常是**并行实验调度**：

```
GPU0  -> 实验 A
GPU1  -> 实验 B

或

GPU0  -> 训练
GPU1  -> 评估 / 推理 / 数据处理
```

这样几乎能获得 2 倍的生产力，因为机器学习研究通常是大量试验，而不是一次巨型运行。

## 1. 最简单：手动分配 GPU

示例：

机器：

```
CPU
 |
 +-- RTX 4070 12GB (GPU0)
 |
 +-- RTX 3090 24GB (GPU1)
```

运行：

终端 1：

```bash
CUDA_VISIBLE_DEVICES=0 python train.py \
  --lr 3e-4 \
  --batch-size 32 \
  --exp exp_lr3e4
```

终端 2：

```bash
CUDA_VISIBLE_DEVICES=1 python train.py \
  --lr 1e-4 \
  --batch-size 64 \
  --exp exp_lr1e4
```

你正在进行超参数搜索。

不再是：

```
一次实验 = 8 小时
```

而是：

```
实验 A = 8 小时
实验 B = 8 小时

总研究吞吐量 = 2 倍
```

---

## 2. 使用作业调度器（迷你 Kubernetes 风格）

对于认真的家庭实验室，创建一个 GPU 队列。

示例：

```
~/gpu-cluster

jobs/
 ├── train_gpt2_124m.yaml
 ├── finetune_qwen.yaml
 └── eval.yaml
```

一个简单的 Python 调度器：

```python
import subprocess
import time

jobs = [
    {
        "gpu":0,
        "cmd":"python train.py --model gpt2-small"
    },
    {
        "gpu":1,
        "cmd":"python train.py --model qwen"
    }
]


for job in jobs:
    env = {
        "CUDA_VISIBLE_DEVICES":str(job["gpu"])
    }

    subprocess.Popen(
        job["cmd"],
        shell=True,
        env=env
    )
```

基本上就是你自己的小型 Slurm。

---

## 3. 分布式训练（两块 GPU = 一块更大的 GPU）

有时你需要这样：

```
        模型
          |
 ----------------
 |              |
GPU0           GPU1
```

PyTorch DDP：

```bash
torchrun \
 --nproc_per_node=2 \
 train.py
```

内部：

```python
model = MyModel()

model = torch.nn.parallel.DistributedDataParallel(
    model,
    device_ids=[local_rank]
)
```

现在：

```
GPU0:
层 + 梯度

GPU1:
层 + 梯度
```

有效显存：

并非：

```
12GB + 12GB = 24GB
```

因为每个 GPU 通常保存一份参数副本。

例如：

```
模型权重：
10GB

GPU0：
10GB 权重
+
GPU1：
10GB 权重
```

所以 DDP 提供的是速度，而不是内存扩展。

---

## 4. 更适合 LLM 实验：拆分角色

对于你的工作流（GPT-2 训练、Qwen 测试、智能体），我会这样做：

```
GPU0：训练

GPU1：推理 + 评估
```

示例：

```
RTX 4070
 |
 +-- 训练 GPT-2 124M


RTX 3090
 |
 +-- vLLM
 +-- embedding
 +-- 数据集过滤
 +-- eval harness
```

然后你的循环变成：

```
训练
 |
检查点
 |
评估 GPU1
 |
指标
 |
更改超参数
 |
再次训练
```

这更接近研究团队的操作方式。

---

## 5. 使用容器

安装：

* Docker
* NVIDIA Container Toolkit

然后：

容器 A：

```bash
docker run \
 --gpus '"device=0"' \
 pytorch-training
```

容器 B：

```bash
docker run \
 --gpus '"device=1"' \
 vllm-server
```

你获得了隔离：

```
主机
 |
 +-- 训练容器 GPU0
 |
 +-- 推理容器 GPU1
```

---

## 6. 针对多个实验：使用 Ray

Ray 对 AI 实验室非常友好。

安装：

```bash
pip install ray
```

示例：

```python
import ray

ray.init()

@ray.remote(num_gpus=1)
class Trainer:
    def run(self):
        import torch
        print(torch.cuda.current_device())


a = Trainer.remote()
b = Trainer.remote()

ray.get([
    a.run.remote(),
    b.run.remote()
])
```

Ray 自动调度：

```
作业 A -> GPU0
作业 B -> GPU1
```

这是许多 AI 智能体系统的发展方向。

---

## 7. 一个现实的家庭 AI 实验室架构

鉴于你的实验（nanoGPT、Qwen、智能体），我会这样构建：

```
             家庭服务器
                 |
        ---------------------
        |                   |
      GPU0                GPU1
   训练                 服务
        |                   |
   PyTorch             vLLM/Ollama
        |
   检查点
        |
     评估
```

软件：

```
Ubuntu
 |
 +-- Docker
 |
 +-- NVIDIA Container Toolkit
 |
 +-- Ray
 |
 +-- MLflow/W&B
```

然后每个实验变成：

```bash
submit experiment.yaml
```

示例：

```yaml
name: gpt2-small-lr-test

gpu: auto

train:
  model: 124m
  lr:
    - 1e-4
    - 3e-4
    - 1e-3
```

调度器启动：

```
GPU0:
lr=1e-4

GPU1:
lr=3e-4

稍后：
lr=1e-3
```

---

对于**双 GPU 家庭实验室**，我对方法的排序如下：

| 方法                    | 生产力 |
| ----------------------- | -----: |
| 两个独立实验            |  ⭐⭐⭐⭐⭐ |
| 训练 + 推理拆分         |  ⭐⭐⭐⭐⭐ |
| Ray 调度器              |  ⭐⭐⭐⭐ |
| Docker GPU 隔离         |  ⭐⭐⭐⭐ |
| DDP 训练                |  ⭐⭐⭐ |
| 模型并行               |  ⭐⭐ |

最大的提升不是“更多 FLOPS”，而是将你的机器变成**一个小型 AI 研究集群，让实验持续运行而无需你时刻看护**。
