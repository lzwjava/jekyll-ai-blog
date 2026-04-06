---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复OpenClaw的Gemma服务器问题
translated: true
type: note
---

## 问题经过

OpenClaw在`openclaw.json`中配置了指向`http://192.168.1.36:8081/v1`的`llama-server`提供程序，使用模型`gemma-4-26B-A4B-it-UD-IQ3_S.gguf`。当您通过OpenClaw发送“hi”时，由于两个问题导致失败：

### 问题一：llama-server未运行

进程未启动。旧的`~/llama.sh`脚本在端口8000上启动的是不同模型（DeepSeek-R1-Distill-Llama-8B），而非端口8081上的Gemma。因此虽然配置已更新为切换至Gemma，但实际服务器并未启动。

### 问题二：Gemma 4的思考模式

即使启动llama-server后，Gemma 4内置“思考”模式。默认情况下（`--reasoning auto`），llama-server根据模型模板检测并将输出拆分为：
- `message.reasoning_content` —— 思考过程/思维链
- `message.content` —— 最终答案

采用默认`auto`设置时，`content`字段返回为空，所有文本都进入`reasoning_content`。而OpenClaw读取`content`字段，因此看起来模型未返回任何内容。

使用`--reasoning-format none`时，思考标记会以原始`<|channel>thought`标记形式泄露到`content`中——仍然存在问题。

### 解决方案

使用`--reasoning off`启动llama-server，完全禁用思考功能：

```bash
nohup /home/lzw/projects/llama.cpp/build/bin/llama-server \
  -m /home/lzw/projects/llama.cpp/models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  --port 8081 -c 32768 --reasoning off \
  >> /home/lzw/llama-server.log 2>&1 &
```

这将在`content`中生成干净的响应，不含思考痕迹。

### 注意事项

- 服务器重启后无法保持运行。您可能需要更新`~/llama.sh`或创建systemd服务以实现持久化。
- `--reasoning off`完全禁用思维链功能，可能会降低复杂推理任务的质量。如果希望保留思考功能同时确保OpenClaw兼容性，替代方案是在`openclaw.json`中将模型配置为`"reasoning": true`，使OpenClaw读取`reasoning_content`字段，然后使用`--reasoning-format deepseek`。
- 上下文窗口设置为32K（`-c 32768`），与openclaw.json配置匹配。该模型原生训练上下文为262K，但26B参数的量化IQ3_S模型需要大量内存才能支持更大的上下文。