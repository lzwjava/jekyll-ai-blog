---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在RunPod上部署vLLM无服务器
translated: true
type: note
---

问题：如何在 RunPod 上设置并运行 vLLM 无服务器端点？

答案：

看到 **$0.00000/s** 和 **0 个运行中的 worker / 0 个进行中的任务** 意味着你的 RunPod 无服务器端点已成功部署，处于空闲状态，并且完全免费！由于它是无服务器架构，只有在你发送实际请求时，worker 才会启动。

以下是关于如何在 RunPod Serverless 上运行并使用你所部署的 vLLM 模板的具体步骤。

---

### 步骤 1：通过 RunPod UI 发送测试请求

激活 worker 并测试你的 vLLM 模型最简单的方式就是直接通过 RunPod 控制面板：

1. 进入 **Serverless Endpoints** 标签页，点击你的端点。
2. 在左侧菜单中，选择 **Requests** 标签页。
3. 你会看到一个默认的 JSON 输入结构。修改它，加入你的提示词：
```json
{
  "input": {
    "prompt": "用一句话解释人工智能。",
    "max_tokens": 100
  }
}
```

4. 点击 **Run**（或 **Submit**）。
5. **关于冷启动的说明：** 由于显示 0 个运行中的 worker，你的第一个请求会触发“冷启动”。RunPod 将配置一个 GPU worker，并将你的 Hugging Face 模型加载到显存中。初始请求可能需要 30 秒到几分钟不等。后续请求会立即返回。

---

### 步骤 2：通过 cURL（API）使用

一旦确认端点工作正常，你可以通过其原生 RunPod 端点 URL 以编程方式与之交互。

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
     -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"input": {"prompt": "为什么天空是蓝色的？", "max_tokens": 150}}'
```

*请将 `YOUR_ENDPOINT_ID` 替换为端点仪表盘上的字母数字 ID，并将 `YOUR_RUNPOD_API_KEY` 替换为账户设置中的 API 令牌。*

---

### 步骤 3：通过 OpenAI 兼容 API 使用

RunPod vLLM worker 原生支持 OpenAI API 结构，允许你直接将其集成到现有的 OpenAI 代码脚本中。

#### Python 实现示例：

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_RUNPOD_API_KEY",
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1"
)

response = client.chat.completions.create(
    model="required-but-ignored-by-vllm", # vLLM 使用你在环境变量中指定的任何模型
    messages=[
        {"role": "user", "content": "给我讲一个关于编程的笑话。"}
    ],
    temperature=0.7,
    max_tokens=200
)

print(response.choices[0].message.content)
```

---

### 重要注意事项

* **空闲超时：** 在端点设置中，你可以配置 **空闲超时**（例如 60 秒）。一旦不再有请求进来，RunPod 会等待此持续时间，然后关闭 GPU worker，使你的活跃成本下降到 $0.00/s。
* **环境变量：** 如果在测试请求期间模型加载失败，请检查端点的环境变量。确保 `MODEL_NAME` 与准确的 Hugging Face 仓库 ID 一致；如果是受限模型（如 Llama），请确保 `HF_TOKEN` 已正确提供。

参考文献：

* [在 Runpod Serverless 上部署 vLLM](https://docs.runpod.io/serverless/vllm/get-started)
* [RunPod vLLM Worker 模板 GitHub](https://github.com/runpod-workers/worker-vllm)