---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gcloud 身份验证上传选项
translated: true
type: note
---

服务器上也没有 gcloud。在 Mac 上我们有 gcloud 但没有凭证。两种方式：

**选项 A — 在 Mac 上认证后直接上传：**

```
gcloud auth login
gcloud config set project lzwjava1
gcloud storage cp -r ~/projects/sec-edgar-gpt-124m gs://lzwjava1/sec-edgar-gpt-124m
```

**选项 B — 在服务器上安装 gcloud 并从那里上传：**

```
ssh root@69.63.219.52
curl -sSL https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud auth login
gcloud storage cp -r /root/sec-edgar-gpt-124m gs://lzwjava1/sec-edgar-gpt-124m
```

哪种方式？如果服务器带宽更好，选择选项 B。否则选项 A 更简单——只需 `gcloud auth login`。