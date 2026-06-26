---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HK Relay 上传至 HuggingFace
translated: true
type: note
---

**完成！** 🎉

model.safetensors 已上传至 HuggingFace，耗时 **11 分 39 秒**（从香港出发）。

```
完整流水线：
  Mac → 香港 (SCP)：       30 分钟   (475 MB, ~263 KB/s)
  香港 → HuggingFace：     11 分钟   (498 MB, ~700 KB/s)
  总计：                  ~42 分钟

你的模型已上线：
  https://huggingface.co/lzwjava/sec-edgar-gpt-124m
  提交：d769c2a2887896bd98db2e8616734ffe31804fe9
```

**清理：** 你现在可以销毁阿里云香港 ECS 实例以停止计费：

```
# 通过阿里云控制台或 CLI
aliyun ecs DeleteInstance --InstanceId <实例ID> --Force true
```

香港中继技巧效果不错——中国→香港可接受（无卡顿），香港→HuggingFace 速度快（~700 KB/s）。下次你需要从中国上传到 HF 时，这就是操作手册。