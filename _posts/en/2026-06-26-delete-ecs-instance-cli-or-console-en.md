---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Delete ECS Instance: CLI or Console?"
translated: false
type: note
---

Aliyun CLI is installed but not configured — no credentials. You have two options:

**Option 1: Configure CLI (need your AccessKey)**

```
aliyun configure
# Enter: AccessKey ID, AccessKey Secret, Region: cn-hongkong
# Then: aliyun ecs DeleteInstance --InstanceId i-j6civepr8vf1085n7x0u --Force true
```

**Option 2: Web console (faster)**
Go to <https://ecs.console.aliyun.com> → find instance `i-j6civepr8vf1085n7x0u` in Hong Kong → Delete

Want to configure the CLI, or just delete it from the web console?
