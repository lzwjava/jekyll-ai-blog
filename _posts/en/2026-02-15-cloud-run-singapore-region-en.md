---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Cloud Run Region for Singapore
translated: false
type: note
---

Question: If I want to deploy to Singapore for low latency, which Google Cloud Run region should I select?

Answer:

For Singapore (or users in/near Singapore), select the region **`asia-southeast1`**.

- This region is physically located **in Singapore** (specifically Jurong West).
- It provides the **lowest possible latency** for users in Singapore, Malaysia, Indonesia, and much of Southeast Asia.
- Cloud Run fully supports `asia-southeast1` (it's listed in the official Cloud Run locations documentation).
- It's one of the standard, generally available regions for Cloud Run deployments.

### Updated deploy command example (replace your previous region)

```bash
gcloud run deploy blog-server \
  --source . \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --verbosity=debug   # optional, for troubleshooting
```

### Nearby alternatives (if needed)
- If `asia-southeast1` has any temporary quota/issue (very rare), the next closest are:
  - `asia-southeast2` → Jakarta, Indonesia (still quite close, good for Indonesia-focused traffic)
  - `asia-east2` → Hong Kong (farther, higher latency from Singapore)
  - `asia-northeast1` → Tokyo (much farther)

But **always prefer `asia-southeast1`** for Singapore.

### Quick verification tip
To see all available regions for Cloud Run in your project (some features like GPUs may vary):

```bash
gcloud run regions list
```

Or check the official docs/console for the latest.

This should give you much better performance than your previous `asia-northeast1` (Tokyo) choice!

References:

- [Cloud Run locations](https://docs.cloud.google.com/run/docs/locations)
- [Google Cloud regions and zones](https://cloud.google.com/about/locations)
- [Regions and zones | Compute Engine (confirms Singapore location)](https://docs.cloud.google.com/compute/docs/regions-zones)
