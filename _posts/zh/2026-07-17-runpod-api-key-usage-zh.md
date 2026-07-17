---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod API 密钥使用
translated: true
type: note
---

问题：如何使用 RunPod API 密钥（REST + GraphQL + Python SDK）？

有两个 API 接口——新的 REST API（`rest.runpod.io`）和旧的 GraphQL（`api.runpod.io/graphql`）。两者都使用来自设置 → API 密钥的同一密钥。

**REST（推荐，使用 `Bearer` 标头）：**

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

**GraphQL（旧版，密钥作为查询参数）：**

```bash
curl -X POST "https://api.runpod.io/graphql?api_key=$RUNPOD_API_KEY" \
  -H 'content-type: application/json' \
  -d '{"query":"mutation { podResume(input:{podId:\"<POD_ID>\", gpuCount:1}) { id desiredStatus } }"}'
```

**Python SDK**（`pip install runpod`），适用于从脚本调用无服务器端点：

```python
import runpod
runpod.api_key = "<RUNPOD_API_KEY>"

endpoint = runpod.Endpoint("<ENDPOINT_ID>")
result = endpoint.run_sync({"input": {"prompt": "hello"}})
print(result)
```

您还可以为每个端点限定密钥范围（`runpod.Endpoint(id, api_key="specific_key")`），如果您想将无服务器工作器与 Pod 管理访问隔离——如果您从 CI 或共享代理运行此操作，这是值得做的，因为否则密钥具有完全账户访问权限（启动/停止/删除 Pod、影响计费的操作）。

对于您的 MI300X 训练运行，REST `/v1/pods` 端点正是您在 bash 循环或 `ww`/`zz` CLI 中实现自动启停所需要的——除非您需要模板管理（REST 尚未完全覆盖），否则无需接触 GraphQL。

参考：

- [RunPod API 密钥](https://docs.runpod.io/get-started/api-keys)
- [RunPod REST API 博客](https://www.runpod.io/blog/runpod-rest-api-gpu-management)
- [管理 Pod - GraphQL API](https://docs.runpod.io/sdks/graphql/manage-pods)
- [runpod PyPI SDK](https://pypi.org/project/runpod/)
