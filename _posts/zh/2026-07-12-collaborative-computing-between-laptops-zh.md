---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 笔记本电脑之间的协同计算
translated: true
type: note
---

问题：两台笔记本电脑或计算机如何协同完成任务？

回答：协作可以分为多个层级，从简单的文件共享到分布式计算。

## 1. 远程控制（一台计算机控制另一台）

最简单的模型：

```
笔记本电脑 A  --->  笔记本电脑 B
          SSH / 远程桌面
```

示例：

### SSH（Linux/macOS/Windows）

笔记本电脑 A：

```bash
ssh user@laptop-b-ip
```

然后在 B 上运行命令：

```bash
python train.py
```

计算发生在 B 上。

对于 AI 开发，这很常见：

```
你的笔记本电脑
    |
    | ssh
    v
GPU 工作站
    |
    v
训练 / 推理
```

---

## 2. 共享文件和代码

使用 Git：

```
计算机 A
   |
   | git push
   v
GitHub/GitLab
   |
   | git pull
   v
计算机 B
```

示例：

计算机 A：

```bash
git add .
git commit -m "experiment"
git push
```

计算机 B：

```bash
git pull
```

两台机器拥有相同的代码。

---

## 3. 拆分工作负载（分布式计算）

对于 AI 训练：

```
              PyTorch 分布式

        +----------------+
        |  主节点        |
        |  笔记本电脑 A  |
        +----------------+
              |
       网络 (NCCL/Gloo)
              |
        +----------------+
        |  工作节点      |
        |  笔记本电脑 B  |
        +----------------+
```

示例：

两个 GPU：

```
GPU0 -> 计算机 A
GPU1 -> 计算机 B
```

PyTorch：

```python
torch.distributed.init_process_group(
    backend="nccl"
)
```

运行：

计算机 A：

```bash
torchrun \
 --nproc_per_node=1 \
 --nnodes=2 \
 --node_rank=0 \
 train.py
```

计算机 B：

```bash
torchrun \
 --nproc_per_node=1 \
 --nnodes=2 \
 --node_rank=1 \
 train.py
```

模型训练是同步的。

---

## 4. 将一台用作服务器

对于工程师来说非常常见：

```
笔记本电脑
   |
   | API 请求
   |
   v
带有 GPU 的台式机

RTX 4070 / MI50 / H100
```

示例：

计算机 B：

```bash
vllm serve qwen-model
```

计算机 A：

```python
requests.post(
 "http://computer-b:8000/v1/chat/completions"
)
```

你的笔记本电脑变成“终端”；GPU 机器负责繁重的工作。

---

## 5. Kubernetes / 集群风格

更高级的方式：

```
             Kubernetes 集群

       +----------------+
       | 控制平面       |
       | 计算机 A      |
       +----------------+

          |
    ----------------
    |              |
计算机 B       计算机 C
 GPU 工作节点   GPU 工作节点
```

任务会被自动调度。

---

## 6. 共享文件夹

简单的家庭实验室：

```
计算机 A
      \
       \
      NAS / 共享存储
       /
      /
计算机 B
```

使用：

* NFS
* SMB
* Syncthing
* MinIO

示例：

```bash
mount server:/data /mnt/data
```

两台计算机看到相同的文件。

---

对于你的 AI 工作站情况（RTX 4070 + 可能的 AMD MI50），一个实用的设置是：

```
                 网络

MacBook/笔记本电脑
      |
      | SSH
      |
      v
AI 台式机
      |
      |
 RTX 4070
 MI50
```

笔记本电脑：

* 编写代码
* 监控训练
* 查看日志

台式机：

* GPU 训练
* 模型推理
* 数据集处理

然后稍后：

```
机器 A RTX 4070
        +
机器 B MI50
        +
机器 C 云端 GPU

        |
        v

分布式 PyTorch 训练
```

这基本上就是小型 AI 实验室的成长方式：从 2 台机器开始，然后变成一个微型集群。