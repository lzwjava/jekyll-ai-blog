---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 持久存储网络卷
translated: true
type: note
---

问题：RunPod 存储：选择 **Volume Disk** 还是 **Network Volume**？

答案：

对于大多数严肃的工作负载（模型、数据集、部署），选择 **Network Volume**。

对比：

|                     | Volume Disk                              | Network Volume                         |
| ------------------- | ---------------------------------------- | -------------------------------------- |
| 范围               | 仅单个 Pod                               | 跨 Pod 共享                            |
| 生命周期           | 与 Pod 生命周期绑定                      | 独立于 Pod                             |
| 删除 Pod            | 数据被删除                               | 数据保留                               |
| 移动到其他 GPU      | 否                                       | 是                                     |
| 多个 Pod            | 否                                       | 是                                     |
| 启动速度            | 快（本地磁盘）                           | 稍慢                                   |
| 成本                | 运行时 $0.10/GB/月，停止时 $0.20/GB/月   | 通常对于长期存储更便宜                 |
| 最适合              | 临时缓存                                 | 模型、数据集、生产环境                 |

对于你的使用场景：

* SGLang
* LibreChat
* LLM 权重（7B/14B/30B）
* 模型缓存
* 训练数据
* 你想复用的脚本

→ **Network Volume 是正确的选择。**

典型设置：

```
RunPod Network Volume
        |
        mounted at
        |
    /workspace

        |
        +-- models/
        |     +-- llama/
        |     +-- qwen/
        |
        +-- datasets/
        |
        +-- scripts/
        |
        +-- configs/
```

然后你可以：

1. 使用 RTX 4090 创建 Pod A
2. 下载模型：

```bash
cd /workspace
huggingface-cli download Qwen/Qwen3-8B --local-dir models/qwen3-8b
```

3. 删除 Pod A。

之后：

4. 使用 A6000/H100/RTX 2000 Ada 创建 Pod B
5. 挂载同一个 Network Volume
6. 模型已经在那里了。

对于 AI 开发，模式是：

```
Network Volume = 持久化状态
Pod = 可丢弃的计算资源
```

类似于：

```
Docker 容器  -> Pod
Docker 卷    -> Network Volume
```

我建议避免将重要内容放在普通 Volume Disk 的 `/workspace` 中。

对于你当前的 RunPod 设置（SGLang + LibreChat 聊天机器人），我会使用：

```
Network Volume: 50-200GB
    /workspace/models
    /workspace/huggingface-cache
    /workspace/projects
```

然后，在更换 GPU 时自由重新创建 Pod。