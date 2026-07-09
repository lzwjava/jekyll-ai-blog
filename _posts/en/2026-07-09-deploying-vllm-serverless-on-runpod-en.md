---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deploying vLLM Serverless on RunPod
translated: false
type: note
---

Question: How do you set up and run a vLLM serverless endpoint on RunPod?

Answer:

Seeing **$0.00000/s** and **0 running workers / 0 jobs in progress** means your RunPod Serverless Endpoint is successfully deployed, idling, and costing you absolutely nothing! Because it is serverless, workers only spin up when you send an actual request.

Here is exactly how to run and use your deployed vLLM template on RunPod Serverless.

---

### Step 1: Send a Test Request from the RunPod UI

The easiest way to activate a worker and test your vLLM model is directly through the RunPod Dashboard:

1. Go to your **Serverless Endpoints** tab and click on your endpoint.
2. Select the **Requests** tab on the left-side menu.
3. You will see a default JSON input structure. Modify it to include your prompt:

```json
{
  "input": {
    "prompt": "Explain artificial intelligence in one sentence.",
    "max_tokens": 100
  }
}

```

4. Click **Run** (or **Submit**).
5. **Note on Cold Starts:** Because it says 0 running workers, your first request will trigger a "cold start." RunPod will provision a GPU worker and load your Hugging Face model into VRAM. This initial request can take anywhere from 30 seconds to a few minutes. Subsequent requests will return instantly.

---

### Step 2: Use via cURL (API)

Once you know the endpoint works, you can interact with it programmatically using its native RunPod endpoint URL.

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
     -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"input": {"prompt": "Why is the sky blue?", "max_tokens": 150}}'

```

*Replace `YOUR_ENDPOINT_ID` with the alphanumeric ID found on your endpoint dashboard, and `YOUR_RUNPOD_API_KEY` with your API token found under account settings.*

---

### Step 3: Use via OpenAI-Compatible API

The RunPod vLLM worker natively supports the OpenAI API structure, allowing you to drop it directly into your existing OpenAI code scripts.

#### Python Implementation Example

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_RUNPOD_API_KEY",
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1"
)

response = client.chat.completions.create(
    model="required-but-ignored-by-vllm", # vLLM uses whatever model you specified in your env vars
    messages=[
        {"role": "user", "content": "Tell me a joke about programming."}
    ],
    temperature=0.7,
    max_tokens=200
)

print(response.choices[0].message.content)

```

---

### Important Things to Remember

* **Idle Timeout:** In your endpoint settings, you can configure an **Idle Timeout** (e.g., 60 seconds). Once requests stop coming in, RunPod will wait for this duration before shutting down the GPU worker, dropping your active cost back to $0.00/s.
* **Environment Variables:** If your model fails to load during the test request, check your endpoint's environment variables. Ensure `MODEL_NAME` matches the exact Hugging Face repo ID, and if it is a gated model (like Llama), ensure your `HF_TOKEN` is correctly supplied.

References:

* [Deploy vLLM on Runpod Serverless](https://docs.runpod.io/serverless/vllm/get-started)
* [RunPod vLLM Worker Template GitHub](https://github.com/runpod-workers/worker-vllm)
