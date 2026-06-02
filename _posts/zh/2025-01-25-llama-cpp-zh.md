---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 尝试 llama.cpp
translated: true
type: post
---

## llama.cpp

尝试使用模型运行 `llama.cpp` 时，可能会遇到类似以下的错误：

```bash
% ./main -m models/7B/Phi-3-mini-4k-instruct-q4.gguf
main: build = 964 (f3c3b4b)
main: seed  = 1737736417
llama.cpp: loading model from models/7B/Phi-3-mini-4k-instruct-q4.gguf
error loading model: unknown (magic, version) combination: 46554747, 00000003; is this really a GGML file?
llama_load_model_from_file: failed to load model
llama_init_from_gpt_params: error: failed to load model 'models/7B/Phi-3-mini-4k-instruct-q4.gguf'
main: error: unable to load model
```

这个错误是因为你在运行 `main` 程序。运行位于 `build/bin` 下的 `llama-cli` 或 `llama-server` 程序应该可以解决这个问题。

`main` 程序是在 2023 年 8 月 8 日创建的，这意味着它不是当前的构建版本。

另一种解决方案是使用 Homebrew 安装 `llama.cpp`：

```bash
brew install llama.cpp
```

这可以确保你有一个兼容的库版本。

## 服务模型

```bash
/home/lzw/Projects/llama.cpp/build/bin/llama-server -m /home/lzw/Projects/llama.cpp/models/DeepSeek-R1-Distill-Qwen-14B-Q5_K_M.gguf --port 8000  --ctx-size 2048 --batch-size 512 --n-gpu-layers 49 --threads 8 --parallel 1
```

参数 `--ctx-size 2048 --batch-size 512 --n-gpu-layers 49 --threads 8 --parallel 1` 非常重要。它们可以提高速度。

## LLM Farm

这是一个非常棒的 iOS 应用。在设置中有大约 20 个模型。当我们自己导入从 Hugging Face 下载的 GGUF 模型时，可能会导致崩溃。

## 好处

自托管这些 LLM 模型可以让你在本地运行它们，而不需要网络访问。例如，当下载大文件时网络拥堵，运行本地模型会有所帮助。

## 资源

*   [Hugging Face GGML Models](https://huggingface.co/ggml-org?sort_models=downloads#models)
*   [llama.cpp GitHub Repository](https://github.com/ggerganov/llama.cpp)
*   [ggml GitHub Repository](https://github.com/ggerganov/ggml)
*   [Ollama](https://ollama.com)
*   [Ollamac](https://github.com/kevinhermawan/Ollamac)
