---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双GPU AI集群
translated: true
type: note
---

问题：两个独立的人工智能工作站（RTX 4070 + RTX 3060/3090）如何协同使用？

回答：

将**两台独立的机器**视为一个小的**AI集群**，而不是一台计算机。

示例：

```
                LAN (1GbE/10GbE)
                     |
        ----------------------------
        |                          |
 工作站 A                    工作站 B
 RTX 4070 12GB              RTX 3090 24GB
 Ubuntu                     Ubuntu
 PyTorch                    vLLM
 训练                       推理
```

最佳用途取决于 GPU 的组合。

---

## 情况 1：RTX 4070 + RTX 3090（最佳组合）

这实际上是一个非常不错的家庭实验室。

### 机器 A：RTX 4070

角色：

* 快速实验
* 微调
* 代码开发
* 较小模型

示例：

```
GPT-2 124M
GPT-2 355M
Qwen3-8B LoRA
嵌入模型
智能体实验
```

### 机器 B：RTX 3090 24GB

角色：

* 大规模推理
* 更大规模的微调
* 评估服务器

示例：

```
Qwen3-8B
Llama 8B
DeepSeek 蒸馏模型
FLUX 图像模型
```

因为 3090 拥有：

```
24GB VRAM
对比
4070 12GB VRAM
```

3090 解锁了不同类别的模型。

---

## 推荐工作流程

像 AI 研究团队一样思考：

```
                 Git 仓库
                    |
        ------------------------
        |                      |
 RTX 4070 机器          RTX 3090 机器
        |                      |
 实验                   评估
 训练                   服务
        |                      |
 检查点  ----------->  测试
```

示例：

你在训练：

```
GPU0:
python train.py \
 --model gpt2-124m \
 --lr 3e-4
```

它生成：

```
checkpoint_10000.pt
```

3090 自动评估：

```
python eval.py \
 checkpoint_10000.pt
```

---

## 使用 SSH + 共享存储

最简单的集群设置：

机器名称：

```
ai4070
ai3090
```

SSH：

```bash
ssh ai3090
```

共享目录：

选项 1：

NFS：

```
ai4070:/data

挂载到：

ai3090:/data
```

选项 2：

Git + rsync：

```bash
rsync -av checkpoints/ ai3090:/data/checkpoints/
```

---

## 远程运行实验

示例：

在 4070 上：

```bash
ssh ai3090 \
"CUDA_VISIBLE_DEVICES=0 \
python eval.py \
--checkpoint /data/model.pt"
```

你的笔记本电脑变成了控制器。

---

## 添加轻量级调度器

在两台机器上安装 Ray：

```
pip install ray
```

主节点：

3090：

```bash
ray start --head
```

输出：

```
ray://192.168.1.100:10001
```

工作节点：

4070：

```bash
ray start \
--address='192.168.1.100:6379'
```

现在：

```
Ray 集群

GPU 资源：

node1:
 RTX3090: 1 GPU

node2:
 RTX4070: 1 GPU
```

你的实验请求：

```python
@ray.remote(num_gpus=1)
class Experiment:
    pass
```

Ray 决定在哪里运行。

---

## 我不会做的事情

避免：

```
RTX4070 + RTX3090
       |
       |
    分布式训练
```

除非你有理由。

为什么？

不同的 GPU：

```
4070:
Ada Lovelace
12GB

3090:
Ampere
24GB
```

问题：

* 不同的 CUDA 性能
* 不同的 VRAM
* PCIe 网络瓶颈
* 同步开销

对于 LLM 训练，通常两个独立的任务更好。

---

## 针对你实验的实用设置

鉴于你之前对 GPT-2/nanoGPT 的工作：

### RTX 4070 盒子

```
角色：
研究工作站

运行：
- nanoGPT 训练
- 数据预处理
- 小型 LoRA
- 编码智能体
```

### RTX 3090 盒子

```
角色：
AI 服务器

运行：
- vLLM
- Ollama
- Qwen 模型
- 嵌入服务
- 评估
```

然后你得到：

```
          Claude/Gemini
               |
               |
          AI 智能体 CLI
               |
       -----------------
       |               |
   RTX4070          RTX3090
   创建              执行
   训练              服务
```

这接近于一个微型内部 AI 实验室。

---

对于家庭使用，我会选择：

1. **RTX 3090 24GB 作为主要 AI 服务器**
2. **RTX 4070 作为日常开发/训练机器**
3. **如果可能，连接 10GbE**（尤其是用于数据集/检查点）
4. 只有在 SSH + 共享存储变得麻烦时再添加 Ray

这样比试图将它们变成一块巨型 GPU 能获得更实际的吞吐量。