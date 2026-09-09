---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4090 服务器就绪
translated: true
type: note
---

连接成功。以下是该服务器上的信息：

## GPU
**NVIDIA GeForce RTX 4090**（1 张卡）
- **显存**：24 GB（24564 MiB）——当前已用 0 MiB，无运行进程
- **驱动**：595.91.07，**CUDA**：13.2
- 空闲状态：26°C，17W / 450W 上限，利用率 0%

## Machine specs

| 资源 | 数值 |
|---|---|
| CPUs | 144 核 |
| 内存 | 629 GB 总计（585 GB 可用） |
| 磁盘（根分区） | 30 GB overlay，基本为空 |
| 操作系统 | 容器化环境（overlay fs） |

单张 RTX 4090，CPU/内存余量充足——适合推理或小规模微调（例如对 7B–13B 模型进行 LoRA），但 30 GB 的根磁盘空间有限，如需存储大型模型会显得紧张，如有需要，请检查是否有其他挂载卷。