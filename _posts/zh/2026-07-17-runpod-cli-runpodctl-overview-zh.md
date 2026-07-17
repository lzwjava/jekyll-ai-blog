---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'RunPod CLI: runpodctl 概览'
translated: true
type: note
---

## Question: RunPod 是否有 CLI？

## Answer: 是的 — `runpodctl`

每个 pod 都预装了它以及一个 pod 作用域的 API 密钥。如果你希望从自己的机器进行远程编排，也可以在本地安装。

**安装：**
```bash
wget -qO- cli.runpod.net | sudo bash
# 或者
brew install runpod/runpodctl/runpodctl
# 或者 conda-forge
conda install conda-forge::runpodctl
```

**首次设置：**
```bash
runpodctl doctor   # 一次性配置 API 密钥和 SSH
# 或者手动配置：
runpodctl config --apiKey=<RUNPOD_API_KEY>
```

**核心命令（名词‑动词模式）：**
```bash
runpodctl gpu list                          # 可用的 GPU 类型
runpodctl datacenter list                   # 数据中心可用性
runpodctl template search pytorch           # 搜索模板
runpodctl pod create --image=runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04 --gpu-id=NVIDIA_A100
runpodctl pod list
runpodctl pod get <pod_id>
runpodctl pod start <pod_id>
runpodctl pod stop <pod_id>
runpodctl pod delete <pod_id>

runpodctl serverless ...   # 别名：sls
runpodctl network-volume ...  # 别名：nv
runpodctl registry ...     # 别名：reg
runpodctl user             # 账户/余额信息，别名：me
runpodctl billing          # 账单历史
```

**文件传输（不需要 API 密钥，使用一次性码）：**
```bash
runpodctl send data.txt
# 代码是：8338-galileo-collect-fidel
# 在另一台机器上：
runpodctl receive 8338-galileo-collect-fidel
```

旧的 `get/create/remove/start/stop/exec/project/config` 动词现已废弃，建议使用名词‑动词形式（如 `pod create`、`pod start` 等），但旧的语法仍然有效。

对于你的 MI300X/GPT-2 训练任务而言，这基本上就是你的整个运维循环：`pod create` → `ssh` → train → `pod stop`，可从头到尾进行脚本化。

参考链接：
- [Runpod CLI Overview](https://docs.runpod.io/runpodctl/overview)
- [runpodctl GitHub README](https://github.com/runpod/runpodctl)
- [runpodctl full command reference](https://github.com/runpod/runpodctl/blob/main/docs/runpodctl.md)