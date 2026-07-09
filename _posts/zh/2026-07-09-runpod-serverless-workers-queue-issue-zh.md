---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod服务器无服务器工作者队列问题
translated: true
type: note
---

问题：为什么我的 RunPod 无服务器请求即使有 2 个运行中的 worker，仍然停留在“排队”状态？

回答：

这**不正常**。如果你看到：

```
2 个运行中的 worker
0 个正在处理的任务
2 个任务在排队等待
```

那么这些 worker **实际上并没有接受请求**。

正常情况下应该显示为：

```
2 个运行中的 worker
1 个正在处理的任务
1 个任务在排队等待
```

或

```
2 个运行中的 worker
2 个正在处理的任务
0 个任务在排队等待
```

## 最常见的原因

### 1. vLLM 仍在加载模型（最常见）

从 RunPod 的角度来看，worker 处于“运行中”状态，但在容器内部，vLLM 仍在进行以下操作：

* 下载模型
* 加载权重
* 分配 KV cache
* 编译 CUDA 内核

如果你正在加载 30B 参数以上的模型，这个过程可能需要几分钟。

请前往：

```
Workers
→ 选择一个 worker
→ Logs
```

如果你看到类似以下内容：

```
Downloading model...
Loading safetensors...
Initializing engine...
```

那么这是正常现象。

---

### 2. Worker 从未进入就绪状态

有时容器已经启动，但你的 handler 从未报告就绪状态。

典型的日志：

```
Starting...
```

然后就没有下文了。

或

```
Waiting for health check...
```

请求会一直排队等待。

---

### 3. vLLM 在启动时崩溃

例如：

```
CUDA out of memory

Killed

Segmentation fault

ImportError
```

RunPod 可能仍在尝试重启 worker，而你的请求则一直停留在队列中。

---

### 4. 错误的 endpoint 配置

例如：

* 端口错误
* 健康检查 endpoint 错误
* handler 错误
* 容器从未开始监听

这种情况下，worker 看起来是存活的，但无法接收推理请求。

---

### 5. 模型大小超过 GPU 内存

例如：

```
72B FP16
```

运行在

```
RTX 4090
16GB GPU
```

worker 反复崩溃，而 RunPod 不断重试。

---

## 我建议首先检查的内容

打开 **Workers → Logs**。

最后几行应该以类似以下内容结尾：

```
INFO Engine initialized
INFO Uvicorn running
INFO Ready
```

或

```
Server started
```

如果最后几行停在

```
Loading checkpoint shards...
```

那么你只需要等待模型初始化完成即可。

---

## 你当前的状况

由于**两个 worker** 都在排队，且**0 个任务正在运行**，我推测可能是以下原因之一：

* ✅ worker 仍在加载模型（≈70% 概率）
* ✅ 启动失败（≈25%）
* ✅ endpoint 配置问题（≈5%）

---

如果你能粘贴 **Worker Logs**（尤其是最后 50–100 行），我通常可以在几分钟内确定具体原因。