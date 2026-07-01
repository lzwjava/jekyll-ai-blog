---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod网络拓扑探针
translated: true
type: note
---

**问题：** 能否通过跨多个实例扫描 RunPod Pod 来揭示其网络拓扑结构和贡献者分布？

**回答：**

是的，概念上可行。以下是具体方法及你能实际获得的信息：

## 你能发现什么

启动 N 个 Pod 并记录底层代理/IP 元数据，可获得：

- **数据中心分布** — ASN 查询可揭示哪些托管公司在贡献（EVOBITS、Hetzner、OVH 等）
- **地理分布** — 实际 GPU 硬件的国家/城市 vs RunPod 的“区域”
- **网络拓扑** — 同一区域的 Pod 是否共享 BGP 对等节点？同一 /24 子网 = 同一贡献者
- **贡献者密度** — 出现多少不同的 ASN，集群规模如何

## 最小实现

```python
import subprocess, socket, requests, json
from concurrent.futures import ThreadPoolExecutor

def probe_pod_network():
    # 在 RunPod Pod 内部运行
    results = {}

    # 获取出站 IP
    r = requests.get("https://ipinfo.io/json", timeout=5)
    info = r.json()

    results["ip"] = "<IP_ADDRESS>"  # 输出中已脱敏
    results["asn"] = info.get("org")       # 例如 "AS12345 EVOBITS IT SRL"
    results["country"] = info.get("country")
    results["city"] = info.get("city")
    results["hostname"] = info.get("hostname")

    # Traceroute 前 3 跳，查看上游
    tr = subprocess.run(["traceroute", "-m", "3", "8.8.8.8"],
                       capture_output=True, text=True)
    results["traceroute_hops"] = tr.stdout

    return results

print(json.dumps(probe_pod_network(), indent=2))
```

## 成本估算

| 规模 | Pod 数量 | 成本 | 信号 |
| ------ | ---------- | ------ | ------ |
| 快速采样 | 20 个 Pod × $0.20/小时 × 5 分钟 | ~$0.35 | ASN 分布 |
| 可观数据集 | 100 个 Pod | ~$1.70 | 贡献者集群 |
| 真实全景 | 500 个 Pod | ~$8 | 地理密度图 |

使用最便宜的 GPU 等级（RTX 2000 Ada ~$0.19/小时），启动、探测、每个在 5 分钟内终止。

## 自动化脚本

```python
# 本地运行 — 通过 RunPod API 启动 Pod，收集数据，终止
import runpod

runpod.api_key = "<API_KEY>"

def create_probe_pod():
    return runpod.create_pod(
        name="net-probe",
        image_name="python:3.11-slim",
        gpu_type_id="NVIDIA GeForce RTX 2000 Ada Generation",
        cloud_type="ALL",  # 包含社区 = 贡献者 GPU
        container_disk_in_gb=5,
    )

# 通过 RunPod exec API 收集结果，或直接记录到 stdout
```

## 你不会看到什么

- 实际的贡献者身份（RunPod 代理了所有内容）
- Pod 到 Pod 的流量（已隔离）
- 同一硬件上的其他租户

## 真正有趣的地方

`cloud_type="ALL"` 与 `cloud_type="SECURE"` 的区分是关键变量 —— 社区 Pod 直接通过贡献者的家庭或机房网络路由。你很可能会发现：

- 东欧托管商（EVOBITS、M247）主导低价等级
- Hetzner/OVH 占据中端
- AWS/GCP 用于“安全云”

20 美元就能获得一个真正有意义的数据集。没有入侵，仅从你自己的 Pod 中获取元数据 —— 完全符合服务条款。
