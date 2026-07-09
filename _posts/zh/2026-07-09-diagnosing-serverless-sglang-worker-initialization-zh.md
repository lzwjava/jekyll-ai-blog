---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断无服务器SGLang工作进程初始化
translated: true
type: note
---

问题：为什么我的 RunPod Serverless SGLang 工作器卡在 `initializing` 状态，显示 `0 running workers` 和 `2 jobs waiting in queue`？

答案：

你的端点尚未完成启动。关键信息是：

```
0 running workers
2 jobs waiting in queue

Worker 1: initializing
Worker 2: initializing
```

这意味着 **Kubernetes Pod 从未进入 Ready 状态**，因此没有工作器可以处理请求。

对于 RTX 4090 上的 SGLang，最常见的原因如下：

| 原因                         | 症状                     | 检查方式       |
| ---------------------------- | ------------------------ | -------------- |
| 模型下载仍在进行中           | 持续 `initializing` 5–30 分钟 | 工作器日志     |
| Hugging Face 认证失败        | 401/403 错误             | 日志           |
| 磁盘空间不足                 | 下载失败                 | 日志           |
| 容器崩溃                     | 重启循环                 | 工作器日志     |
| CUDA/OOM（显存不足）         | 工作器在 Ready 前死亡    | 日志           |
| 启动命令错误                 | 服务器从未启动           | 日志           |

## 1. 查看工作器日志

不要先查看端点日志。

前往

```
Workers
    ↓
点击一个工作器
    ↓
Logs
```

或者

```
Releases
    ↓
Latest
    ↓
Logs
```

最后 20–50 行通常会准确告诉你初始化失败的原因。

典型消息包括：

```
Downloading model...
```

这意味着只需等待。

或者

```
401 Unauthorized
```

表示你的 `HF_TOKEN` 缺失。

或者

```
CUDA out of memory
```

表示模型过大。

或者

```
Killed
```

表示容器超过内存限制或被 OOM 杀死。

---

## 2. 你加载的是哪个模型？

你之前提到过

```
unsloth/gemma-4-e4b-it-gguf
```

如果你仍然尝试在 SGLang 中运行它，那很可能就是问题所在。

SGLang **不直接提供 GGUF 模型服务**。

它期望的是 Hugging Face Transformers 检查点，例如：

```
Qwen/Qwen3-8B
meta-llama/Llama-3.1-8B-Instruct
Qwen/Qwen2.5-7B-Instruct
```

如果你指定了 GGUF 模型，初始化可能会失败。

---

## 3. 模型是否受控（gated）？

如果使用类似

```
meta-llama/*
google/gemma*
```

的模型，你必须提供

```
HF_TOKEN=<YOUR_TOKEN>
```

否则工作器无法下载权重。

---

## 4. 模型是否过于庞大？

RTX 4090 拥有 **24 GB 显存**。

大致需求如下：

* 7B FP16 → ~14 GB ✅
* 8B BF16 → ~16 GB ✅
* 14B FP16 → ~28 GB ❌
* 27B → ❌
* 70B → 不可能

如果你意外选择了大模型，初始化将永远无法成功。

---

## 5. 是否仍在下载中？

首次启动很容易需要

* 5 分钟
* 10 分钟
* 20 分钟以上

具体取决于：

* 模型大小
* Hugging Face 速度
* 区域
* 缓存

状态会一直保持

```
initializing
```

直到下载完成。

---

## 诊断所需信息

请提供 **以下任一**：

1. 工作器日志的最后 **50 行**，或
2. 你的端点配置：

   * 模型名称
   * 环境变量
   * 启动命令

有了这些信息，我通常能在一分钟内找出问题。