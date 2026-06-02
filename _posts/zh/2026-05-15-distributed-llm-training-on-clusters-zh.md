---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 集群上的分布式LLM训练
translated: true
type: note
---

问题：如何使用集群训练大型语言模型（LLM）或 nanoGPT？

回答：

由于巨大的计算和内存需求，在单台机器上训练 GPT 或 nanoGPT 等大型语言模型通常不切实际。使用计算集群可以让您将训练分布到多个 GPU 或节点上。以下是一份全面的操作指南：

---

### 1. **选择您的集群环境**

* **本地集群：** 您的组织可能拥有多台通过 InfiniBand 等高速互连连接的 GPU 服务器。
* **云集群：** AWS、GCP、Azure 或 Lambda Labs 等提供商提供多 GPU 实例以及托管的 Kubernetes 或 HPC 集群。
* **关键考量：** GPU 数量、GPU 内存、网络带宽、存储速度。

---

### 2. **搭建环境**

* **GPU 驱动与 CUDA：** 确保所有节点都安装了兼容的 NVIDIA 驱动以及 CUDA/cuDNN 版本。
* **Python 环境：** 使用 `conda` 或 `virtualenv` 在节点间复制相同的环境。
* **框架：** 通常使用 PyTorch；nanoGPT 基于 PyTorch 构建。

示例设置：

```bash
conda create -n llm python=3.11
conda activate llm
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install numpy transformers datasets wandb
```

---

### 3. **分布式训练策略**

LLM 训练通常需要同时分布计算和内存：

#### **a. 数据并行**

* 每个 GPU 都拥有一份模型副本。
* 每个 GPU 在不同数据子集上计算梯度。
* 每批次后同步梯度。
* 简单，但模型非常大时扩展性不佳。

```python
from torch.nn.parallel import DistributedDataParallel as DDP
```

#### **b. 模型并行**

* 将模型拆分到多个 GPU 上。
* 当单个 GPU 无法容纳模型时非常有用。
* 稍微复杂，需要手动分区。

#### **c. 流水线并行**

* 将模型分成多个阶段，每个阶段放在不同的 GPU 上。
* 前向和反向传播通过流水线方式提高效率。

#### **d. 混合并行**

* 结合数据、模型和流水线并行。
* 用于最先进的 LLM 训练。

**对于 nanoGPT**（小型 GPT 模型）：

* 通常，多 GPU 设置下**数据并行**就足够了。
* 使用 PyTorch DDP 将批次分布到各个 GPU 上。

---

### 4. **集群作业管理**

* 使用 **SLURM**、**Kubernetes** 或 **AWS Batch** 等作业调度程序在节点间运行任务。
* 示例 SLURM 脚本（4 GPU）：

```bash
#!/bin/bash
#SBATCH --job-name=nanogpt
#SBATCH --gres=gpu:4
#SBATCH --nodes=1
#SBATCH --time=12:00:00

module load cuda/12.0
source activate llm

srun python train.py --config config.yaml
```

---

### 5. **PyTorch 中的分布式训练（nanoGPT 示例）**

nanoGPT 提供了一个 `train.py` 脚本，支持通过 DDP 进行多 GPU 训练：

```bash
# 在单个节点上使用 4 个 GPU 启动
python -m torch.distributed.run --nproc_per_node=4 train.py config/train_shakespeare_char.py
```

关键点：

* `--nproc_per_node`：每个节点的 GPU 数量。
* `train.py` 内部使用 `DistributedDataParallel`。
* 对于多节点设置，需要指定 `--nnodes`、`--node_rank` 以及 `--master_addr` 和 `--master_port`。

---

### 6. **优化技巧**

* **混合精度训练：** 使用 `torch.cuda.amp` 或 nanoGPT 中的 `--dtype float16` 来减少内存使用。
* **梯度累积：** 有助于模拟更大的批次大小。
* **检查点：** 定期保存模型权重，适用于长时间运行的作业。
* **监控：** 使用 `wandb` 或 `TensorBoard` 监控训练指标。

---

### 7. **集群存储与数据处理**

* 将数据集存储在共享文件系统中（例如 NFS、S3、GCS）。
* 使用 `torch.utils.data.DistributedSampler` 将数据分配到各个节点。
* 确保网络带宽能够处理数据传输。

---

### 8. **示例：在 2 节点集群上训练 nanoGPT**

```bash
# 节点 0
python -m torch.distributed.run --nproc_per_node=4 --nnodes=2 --node_rank=0 --master_addr="node0_ip" --master_port=12345 train.py config.yaml

# 节点 1
python -m torch.distributed.run --nproc_per_node=4 --nnodes=2 --node_rank=1 --master_addr="node0_ip" --master_port=12345 train.py config.yaml
```

---

### 9. **参考 / 资源**

* [nanoGPT GitHub](https://github.com/karpathy/nanoGPT)
* [PyTorch 分布式训练](https://pytorch.org/docs/stable/distributed.html)
* [SLURM 文档](https://slurm.schedmd.com/documentation.html)
* [Hugging Face Accelerate](https://huggingface.co/docs/accelerate/index) — 简化多 GPU/多节点训练

---

高效使用集群需要在**内存、计算和网络开销**之间取得平衡。对于 nanoGPT 等小模型，多 GPU DDP 训练通常就足够了。对于更大的 LLM，您需要结合**数据、模型和流水线并行**。

---

如果您愿意，我可以绘制一个**图表，精确展示 nanoGPT 训练如何分布到集群中的多个 GPU 上**——这会让概念更加清晰。需要我这样做吗？
