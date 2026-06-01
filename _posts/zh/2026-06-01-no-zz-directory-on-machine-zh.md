---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 机器上没有ZZ目录
translated: true
type: note
---

此机器上不存在 `zz` 目录。以下是完整情况：

```
根磁盘（697G，已用 88G，可用 610G）
├── /var            60G   ← containerd 59G + 系统日志
├── /opt            22G   ← ROCm 7.2.0（GPU 运行时，必需）
├── /root           385M  ← llama.cpp 源码 + 构建脚本
├── /usr            6.3G  ← 系统软件包
└── /home           空

卷（100G，已用 37G，可用 63G）
└── llama-models    37G   ← GGUF 模型（从 /root/llama.cpp/models 符号链接）
```

此处没有 `zz` 数据。这台机器上仅有的体积较大的数据如下：

| 项目 | 位置 | 大小 |
|------|------|------|
| ROCm 运行时 | /opt/rocm-7.2.0 | 22G |
| 容器镜像 | /var/lib/containerd | 59G |
| Llama 模型 | 卷（符号链接） | 37G |

一切都在原位，无需移动。根磁盘尚有 610G 可用空间——无需再将其他数据移动到卷上。实际上卷的空间更为紧张（仅剩 63G 可用）。

`zz` 是您期望在这台机器上看到的内容，还是另有所指？