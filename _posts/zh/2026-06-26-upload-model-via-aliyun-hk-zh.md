---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过阿里云香港上传模型
translated: true
type: note
---

没有阿里云CLI。两种方式：

**快速方式——网页控制台（5分钟）：**
1. 访问 ecs.console.aliyun.com
2. 创建实例：香港、Ubuntu 22.04、2核4G、按量付费
3. 设置安全组：允许SSH（22端口）
4. SSH登录，安装 `hf` CLI，上传

**CLI方式——安装阿里云CLI：**
```
brew install aliyun-cli
aliyun configure
# 然后编写脚本创建ECS
```

一次性操作的话，网页控制台更快。需要我为你编写一个完整的shell脚本，在香港实例启动后运行吗？

```bash
# 在阿里云香港实例上执行：
pip install huggingface-hub
hf auth login  # 粘贴你的令牌
# 然后直接从此处上传
hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
```

但首先需要将475MB文件传输到香港。有两种方式：
1. **从Mac通过SCP传输到香港**（通过CN2快速传输，约50MB/s）
2. **在香港从GCS下载**（如果GCS上传已完成）

需要我通过CLI启动实例，还是你想使用网页控制台？