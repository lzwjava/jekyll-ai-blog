---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 超越Ubuntu的AI工作负载
translated: true
type: note
---

除了Ubuntu，人们还用哪些系统来运行模型、PyTorch和一般的LLM工作负载？

回答：

Ubuntu是AI开发的**主导选择**，但并非唯一。整个生态系统基本以Linux为主，因为CUDA、驱动、分布式训练和集群工具都是围绕Linux构建的。

常见选择：

| 操作系统                              | 用途                             | 备注                                                      |
| ---------------------------------- | -------------------------------- | -------------------------------------------------------- |
| **Ubuntu Linux**                   | ⭐ 最常用于AI研究/开发            | 最佳的CUDA/PyTorch兼容性，教程最简单                      |
| **Debian**                         | 服务器、自定义基础设施            | 更稳定，软件包更新较慢                                    |
| **Rocky Linux / AlmaLinux / RHEL** | 企业级AI集群                      | 常见于高校和拥有HPC的公司                                 |
| **CentOS（较旧版本）**             | 遗留HPC集群                       | 正被Rocky/Alma取代                                       |
| **SUSE Linux Enterprise**          | 企业/HPC                          | 用于一些超级计算环境                                      |
| **Arch Linux**                     | 个人开发者                        | 软件包最新，维护成本更高                                  |
| **Fedora**                         | 开发者                            | 更新的Linux技术                                           |
| **Windows + WSL2**                 | 本地AI开发者                      | 现在非常流行；在Windows内部运行Ubuntu环境                 |
| **macOS**                          | 开发/测试                         | 适合Apple Silicon，不适合CUDA训练                         |

---

## 1. Ubuntu（默认选择）

大多数教程假设：

```
Ubuntu 22.04 / 24.04
CUDA
cuDNN
PyTorch
NVIDIA驱动
```

示例：

```bash
sudo apt install nvidia-driver-580
pip install torch torchvision
python train.py
```

大多数GitHub上的AI项目都是在Ubuntu上测试的。

---

## 2. Windows + WSL2

很多个人开发者使用：

```
Windows
 └── WSL2
      └── Ubuntu
           ├── CUDA
           ├── PyTorch
           └── LLM工具
```

你可以获得：

* Windows桌面/游戏/工具
* Linux AI环境

示例：

```powershell
wsl --install
```

然后在Ubuntu内部：

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

对于单张RTX 4070/4090工作站，这种方式非常常见。

---

## 3. Debian

Ubuntu本身基于Debian。

很多服务器使用Debian：

```
Debian 12
 ├── NVIDIA驱动
 ├── Docker
 ├── Kubernetes
 └── PyTorch容器
```

优点：

* 稳定
* 精简
* 适合长期运行的服务器

缺点：

* 一些AI教程假设使用Ubuntu命令。

---

## 4. 企业级Linux（Rocky / RHEL）

大型AI集群通常使用：

```
Rocky Linux
      |
      +-- Slurm
      +-- CUDA
      +-- NCCL
      +-- PyTorch
```

示例环境：

* 大学
* 国家实验室
* 云GPU集群

他们关注：

* 5年支持
* 安全补丁
* 可预测的更新

---

## 5. Docker（实际上比操作系统更重要）

在现代AI中，人们经常这样想：

```
主机操作系统
   |
   Docker
   |
   CUDA容器
   |
   PyTorch
   |
   模型
```

示例：

```bash
docker run \
 --gpus all \
 -it \
 pytorch/pytorch:2.7.0-cuda12.8-cudnn9-runtime
```

这避免了“依赖地狱”。

研究人员可能会运行：

```
Ubuntu 24.04主机

容器：
    Ubuntu 22.04
    CUDA 12.6
    PyTorch 2.7
    Transformers
    FlashAttention
```

---

## 6. 云AI环境

很多人从不自己管理操作系统：

### AWS

```
EC2 GPU实例
Amazon Linux / Ubuntu
Docker
PyTorch
```

### Google Cloud

```
GKE
Vertex AI
Deep Learning VM
```

### Azure

```
Azure ML
GPU VM
```

---

## 7. 对于Apple Silicon Mac

人们使用：

```
macOS
 |
PyTorch MPS后端
 |
Metal GPU
```

示例：

```python
device = "mps"

model.to(device)
```

适合：

* 推理
* 小模型
* 开发

不适合：

* 大型LLM训练
* CUDA生态

---

对于你的情况（RTX 4070 + LLM实验），典型的技术栈是：

```
Ubuntu 24.04
    |
NVIDIA驱动
    |
CUDA 12.x
    |
PyTorch
    |
Transformers / vLLM / SGLang / DeepSpeed
    |
LLM实验
```

或者：

```
Windows
 |
WSL2 Ubuntu
 |
相同的AI技术栈
```

如今大多数LLM工程师实际上都在使用**Ubuntu + Docker + CUDA**，无论物理机器是什么。