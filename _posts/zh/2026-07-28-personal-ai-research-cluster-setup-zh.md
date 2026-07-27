---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 个人AI研究集群搭建
translated: true
type: note
---

问题：**有没有一款软件能让我用3-5台电脑（其中一些带GPU）作为共享环境，运行AI智能体会话、实验和研究？**

答案：

有。你需要的本质上是一个**个人AI研究集群 / 智能体工作站编排层**。根据你的需求，有几种不同的方案：

1. 跨机器运行智能体/任务
2. 共享GPU算力
3. 管理实验
4. 用一个"大脑"控制多个工作节点

针对你的配置（RTX 4070 + 其他PC + AI智能体），我建议看看以下方案：

---

## 1. Ray —— 可能是最接近的选择

Ray

Ray正是为此而生：

* 多台机器
* CPU/GPU调度
* 分布式Python工作负载
* 强化学习/大语言模型实验
* 智能体

架构：

```
                 Ray Head Node（头节点）
              （你的主电脑）
                      |
        +-------------+-------------+
        |             |             |
     Worker 1      Worker 2      Worker 3
     RTX 4070      RTX GPU       CPU only

        |             |             |
     LLM智能体      训练          评估
```

示例：

机器A：

```bash
ray start --head --port=6379
```

机器B/C/D：

```bash
ray start \
  --address='192.168.1.10:6379'
```

然后Python：

```python
import ray

ray.init()

@ray.remote(num_gpus=1)
class GPUWorker:
    def run(self):
        return "training on GPU"

worker = GPUWorker.remote()

print(ray.get(worker.run.remote()))
```

你可以运行：

* 多个Claude/OpenAI/本地智能体
* 模型评估
* 微调任务
* 数据处理

这正是许多AI实验室内部使用的方案。

---

## 2. Kubernetes + GPU调度

如果你想要一个迷你AI云：

```
                 Kubernetes
                     |
       +-------------+-------------+
       |             |             |
     PC1           PC2           PC3
   RTX4070       RTX GPU        CPU

       |
  vLLM / Ollama / 训练 / 智能体
```

技术栈：

* Kubernetes
* NVIDIA GPU Operator
* KServe
* vLLM
* Argo Workflows

更接近生产环境。

但对于3-5台家用电脑来说，Kubernetes常常显得过于复杂。

---

## 3. Slurm —— HPC风格

Slurm Workload Manager

经典的研究集群调度器。

使用者：

* 大学
* 超级计算中心
* AI实验室

示例：

```
提交作业

sbatch train.sh


调度器决定：

node1 GPU
node2 GPU
node3 CPU
```

非常适合：

* GPT训练
* 分布式实验
* 超参数扫描

不太适合交互式智能体。

---

## 4. Docker Swarm —— 简单的家庭集群

如果你想要轻量级方案：

```
docker swarm init

docker swarm join
```

然后：

```
docker service create \
 --replicas 5 \
 my-agent
```

适合：

* 智能体服务器
* API工作节点
* 数据库

不太适合GPU机器学习。

---

## 5. AI智能体专用：OpenHands / SWE-agent风格工作节点

对于编码智能体：

OpenHands

你可以这样设置：

```
控制器

 |
 +-- 智能体工作节点1
 |       编码任务
 |
 +-- 智能体工作节点2
 |       测试任务
 |
 +-- 智能体工作节点3
        研究任务
```

结合Ray：

```
Ray
 |
 +-- Claude API智能体
 +-- Qwen本地智能体
 +-- 编码沙箱
 +-- 评估工作节点
```

---

## 6. 我为你推荐的整体架构

考虑到你的背景：

* RTX 4070
* 本地训练过GPT-2
* 构建CLI智能体
* 运行实验
* 多台电脑

我会构建：

```
                 Mac / 笔记本电脑
              智能体控制器
                    |
                  Ray
                    |
       +------------+------------+
       |            |            |
    Ubuntu GPU   Windows GPU   CPU盒子

       |            |            |
    vLLM        Ollama       数据任务

       |
   实验数据库
       |
   MLflow/W&B
```

软件：

| 用途               | 工具                     |
| ------------------ | ------------------------ |
| 集群控制           | Ray                      |
| 容器               | Docker                   |
| 本地LLM服务        | vLLM / Ollama            |
| 实验管理           | MLflow                   |
| 数据集处理         | Ray Data                 |
| 智能体编排         | LangGraph / 你自己的CLI  |
| 监控               | Prometheus + Grafana     |

---

## 最小化家庭版

安装Ray：

```bash
pip install ray
```

头节点：

```bash
ray start --head
```

工作节点：

```bash
ray start --address=<HEAD_IP>:6379
```

现在你的5台电脑就变成了一台逻辑机器。

---

对于正在构建智能体的AI工程师，我会选择：

**先Ray → 再加MLflow → 再加Docker → 最后才考虑Kubernetes。**

这样能以20%的复杂度获得80%的AI实验室集群功能。

参考资料：

* Ray文档：https://docs.ray.io/
* Slurm Workload Manager：https://slurm.schedmd.com/
* MLflow：https://mlflow.org/
* Kubernetes：https://kubernetes.io/