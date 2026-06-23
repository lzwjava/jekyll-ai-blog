---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何在RunPod上列出RTX 4070
translated: true
type: note
---

**问题：** 如何将我的 RTX 4070 GPU 机器列在 RunPod 上供他人租用？

**答案：**

RunPod 提供 **Secure Cloud**（他们自己的数据中心）和 **Community Cloud**（你的硬件）。你需要的是 Community Cloud 托管计划。

## 要求

- Linux 主机（推荐 Ubuntu 20.04+）
- 静态或稳定的公网 IP
- 已安装 Docker
- NVIDIA 驱动 + `nvidia-container-toolkit`
- 开放端口：`22`、`8888`、`2222`、`443`，以及一个用于 Pod 转发的端口范围

## 步骤

### 1. 安装 RunPod 主机守护进程

```bash
# 安装依赖
curl -fsSL https://get.docker.com | sh
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list \
  | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 验证 Docker 能识别 GPU
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

### 2. 在 RunPod 上注册为托管方

前往：https://www.runpod.io/console/host/machines → **"List a GPU"**

你需要：
- RunPod 账户，并已设置账单/收款（Stripe）
- 你机器的公网 IP

### 3. 运行主机代理

注册后 RunPod 会给你一行命令，类似：

```bash
sudo docker run -d \
  --name runpod-host \
  --restart always \
  --privileged \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e RUNPOD_API_KEY=<API_KEY> \
  runpod/host-agent:latest
```

### 4. 配置定价

在控制面板中设置：
- **GPU 价格**（美元/小时）—— RTX 4070 社区云目前约 $0.15–0.25/小时
- **磁盘价格**
- **最小/最大 Pod 时长**

### 5. 防火墙规则（ufw 示例）

```bash
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8888/tcp
sudo ufw allow 2222/tcp
sudo ufw allow 40000:60000/tcp  # pod 端口转发范围
```

## 针对你设置的注意事项

| 问题 | 详情 |
|---|---|
| **家庭 ISP** | 大多数家庭宽带会封锁入站端口或使用 CGNAT——请用 `curl ifconfig.me` 检查你是否拥有真实公网 IP，并测试入站连通性 |
| **动态 IP** | 使用 DDNS 服务或付费购买静态 IP；RunPod 需要稳定的路由 |
| **运行时间预期** | 租户期望高可用性——RunPod 会记录你的在线率评分 |
| **RTX 4070 12GB** | 在推理工作负载（Mistral 7B、SDXL、Whisper）上表现不错，但不会吸引训练任务 |
| **带宽** | 你承担家庭网络的出站流量——高带宽 Pod 会消耗你的配额 |

## 客观评估

对于**家庭网络上的家用机器**，RunPod 托管存在以下局限：
- CGNAT / 动态 IP 是最大的障碍
- RTX 4070 的收入很低（若 100% 利用率，最多约 $2–5/天，但很少能实现）
- 你位于 `192.168.1.36` 的工作站更适合用于本地开发和自己的推理任务

如果你想要被动的 GPU 收入，**Vast.ai** 通常更容易设置社区托管，并且对家庭主机来说门槛比 RunPod 更低。

```bash
# 检查你是否拥有真实公网 IP（非 CGNAT）
curl ifconfig.me
# 然后检查端口 22 是否可以从外部访问：
# 使用 https://portchecker.co 或请他人执行 nc -zv <你的IP> 22
```

**参考资料：**

- [RunPod 社区云托管文档](https://docs.runpod.io/hosting/overview)
- [Vast.ai 主机设置](https://vast.ai/docs/hosting/setup)