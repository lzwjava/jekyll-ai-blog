---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes Agent 通知挂钩设置
translated: true
type: note
---

已创建：

**脚本：** `/Users/lzwjava/.hermes/agent-hooks/on-agent-done.sh`

从标准输入读取钩子 JSON 负载，提取工作目录，并通过 `osascript` 发送 macOS 通知中心通知。通知显示为：

> **Hermes Agent — jekyll-ai-blog**
> 等待下一次输入

**已添加到 `config.yaml` 的配置：**

```yaml
hooks:
  post_llm_call:
    - command: "~/.hermes/agent-hooks/on-agent-done.sh"
      timeout: 5
hooks_auto_accept: true
```

钩子在启动时加载，因此需要重启 Hermes 才能生效（输入 `/exit` 后再启动）。之后，每次代理完成一个轮次时，你都会收到一条系统通知，显示当前工作目录的名称。

如需自定义通知（声音、消息等），请编辑脚本——`osascript` 行位于文件末尾附近。删除 `sound name "Glass"` 可静默通知，或使用 `"Basso"`、`"Funk"`、`"Ping"` 等来更换提示音。
