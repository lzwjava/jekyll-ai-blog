---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 启动 RunPod 无服务器端点
translated: true
type: note
---

问题：当 RunPod Serverless vLLM 端点显示 `0 个运行中的工作进程`、`0 个进行中的任务` 和 `0 个队列中等待的任务` 时，我该如何实际启动它？

回答：

这种状态是 **正常的**。RunPod Serverless 采用 **按需缩容至零** 机制。

```
0 个运行中的工作进程
0 个任务
```

并 **不** 意味着出现问题。它表示：

* 当前未分配 GPU。
* 尚未收到任何请求。
* 您无需为空闲 GPU 付费。

其生命周期如下：

```
创建端点
        │
        ▼
0 个工作进程（空闲）
        │
        ▼
发送第一个请求
        │
        ▼
RunPod 分配 GPU
        │
        ▼
下载模型
        │
        ▼
启动 vLLM
        │
        ▼
处理请求
        │
        ▼
返回结果
        │
        ▼
空闲超时后
        │
        ▼
工作进程再次关闭
```

### 选项一 — 使用 RunPod UI（最简单）

打开您的端点：

```
请求
```

使用类似以下内容：

```json
{
  "input": {
    "prompt": "Hello"
  }
}
```

点击 **运行**。

队列将变为

```
1 个等待中
```

然后变为

```
1 个运行中
```

接着您会看到

```
1 个工作进程
```

在执行过程中。首个请求可能需要几分钟时间，因为 RunPod 必须配置 GPU 并下载模型。([Runpod 文档][1])

---

### 选项二 — 使用 curl

```bash
curl -X POST \
  https://api.runpod.ai/v2/<ENDPOINT_ID>/runsync \
  -H "Authorization: Bearer <RUNPOD_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
          "prompt": "Hello"
        }
      }'
```

这个单独的请求会自动启动一个工作进程。([Runpod 文档][1])

---

### 选项三 — 兼容 OpenAI 的 API

在工作进程运行后，vLLM 模板也会暴露一个兼容 OpenAI 的 API，因此您可以将 OpenAI SDK 或 LiteLLM/OpenWebUI 指向它。([Runpod 文档][2])

---

### 如果工作进程始终为 0

那么说明存在问题。请检查：

* 端点状态是否为 **活跃**
* 是否已选择 GPU 类型
* 如果您期望工作进程始终保持活跃，`MIN_WORKERS` 是否意外设置为 0
* 模型名称是否正确（例如 `Qwen/Qwen3-8B`）
* 如果模型受限制，是否已配置 Hugging Face 令牌
* 端点日志中是否有模型下载或 OOM 错误 ([Runpod 文档][1])

---

由于您一直在 RunPod 上尝试 **SGLang** 和 **vLLM**，我建议先发送一个简单的 `runsync` 请求。如果您提供：

* 端点配置，
* 所选 GPU，
* 模型名称，以及
* 端点日志，

我通常可以在一分钟内识别启动问题。

参考：

* [RunPod: 在 Serverless 上部署 vLLM](https://docs.runpod.io/serverless/vllm/get-started?utm_source=chatgpt.com)
* [RunPod vLLM 概述](https://docs.runpod.io/serverless/vllm/overview?utm_source=chatgpt.com)

[1]: https://docs.runpod.io/serverless/vllm/get-started?utm_source=chatgpt.com "在 Runpod Serverless 上部署 vLLM - Runpod 文档"
[2]: https://docs.runpod.io/serverless/vllm/overview?utm_source=chatgpt.com "概述 - Runpod 文档"