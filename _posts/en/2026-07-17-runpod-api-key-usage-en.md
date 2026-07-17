---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod API Key Usage
translated: false
type: note
---

Question: How do I use a RunPod API key (REST + GraphQL + Python SDK)?

Answer: There are two API surfaces — new REST API (`rest.runpod.io`) and legacy GraphQL (`api.runpod.io/graphql`). Both use the same key from Settings → API Keys.

**REST (preferred, use `Bearer` header):**

```bash
export RUNPOD_API_KEY=<RUNPOD_API_KEY>

# list pods
curl https://rest.runpod.io/v1/pods \
  --header "Authorization: Bearer $RUNPOD_API_KEY"

# stop a pod
curl -X POST https://rest.runpod.io/v1/pods/<POD_ID>/stop \
  --header "Authorization: Bearer $RUNPOD_API_KEY"

# create a serverless endpoint
curl -X POST https://rest.runpod.io/v1/endpoints \
  --header "Authorization: Bearer $RUNPOD_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "my-endpoint",
    "templateId": "<TEMPLATE_ID>",
    "gpuTypeIds": ["NVIDIA GeForce RTX 4090"],
    "scalerType": "QUEUE_DELAY",
    "scalerValue": 4,
    "workersMin": 0,
    "workersMax": 5
  }'
```

**GraphQL (legacy, key as query param):**

```bash
curl -X POST "https://api.runpod.io/graphql?api_key=$RUNPOD_API_KEY" \
  -H 'content-type: application/json' \
  -d '{"query":"mutation { podResume(input:{podId:\"<POD_ID>\", gpuCount:1}) { id desiredStatus } }"}'
```

**Python SDK** (`pip install runpod`), useful if you're calling serverless endpoints from a script:

```python
import runpod
runpod.api_key = "<RUNPOD_API_KEY>"

endpoint = runpod.Endpoint("<ENDPOINT_ID>")
result = endpoint.run_sync({"input": {"prompt": "hello"}})
print(result)
```

You can also scope a key per-endpoint (`runpod.Endpoint(id, api_key="specific_key")`) if you want to isolate serverless workers from pod-management access — worth doing if you're running this from CI or a shared agent, since the key otherwise has full account access (start/stop/delete pods, billing-affecting actions).

For your MI300X training runs, the REST `/v1/pods` endpoints are what you want for spin-up/spin-down automation in a bash loop or your `ww`/`zz` CLI — no need to touch GraphQL unless you need template management, which REST doesn't fully cover yet.

References:

- [RunPod API Keys](https://docs.runpod.io/get-started/api-keys)
- [RunPod REST API blog](https://www.runpod.io/blog/runpod-rest-api-gpu-management)
- [Manage Pods - GraphQL API](https://docs.runpod.io/sdks/graphql/manage-pods)
- [runpod PyPI SDK](https://pypi.org/project/runpod/)
