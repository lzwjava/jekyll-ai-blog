---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod 网络卷 S3 访问
translated: true
type: note
---

问：RunPod 网络卷存储使用的是 S3 吗？

答：**是的，但有一个重要区别。** RunPod 网络卷**实际上并非 AWS S3 存储桶**，但 RunPod 提供了一个 **S3 兼容的 API 层** 来访问它们。

你的卷：

```
名称：pleasant_apricot_swift
大小：30 GB
数据中心：EU-RO-1
S3 API 访问：已启用
```

意味着：

* 实际存储是一个 **RunPod 网络卷**。
* 你可以在 Pod 内正常挂载它（例如 `/workspace`）。
* 你还可以通过 **S3 兼容的端点** 使用以下工具从外部访问它：

  * `aws s3`
  * `s3cmd`
  * `rclone`
  * Python SDK（`boto3`）

模型大致如下：

```
                 +----------------+
                 | RunPod Pod     |
                 |                |
                 | /workspace     |
                 +-------+--------+
                         |
                         |
                 RunPod 网络卷
                         |
                         |
              +----------+----------+
              |                     |
        POSIX 挂载              S3 API
        （文件系统）             （对象 API）
              |                     |
        Linux 命令              aws/rclone/boto3
        cp/rsync               上传/下载
```

Pod 内示例：

```bash
ls /workspace
cp model.gguf /workspace/models/
```

通过 S3 API 示例：

```bash
aws configure
```

设置：

```
AWS_ACCESS_KEY_ID=<RUNPOD_ACCESS_KEY>
AWS_SECRET_ACCESS_KEY=<RUNPOD_SECRET>
```

然后：

```bash
aws s3 ls \
  --endpoint-url https://<runpod-s3-endpoint>
```

或者：

```bash
aws s3 cp model.gguf \
  s3://<卷名称>/models/
```

S3 接口适用于：

* 在启动 Pod 之前上传大型模型
* 在机器之间移动数据集
* 备份
* 自动化流水线

对于 AI 工作负载，常见模式如下：

```
网络卷
      |
      +-- models/
      |     llama/
      |     qwen/
      |     gemma/
      |
      +-- datasets/
      |
      +-- checkpoints/
      |
      +-- cache/
            huggingface/
            torch/
```

然后，同一 RunPod 区域内的每个新 GPU Pod 都可以挂载此卷并立即重用数据。

一个重要限制：**网络卷是区域特定的。** 你的卷是：

```
EU-RO-1
```

因此通常只能挂载到同一数据中心/区域的 Pod 上。它不像全局复制的 S3 存储那样全球可用。

对于 LLM 服务（SGLang/vLLM），这实际上是首选设置：将模型放在网络卷上，启动 GPU Pod，挂载卷，然后启动服务器。
