---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GGUF转换流水线
translated: true
type: note
---

问题：如何使用转换脚本将我的模型转换为 GGUF 格式？

答案：

单独的 `gguf` pip 包无法完成转换——它只是一个写入库。你需要从 llama.cpp 仓库获取 `convert_hf_to_gguf.py`，然后使用 `llama-quantize` 二进制文件进行量化。

完整流程如下：

```bash
# 在远程服务器上（213.173.x.x）
cd /workspace

# 1. 获取 llama.cpp（转换脚本位于此处，而非 pip gguf 中）
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
pip3 install -r requirements.txt   # numpy、gguf、sentencepiece、transformers 等

# 2. 将 HF 检查点转换为 GGUF（先转为 fp16，无损）
python3 convert_hf_to_gguf.py /workspace/model \
  --outfile /workspace/model-f16.gguf \
  --outtype f16

# 3. 构建量化器
cmake -B build && cmake --build build --config Release -j$(nproc)

# 4. 将 fp16 量化为 Q4_K_M（最佳大小/质量默认值）
./build/bin/llama-quantize \
  /workspace/model-f16.gguf \
  /workspace/model-Q4_K_M.gguf \
  Q4_K_M
```

针对你的情况，有几点需要注意：

**`--outtype` 选项：** `f16`（16 位，完整质量，体积大）、`bf16`、`q8_0`（接近无损，速度快）或 `f32`。始终先转换为 `f16`/`bf16`，然后单独量化——直接通过脚本转换为低位类型会跳过更好的 k-quant imatrix 路径。

**值得了解的量化类型：** `Q4_K_M`（约 4.5 bpw，标准）、`Q5_K_M`（质量更好）、`Q6_K`（接近 fp16）、`Q8_0`（基本无损）。对于你在本地测试的“专业”模型，如果磁盘空间允许，`Q5_K_M` 或 `Q6_K` 是一个不错的折中选择。

**如果是 MoE 或更新的架构**（mimo-v2.5——检查配置文件），`convert_hf_to_gguf.py` 必须明确支持该架构。如果你遇到 `Model architecture 'XXX' not supported` 错误，说明转换器还不支持它——你需要一个在 `convert_hf_to_gguf.py` 中有对应 `@Model.register("XXX")` 条目的 llama.cpp 版本，否则它根本无法转换为 GGUF。

**然后运行它**，使用你已经安装的 llama-cpp-python：

```python
from llama_cpp import Llama
llm = Llama(model_path="/workspace/model-Q4_K_M.gguf", n_gpu_layers=-1, n_ctx=4096)
print(llm("Hello", max_tokens=64)["choices"][0]["text"])
```

有一点需要注意：你截图中的进度条显示下载仍在 8%（86.7K/1M，大约还剩 1 小时 48 分钟）。在转换前让它完成——部分检查点会因 safetensors/shard 错误而失败。

`/workspace/model/config.json` 中的实际架构是什么？这将决定 GGUF 转换是否能在 mimo-v2.5 上正常工作。
