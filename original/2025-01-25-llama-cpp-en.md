---
audio: true
generated: false
image: false
lang: en
layout: post
title: Trying llama.cpp and Ollama
type: post
---

## llama.cpp

When attempting to run `llama.cpp` with a model, you might encounter an error like this:

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

This error occurs because you are running the `main` program. Running the `llama-cli` or `llama-server` programs located under `build/bin` should resolve the issue.

The `main` program was created on Aug 8 2023, which means it is not the current build.

Another solution is to install `llama.cpp` using Homebrew:

```bash
brew install llama.cpp
```

This ensures that you have a compatible version of the library.

### Serving the Model

```bash
/home/lzw/Projects/llama.cpp/build/bin/llama-server -m /home/lzw/Projects/llama.cpp/models/DeepSeek-R1-Distill-Qwen-14B-Q5_K_M.gguf --port 8000  --ctx-size 2048 --batch-size 512 --n-gpu-layers 49 --threads 8 --parallel 1
```

The parameters `--ctx-size 2048 --batch-size 512 --n-gpu-layers 49 --threads 8 --parallel 1` are important. They will boost the speed.


### LLM Farm

It's a great iOS app. In the settings, there are around 20 models. When importing a GGUF model by ourselves, which are downloaded from Hugging Face, it may lead to a crash.

### Benefits

Self-hosting these LLM models allows you to run them locally without needing network access. For example, when downloading large files that congest the network, running a local model can be beneficial.

### Resources

*   [Hugging Face GGML Models](https://huggingface.co/ggml-org?sort_models=downloads#models)
*   [llama.cpp GitHub Repository](https://github.com/ggerganov/llama.cpp)
*   [ggml GitHub Repository](https://github.com/ggerganov/ggml)
*   [Ollama](https://ollama.com)
*   [Ollamac](https://github.com/kevinhermawan/Ollamac)

---

## Using Ollama

```bash
% ollama list
NAME                   ID              SIZE      MODIFIED
deepseek-coder:6.7b    ce298d984115    3.8 GB    14 hours ago
mistral:7b             f974a74358d6    4.1 GB    15 hours ago
```

```bash
ollama remove model
```

It's a great tool to use. There are some bugs in Ollamac. For example, when it receives a response from the local API, several text boxes in the app update.

However, in Linux, Ollama runs as a system service. Here is the service configuration file:

`/etc/systemd/system/ollama.service`:

```bash
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=/home/lzw/.local/bin:/home/lzw/bin:/usr/local/cuda-12.2/bin:/home/lzw/.local/share/gem/ruby/3.0.0/bin:/home/lzw/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin"

[Install]
WantedBy=default.target
```

Use the following commands to control the Ollama service:

```bash
sudo systemctl stop ollama.service
sudo systemctl disable ollama.service
sudo systemctl status ollama.service
```
