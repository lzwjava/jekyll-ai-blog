---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod CLI 和 P2P 文件传输
translated: true
type: note
---

是的，RunPod 提供了一个名为 `runpodctl` 的官方 CLI。

它已预装在每一个 RunPod Pod 中。本地安装方式如下：

```bash
# macOS (Air)
brew install runpod/runpodctl/runpodctl

# Linux (工作站)
wget -qO- cli.runpod.net | sudo bash
```

认证与核心用法：

```bash
runpodctl config --apiKey <​API_KEY>

# Pod 管理
runpodctl get pod
runpodctl create pod --name dev --imageName runpod/pytorch:latest --gpuType "NVIDIA A100"
runpodctl start pod <POD_ID>
runpodctl stop pod <POD_ID>
runpodctl remove pod <POD_ID>

# 文件传输（点对点，无需 SSH）
runpodctl send model.pt        # 打印一次性验证码
runpodctl receive <CODE>       # 在另一台机器上执行
```

`send` / `receive` 组合是最实用的功能——它基于 croc 实现点对点传输，无需配置 SSH 密钥即可穿越 NAT，非常适合在工作站和租用的 Pod 之间移动检查点（checkpoint）。

如需在程序层面控制（在 agent 中启动/关闭 Pod），GraphQL API 和 `runpod` Python SDK（`pip install runpod`）比 CLI 提供了更精细的控制——包括无服务器端点（serverless endpoints）、自动扩缩容（autoscaling），以及可集成到自动化流程中的 `runpod.create_pod()` 调用。

参考资料：

- [runpodctl GitHub](https://github.com/runpod/runpodctl)
- [RunPod CLI 文档](https://docs.runpod.io/cli/overview)
- [RunPod Python SDK](https://github.com/runpod/runpod-python)
