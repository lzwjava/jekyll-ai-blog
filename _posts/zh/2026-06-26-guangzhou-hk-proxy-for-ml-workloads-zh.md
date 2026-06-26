---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 广州-香港机器学习工作负载代理
translated: true
type: note
---

您的 VPN/代理路由为广州 → 香港，对于 HuggingFace 及多数国际 ML 流量而言，这确实是一个不错的配置。

原因如下：

**地理 + 对等直连。** 广州到香港约 140 公里。您测得的 1.6ms 延迟意味着流量几乎立即到达 CloudFront HKG 边缘节点。香港位于 GFW 之外，因此一旦数据包抵达阿里云香港实例（AS45102），便能通过不受限制、对等良好的路由访问 AWS/CloudFront/HuggingFace CDN 端点。

**瓶颈不在香港→HuggingFace，而在内地→香港。** 您测得的 5.7 MB/s 是香港节点到 HuggingFace 的出站速度——这是干净的。您的实际限制是广州→香港段跨越边境的部分，限流、丢包和抖动都发生在这里。因此，明智的架构是：让香港节点负责大量拉取工作，而不是通过隧道在您的 Mac 上完成。

针对您的实际工作流，这意味着：

```bash
# 在香港的阿里云节点上拉取/缓存模型
export HF_HUB_ENABLE_HF_TRANSFER=1
pip install -U "huggingface_hub[hf_transfer]" hf_transfer
hf download deepseek-ai/DeepSeek-V3 --local-dir ./models/dsv3

# 然后通过压缩一次性同步到您的 Mac / 工作站（跨越边境）
rsync -avz --progress lzw@<HK_IP>:./models/dsv3 ~/models/
```

`hf_transfer`（基于 Rust）通过并行分块下载饱和链路——如果 HuggingFace 的 CDN 提供更多并发连接，它将使 5.7 MB/s 更高。值得对比测试开启与关闭该功能的效果。

关于“不错”的一点说明：5.7 MB/s（约 45 Mbps）对于香港数据中心节点来说*还可以*，但并不出色——阿里云香港实例到 AWS 边缘通常能达到 100+ Mbps。如果您要拉取一个 600GB 的 MoE 检查点，5.7 MB/s 大约需要 30 小时。请检查您的实例是否有带宽上限（1.6GB RAM / 2 核表明是小规格/可突发实例，这类实例通常出站带宽受限）：

```bash
# 快速原始吞吐测试，绕过 HF 应用层
curl -o /dev/null -w "%{speed_download}\n" \
  https://cdn-lfs.huggingface.co/<some-large-file>
```

因此：通过广州→香港路由是访问国际 ML 基础设施的正确选择。只需让香港节点作为主力，将跨境链路视为一次性同步，而非热点路径。