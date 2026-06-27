---
audio: false
generated: true
image: false
lang: en
layout: post
title: Missing Channel for azure/gpt-5.5
translated: false
type: note
---

The error is not from Hermes — it's from **ORG2** trying to call `azure/gpt-5.5` through a new-api/one-api reverse proxy. The Chinese error message:

```
分组 default 下模型 azure/gpt-5.5 无可用渠道（distributor）
```

means: **"Model azure/gpt-5.5 has no available channels under the 'default' group"**

This is a backend config issue on the API proxy side, not an ORG2 code bug.


## How to Fix

**Option 1 — Change the model in ORG2**

In the ORG2 app, go to Settings → Provider/Model settings and switch from `azure/gpt-5.5` to a model that actually exists in your proxy. If your proxy is backed by Azure OpenAI, common available models are:
- `azure/gpt-4o`
- `azure/gpt-4o-mini`
- `azure/gpt-4.1`

**Option 2 — Add the model to your new-api/one-api proxy**

If you're running a new-api or one-api instance:
1. Log in to your proxy admin panel
2. Go to Channels → edit the Azure channel
3. Add `gpt-5.5` to the model list (or check if it's even a real model name — as of now, `gpt-5.5` doesn't exist from OpenAI/Azure)
4. Make sure the channel is enabled and healthy

**Option 3 — Check if the model name is correct**

`gpt-5.5` is not a known OpenAI/Azure model. If you meant:
- `gpt-4.5` → available as Azure model in some regions
- `o3` / `o4-mini` → reasoning models
- `gpt-4o` → most common

Update the model name in ORG2 to match what your proxy actually supports.


## TL;DR

Your API proxy (new-api/one-api) has no channel configured for `azure/gpt-5.5`. Either fix the model name in ORG2 settings, or add the model to your proxy's channel config. The "reconnecting" state is ORG2 retrying the failed request.
