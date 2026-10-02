---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 下载并运行Llama服务器
translated: true
type: note
---

```bash
cd ~/projects/llama.cpp && wget -O models/Qwen3.8-27B-UD-IQ1_M.gguf https://huggingface.co/unsloth/Qwen3.8-27B-GGUF/resolve/main/Qwen3.8-27B-UD-IQ1_M.gguf
```

然后运行：

```bash
./build/bin/llama-server -m models/Qwen3.8-27B-UD-IQ1_M.gguf --port 8080
```

在浏览器中打开 `http://localhost:8080`。

注意：这是一个 **27B 模型，采用 IQ1（1 位量化）**，因此体积较小，但质量可能受到影响。如果你有足够的显存（约 16GB），使用 Q4 或 Q3 版本会获得更好的效果。需要我为这个模型找一个更高质量的 GGUF 吗？
