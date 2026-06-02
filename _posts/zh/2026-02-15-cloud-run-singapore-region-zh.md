---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 新加坡最佳 Cloud Run 区域
translated: true
type: note
---

Question: 如果我想部署到 Singapore 以获得低延迟，我应该选择哪个 Google Cloud Run region？

Answer:

对于 Singapore（或位于/靠近 Singapore 的用户），请选择 region **`asia-southeast1`**。

- 该 region 的物理位置位于 **Singapore**（具体在 Jurong West）。
- 它为 Singapore、Malaysia、Indonesia 以及大部分 Southeast Asia 的用户提供**最低的延迟**。
- Cloud Run 完全支持 `asia-southeast1`（它已列在官方 Cloud Run locations 文档中）。
- 它是 Cloud Run 部署的标准、常规可用的 regions 之一。

### 更新后的 deploy command 示例（替换你之前的 region）

```bash
gcloud run deploy blog-server \
  --source . \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --verbosity=debug   # 可选，用于 troubleshooting
```

### 附近的备选方案（如有需要）

- 如果 `asia-southeast1` 出现任何临时的配额/问题（非常罕见），距离最近的备选方案是：
  - `asia-southeast2` → Jakarta, Indonesia（仍然非常近，适合针对 Indonesia 流量）
  - `asia-east2` → Hong Kong（较远，从 Singapore 访问延迟较高）
  - `asia-northeast1` → Tokyo（远得多）

但针对 Singapore，**始终首选 `asia-southeast1`**。

### 快速验证技巧

要查看项目中 Cloud Run 所有可用的 regions（某些功能如 GPUs 可能会有所不同）：

```bash
gcloud run regions list
```

或者检查官方文档/控制台获取最新信息。

这应该会比你之前选择的 `asia-northeast1` (Tokyo) 提供更好的性能！

References:

- [Cloud Run locations](https://docs.cloud.google.com/run/docs/locations)
- [Google Cloud regions and zones](https://cloud.google.com/about/locations)
- [Regions and zones | Compute Engine (确认 Singapore 位置)](https://docs.cloud.google.com/compute/docs/regions-zones)
