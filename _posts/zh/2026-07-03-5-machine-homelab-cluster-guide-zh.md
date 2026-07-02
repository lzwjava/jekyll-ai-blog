---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 5机器家庭实验室集群指南
translated: true
type: note
---

**问题：** 如何将 4 台笔记本电脑 + 1 台 RTX 4070 工作站改造成家庭实验室，用于 Kubernetes 集群、分布式 Docker 构建、编译农场和机器学习工作负载的实验？

**回答：**

把这 5 台机器当作一个集群来对待，而不是 5 台独立的电脑。有效的架构如下：

```
lzw@192.168.x.x (RTX 4070, 62GB)  → 控制平面 + GPU 节点 + 构建服务器
laptop-1..4                        → 工作节点 / 混沌测试目标
MacBook Air M2                     → 你的终端，永远不作为服务器
```

## 第 0 层：先搭扁平 SSH 网络

所有其他功能都建立在免密码 SSH 之上。只需做一次：

```bash
# 在 Air 上（你的控制台）
ssh-keygen -t ed25519 -f ~/.ssh/homelab
for h in node1 node2 node3 node4 gpu; do
  ssh-copy-id -i ~/.ssh/homelab.pub lzw@$h
done
```

`~/.ssh/config` 文件：

```
Host gpu
  HostName <IP_ADDRESS>
  User lzw
Host node*
  User lzw
  IdentityFile ~/.ssh/homelab
```

强烈建议在所有 5 台机器上安装 **Tailscale**——你将获得一个稳定的网状网络（即使某台笔记本被带到咖啡馆也能工作），MagicDNS 名称（从任何地方都可以 `ssh gpu`），并且还能让 AMD 云主机就像在本地局域网中一样可达。免费套餐支持 100 台设备。

老旧笔记本：安装 Ubuntu Server（不带桌面——节省约 1GB 内存），设置 `systemctl set-default multi-user.target`，并在 `/etc/systemd/logind.conf` 中设置 `HandleLidSwitch=ignore`，这样合上盖子也不会让节点休眠。笔记本其实是很棒的家庭实验室节点：自带 UPS（电池）、功耗低。

## 第 1 层：Kubernetes —— 使用 k3s，而不是 kubeadm

对于学习和实验，k3s 是正确选择：单个二进制文件，约 512MB 内存占用，真正的 CNCF 认证 Kubernetes。

```bash
# 在 4070 主机上（控制平面）
curl -sfL https://get.k3s.io | sh -
sudo cat /var/lib/rancher/k3s/server/node-token   # 复制此令牌

# 在每台笔记本上
curl -sfL https://get.k3s.io | K3S_URL=https://gpu:6443 \
  K3S_TOKEN=<SECRET> sh -

# 在 Air 上
scp gpu:/etc/rancher/k3s/k3s.yaml ~/.kube/config
sed -i '' 's/127.0.0.1/gpu/' ~/.kube/config
kubectl get nodes   # 5 节点集群
```

然后通过 NVIDIA 设备插件使 GPU 在集群中可调度：

```bash
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/main/deployments/static/nvidia-device-plugin.yml
```

现在 Pod 可以请求 `nvidia.com/gpu: 1` 并落在 4070 节点上。这正是生产级 ML 平台调度 GPU 任务的方式——你在家庭规模下学习真实的东西。

**真正能让你学到东西的实验：**

- 在部署过程中拔掉一台笔记本的电源（`sudo poweroff`），然后观察 Pod 重新调度、污点、驱逐超时。这是你在单机或 minikube 上无法进行的混沌工程。
- 在 GPU 节点上将 vLLM 部署为 k8s Deployment，在前面放一个 Service + Ingress，然后从笔记本上用负载生成器访问它。这样你就端到端地理解了 LLM 服务基础设施。
- 在笔记本上运行一个 3 副本的 etcd/Postgres/Redis，然后通过网络分区（`iptables -A INPUT -s node2 -j DROP`）观察脑裂/法定人数行为。分布式系统理论变得触手可及。
- 尝试 k3s 高可用模式：用 3 台笔记本作为嵌入式 etcd 服务器，而不是单个控制平面。

## 第 2 层：分布式 Docker 构建

Docker Buildx 可以通过 SSH 将构建任务分发到多台机器上：

```bash
docker buildx create --name farm \
  --node gpu   ssh://lzw@gpu \
  --node node1 ssh://lzw@node1 --append \
  --node node2 ssh://lzw@node2 --append

# 跨构建农场进行多架构构建
docker buildx build --builder farm \
  --platform linux/amd64,linux/arm64 -t myimage .
```

同时在 4070 主机上运行一个本地镜像仓库，避免镜像往返 Docker Hub：

```bash
docker run -d -p 5000:5000 --restart=always --name registry registry:2
# 推送：docker tag myimage gpu:5000/myimage && docker push gpu:5000/myimage
```

通过每个节点上的 `/etc/rancher/k3s/registries.yaml` 让 k3s 指向该仓库。你的构建→推送→部署循环将从几分钟缩短到几秒。

## 第 3 层：编译农场

对于大型 C/C++ 构建（Linux 内核、LLVM——与你的内核内部笔记相关）：

```bash
# 在所有 Linux 节点上安装 distcc
sudo apt install distcc
# 在工作节点上：distccd --daemon --allow 192.168.x.0/24

# 在负责构建的机器上
export DISTCC_HOSTS="gpu/16 node1/8 node2/8 node3/8"
make -j40 CC="distcc gcc"
```

原本在一台笔记本上需要 25 分钟的内核编译，使用编译农场后大约 6 分钟就能完成。在 distcc 前面加上 `ccache` 可以实现近乎即时的重编译。对于 Rust，可以使用相同拓扑的 `sccache` 进行分布式编译。

## 第 4 层：ML 特定用途

- **多节点训练实践：** 你只有一块 GPU，但仍然可以运行 `torchrun --nnodes=2`，配合仅 CPU 的 gloo 后端，在笔记本上学习 DDP/FSDP 的机制—— rendezvous、NCCL 与 gloo 的区别、梯度同步——然后再花 2 美元/小时使用 MI300X。先免费调试编排流程，然后切换到真正的 GPU。
- **Ray 集群：** 在 4070 主机上运行 `ray start --head`，在笔记本上运行 `ray start --address=gpu:6379`。现在你可以进行分布式超参数搜索、跨家中所有 CPU 核心进行数据预处理，而 GPU 节点负责训练。Ray 也是 vLLM 和许多 RLHF 堆栈（OpenRLHF, verl）的基础——了解它直接服务于你的 GRPO/RLHF 目标。
- **推理服务：** GPU 节点运行 vLLM/llama.cpp；笔记本运行你的代理（ww/iclaw/zz）向其发起大量请求。这是对你 CLI 代理工具的真实负载测试。

## 实际操作顺序

第 1 周：SSH 网状网络 + Tailscale + 笔记本上安装 Ubuntu Server。第 2 周：k3s 集群 + GPU 设备插件 + 本地镜像仓库。第 3 周：在集群中部署 vLLM，故意制造故障。之后根据需要添加 Ray 和 distcc。总新增成本：¥0 —— 这只是对你已有硬件的纯利用，而 k8s/分布式系统技能可以直接迁移到任何 AI 基础设施岗位或你未来创业的服务栈中。

一条警告：不要过度工程化。这个集群的存在是为了教你认识故障模式，并为你提供一个构建/服务的基础平台——如果你发现自己把晚上的时间花在美化 Helm Chart 而不是做实验上，那就属于你自己规则中的“税”类目了。
