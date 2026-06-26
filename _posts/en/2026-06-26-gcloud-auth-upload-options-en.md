---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gcloud Auth Upload Options
translated: false
type: note
---

No gcloud on the server either. On the Mac we have gcloud but no credentials. Two paths:

**Option A — Auth on Mac, upload directly:**

```
gcloud auth login
gcloud config set project lzwjava1
gcloud storage cp -r ~/projects/sec-edgar-gpt-124m gs://lzwjava1/sec-edgar-gpt-124m
```

**Option B — Install gcloud on server, upload from there:**

```
ssh root@69.63.219.52
curl -sSL https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud auth login
gcloud storage cp -r /root/sec-edgar-gpt-124m gs://lzwjava1/sec-edgar-gpt-124m
```

Which way? If the server has better bandwidth, Option B. Otherwise A is simpler — just need `gcloud auth login` (opens browser).
