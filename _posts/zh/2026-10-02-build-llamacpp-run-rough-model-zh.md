---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建llama.cpp，运行粗略模型
translated: true
type: note
---

远程机器上有llama.cpp的源代码，但**尚未编译**——没有`build`目录或可执行文件。旧的llama-server（PID 7946）一定来自其他来源。

你需要先编译它：

```bash
ssh lzw@192.168.1.34
cd ~/projects/llama.cpp
cmake -B build
cmake --build build --config Release -j $(nproc)
```

编译需要几分钟时间。完成后，运行：

```bash
./build/bin/llama-server -m models/Qwen3.8-27B-UD-IQ1_M.gguf --port 8080 --host 0.0.0.0
```

考虑到你的Tesla M40拥有**11.5GB显存**，而该模型仅为**6.3GB**（Qwen 3.8 27B的IQ1_M量化版本），应该可以容纳。不过IQ1_M是极低比特量化——质量可能非常粗糙。