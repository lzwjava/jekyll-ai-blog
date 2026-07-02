---
audio: false
generated: true
image: false
lang: en
layout: post
title: 5-Machine Homelab Cluster Guide
translated: false
type: note
---

**Question:** How do I turn 4 laptops + 1 RTX 4070 workstation into a home lab for experiments — Kubernetes clusters, distributed Docker builds, compilation farms, and ML workloads?

**Answer:**

Treat the 5 machines as a cluster, not 5 separate computers. The architecture that works:

```
lzw@192.168.x.x (RTX 4070, 62GB)  → control plane + GPU node + build server
laptop-1..4                        → worker nodes / chaos-test targets
MacBook Air M2                     → your terminal, never a server
```

## Layer 0: Flat SSH mesh first

Everything else builds on passwordless SSH. Do this once:

```bash
# On the Air (your cockpit)
ssh-keygen -t ed25519 -f ~/.ssh/homelab
for h in node1 node2 node3 node4 gpu; do
  ssh-copy-id -i ~/.ssh/homelab.pub lzw@$h
done
```

`~/.ssh/config`:

```
Host gpu
  HostName <IP_ADDRESS>
  User lzw
Host node*
  User lzw
  IdentityFile ~/.ssh/homelab
```

Strongly recommend **Tailscale** on all 5 machines — you get a stable mesh network (works even when a laptop moves to a café), MagicDNS names (`ssh gpu` from anywhere), and it makes the AMD cloud droplet reachable as if it were on your LAN. Free tier covers 100 devices.

Old laptops: install Ubuntu Server (no desktop — saves ~1GB RAM), set `systemctl set-default multi-user.target`, and in `/etc/systemd/logind.conf` set `HandleLidSwitch=ignore` so closing the lid doesn't suspend the node. Laptops are actually great homelab nodes: built-in UPS (battery), low power draw.

## Layer 1: Kubernetes — use k3s, not kubeadm

For learning and experiments, k3s is the right call: single binary, ~512MB RAM footprint, real CNCF-conformant Kubernetes.

```bash
# On the 4070 box (control plane)
curl -sfL https://get.k3s.io | sh -
sudo cat /var/lib/rancher/k3s/server/node-token   # copy this

# On each laptop
curl -sfL https://get.k3s.io | K3S_URL=https://gpu:6443 \
  K3S_TOKEN=<SECRET> sh -

# From the Air
scp gpu:/etc/rancher/k3s/k3s.yaml ~/.kube/config
sed -i '' 's/127.0.0.1/gpu/' ~/.kube/config
kubectl get nodes   # 5-node cluster
```

Then make the GPU schedulable in-cluster with the NVIDIA device plugin:

```bash
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/main/deployments/static/nvidia-device-plugin.yml
```

Now pods can request `nvidia.com/gpu: 1` and land on the 4070 node. This is exactly how production ML platforms schedule GPU jobs — you're learning the real thing at home scale.

**Experiments that actually teach you something:**

- Kill a laptop mid-deployment (`sudo poweroff`) and watch pod rescheduling, taints, eviction timeouts. This is chaos engineering you can't do on a single machine or minikube.
- Deploy vLLM as a k8s Deployment on the GPU node, put a Service + Ingress in front, and hit it from the laptops with a load generator. You now understand LLM serving infra end to end.
- Run a 3-replica etcd/Postgres/Redis across laptops, then partition the network (`iptables -A INPUT -s node2 -j DROP`) and observe split-brain/quorum behavior. Distributed systems theory made visceral.
- Try k3s HA mode: 3 laptops as embedded-etcd servers instead of one control plane.

## Layer 2: Distributed Docker builds

Docker Buildx can fan builds out across machines over SSH:

```bash
docker buildx create --name farm \
  --node gpu   ssh://lzw@gpu \
  --node node1 ssh://lzw@node1 --append \
  --node node2 ssh://lzw@node2 --append

# Multi-arch builds distributed across the farm
docker buildx build --builder farm \
  --platform linux/amd64,linux/arm64 -t myimage .
```

Also run a local registry on the 4070 box so images don't round-trip to Docker Hub:

```bash
docker run -d -p 5000:5000 --restart=always --name registry registry:2
# push: docker tag myimage gpu:5000/myimage && docker push gpu:5000/myimage
```

Point k3s at it via `/etc/rancher/k3s/registries.yaml` on each node. Your build→push→deploy loop drops from minutes to seconds.

## Layer 3: Compile farm

For big C/C++ builds (Linux kernel, LLVM — relevant to your kernel-internals notes):

```bash
# distcc on all Linux nodes
sudo apt install distcc
# on workers: distccd --daemon --allow 192.168.x.0/24

# On the machine driving the build
export DISTCC_HOSTS="gpu/16 node1/8 node2/8 node3/8"
make -j40 CC="distcc gcc"
```

A kernel compile that takes 25 min on one laptop finishes in ~6 with the farm. Add `ccache` in front of distcc for near-instant rebuilds. For Rust, distributed compilation via `sccache` with the same topology.

## Layer 4: ML-specific uses

- **Multi-node training practice:** you only have one GPU, but you can still run `torchrun --nnodes=2` with CPU-only gloo backend across laptops to learn DDP/FSDP mechanics — the rendezvous, NCCL vs gloo, gradient sync — before spending $2/hr on MI300X. Debug the orchestration for free, then flip to the real GPU.
- **Ray cluster:** `ray start --head` on the 4070 box, `ray start --address=gpu:6379` on laptops. Now you can do distributed hyperparameter sweeps, data preprocessing across all CPU cores in the house, with the GPU node handling training. Ray is also the substrate under vLLM and many RLHF stacks (OpenRLHF, verl) — knowing it directly serves your GRPO/RLHF goals.
- **Inference serving:** GPU node runs vLLM/llama.cpp; laptops run your agents (ww/iclaw/zz) hammering it. Real load testing for your CLI agent tools.

## Practical ordering

Week 1: SSH mesh + Tailscale + Ubuntu Server on laptops. Week 2: k3s cluster + GPU device plugin + local registry. Week 3: deploy vLLM in-cluster, break things deliberately. After that, Ray and distcc as needed. Total incremental cost: ¥0 — this is pure leverage from hardware you already own, and the k8s/distributed-systems skills transfer directly to any AI infra role or your future startup's serving stack.

One warning: don't over-engineer. The cluster exists to teach you failure modes and give you a build/serve substrate — if you find yourself spending evenings on Helm chart aesthetics instead of experiments, that's the "tax" category from your own playbook.
