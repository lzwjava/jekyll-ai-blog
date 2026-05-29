---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Droplets与自定义镜像详解
translated: true
type: note
---

问题：为什么人们在 DigitalOcean 或 AMD Developer Cloud 中会使用 Droplets 而不是自定义镜像，或者反之？

答案：

在像 [DigitalOcean](https://www.digitalocean.com?utm_source=chatgpt.com) 或 AMD Developer Cloud 这样的平台上，**Droplets** 和 **自定义镜像** 解决的是不同的问题。它们相辅相成，而不是相互替代。

## 什么是 Droplet？

**Droplet** 本质上是一个正在运行的虚拟机（VM）。

可以将其理解为：

* CPU
* 内存
* 磁盘
* 网络
* 操作系统
* 运行的进程/服务

它是你可以通过 SSH 登录并运行工作负载的实际计算实例。

示例：

* LLM 推理服务器
* Kubernetes 节点
* Jupyter notebook
* 数据库服务器
* Web 后端
* GPU 训练机器

在 DigitalOcean 的术语中：

* Droplet = VM 实例
* 快照/自定义镜像 = 可重用的 VM 模板

---

## 什么是自定义镜像？

**自定义镜像** 就像是一个保存的模板或机器冻结状态。

它通常包含：

* 操作系统
* 已安装的软件包
* CUDA/ROCm
* Python 环境
* Docker 镜像
* SSH 配置
* 模型权重
* 你的项目设置

你可以用它来快速创建新的 Droplets。

无需执行：

```bash
apt install ...
pip install ...
git clone ...
docker pull ...
```

而是从准备好的镜像启动，一切都已经就位。

---

# 为什么人们直接使用 Droplets

大多数人只需要：

* 一台机器
* 临时测试
* 实验
* 简单的工作负载

所以他们只是：

1. 创建一个 Droplet
2. 手动配置
3. 使用它
4. 之后销毁

这种方式起初更简单且成本更低。

特别适用于：

* 业余用户
* 学生
* 研究人员
* 短时间的 GPU 会话

在 AMD Developer Cloud 上，许多用户：

* 启动 MI300X
* 测试 ROCm
* 进行基准测试
* 然后终止

不需要可重用的镜像。

---

# 为什么人们使用自定义镜像

当环境配置代价高昂或重复进行时，自定义镜像就变得非常有用。

## 常见原因

### 1. 快速扩展

假设你花费了：

* 2 天配置 ROCm
* 优化 PyTorch
* 推理栈
* 监控
* 数据集

你不希望每次重新做这些工作。

因此，你创建一个自定义镜像，然后立即克隆新的机器。

这在以下场景中很常见：

* AI 初创公司
* MLOps
* 分布式推理
* Kubernetes 工作节点池

---

### 2. 一致性

没有镜像的情况下：

* 一台服务器有 CUDA 12.1
* 另一台有 CUDA 12.4
* 不同的 Python 库
* 不同的 bug

自定义镜像确保：

* 相同的环境
* 可重现的部署
* 更少的“在我机器上能运行”的问题

在企业及银行（如 [HSBC](https://www.hsbc.com?utm_source=chatgpt.com)）中非常重要。

---

### 3. 灾难恢复

如果一台服务器宕机：

* 几分钟内从镜像重新创建

而不是手动重建。

这对以下方面很重要：

* 生产服务
* GPU 集群
* CI/CD 基础设施

---

### 4. 时间成本优化

镜像需要存储费用：

* DigitalOcean 上为 $0.06/GiB/月

但工程师是昂贵的。

例如：

* 100 GB 镜像 ≈ $6/月
* 手动重建环境可能需要 4–8 小时

因此公司愿意支付存储费用。

---

# 为什么人们避免使用自定义镜像

## 1. 存储成本

大型 AI 镜像变得非常大。

典型的机器学习镜像：

* Ubuntu
* ROCm/CUDA
* Docker
* 模型
* Conda 缓存

很容易变成：

* 50 GB
* 100 GB
* 300 GB+

跨多个快照时，这会变得很昂贵。

---

## 2. 镜像会过时

你今天保存的镜像：

* 下个月软件包就过时了
* 缺少安全补丁
* 旧的驱动程序
* 不兼容的库

然后维护镜像就变成了运维工作。

---

## 3. 基础设施即代码变得流行

现代 DevOps 常常偏好：

* Docker
* Terraform
* Ansible
* Kubernetes
* cloud-init

而不是大型 VM 快照。

原因：

* 文本配置可以进行版本控制
* 更容易审计
* 更容易重现

因此，许多高级团队现在使用：

* 小型基础镜像
* 自动化的配置脚本

而不是庞大的自定义镜像。

---

# 在 AI/GPU 工作负载中

自定义镜像尤其有价值，因为环境配置很繁琐。

以 AMD MI300X 为例：

* ROCm 版本兼容性
* PyTorch 构建
* 内核模块
* Flash Attention
* vLLM
* 模型缓存

可能需要数小时。

因此，AI 工程师通常：

1. 配置一台完美的 GPU 虚拟机
2. 制作快照
3. 到处重用

这非常常见。

---

# 简单类比

| 概念          | 现实世界类比                 |
| ------------- | ---------------------------- |
| Droplet       | 正在运行的计算机             |
| 自定义镜像    | 备份磁盘 / 机器模板         |
| 快照          | 保存的还原点                |
| Docker 镜像   | 应用级模板                  |
| Kubernetes    | 大规模编排                  |

---

# 你关于 AMD Developer Cloud 配额的观察与此相关

你注意到 AMD 限制了用户的小型 GPU 配额。

这改变了行为：

* 用户通常将 GPU 实例视为临时性的
* 对持久性基础设施的需求减少
* 更多“临时实验”

因此用户：

* 创建 Droplet
* 测试
* 销毁

而不是构建大型镜像流水线。

但初创公司或高级用户通常仍然会创建可重用镜像，因为 GPU 环境配置既昂贵又脆弱。

参考资料：

* [https://www.digitalocean.com/products/droplets](https://www.digitalocean.com/products/droplets)
* [https://docs.digitalocean.com/products/images/custom-images/](https://docs.digitalocean.com/products/images/custom-images/)
* [https://www.amd.com/en/developer/resources/cloud-access.html](https://www.amd.com/en/developer/resources/cloud-access.html)