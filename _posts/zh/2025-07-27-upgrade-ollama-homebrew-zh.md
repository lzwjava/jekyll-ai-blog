---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 Homebrew 升级 Ollama
translated: true
type: note
---

要在 macOS 上使用 Homebrew 将 Ollama 升级至最新版本（截至 2025 年 7 月当前版本为 v0.10.0），请按以下步骤操作：

1. 更新 Homebrew 的配方库以确保其知晓最新可用版本：
   ```
   brew update
   ```

2. 单独升级 Ollama：
   ```
   brew upgrade ollama
   ```

3. 通过以下命令验证升级是否成功：
   ```
   ollama --version
   ```

若您将 Ollama 作为后台服务运行，请在升级后重启服务：
```
brew services restart ollama
```

若采用手动运行方式，请先终止现有进程，再用您偏好的命令重新启动（例如根据安装输出提示中的说明）：
```
OLLAMA_FLASH_ATTENTION="1" OLLAMA_KV_CACHE_TYPE="q8_0" /opt/homebrew/opt/ollama/bin/ollama serve
```

除上述标准流程外，无需其他特殊升级操作。

[Ollama 版本发布](https://github.com/ollama/ollama/releases)
