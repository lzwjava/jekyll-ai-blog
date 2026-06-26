---
audio: false
generated: true
image: false
lang: en
layout: post
title: HK Relay Upload to HuggingFace
translated: false
type: note
---

**Done!** 🎉

model.safetensors uploaded to HuggingFace in **11 min 39 sec** from HK.

```
Full pipeline completed:
  Mac → HK (SCP):       30 min   (475 MB, ~263 KB/s)
  HK → HuggingFace:     11 min   (498 MB, ~700 KB/s)
  Total:                ~42 min

Your model is live:
  https://huggingface.co/lzwjava/sec-edgar-gpt-124m
  Commit: d769c2a2887896bd98db2e8616734ffe31804fe9
```

**Cleanup:** You can now destroy the Aliyun HK ECS instance to stop paying:

```
# Via Aliyun console or CLI
aliyun ecs DeleteInstance --InstanceId <instance-id> --Force true
```

The HK relay trick worked well — China→HK tolerable (no stalls), HK→HuggingFace fast (~700 KB/s). Next time you need to upload to HF from China, this is the playbook.
