---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang 在 CUDA 图捕获期间发生段错误
translated: true
type: note
---

问题：我的 SGLang 服务器在 CUDA 图捕获期间（FlashInfer 后端，Triton 编译）出现段错误，如何修复？

答案：

段错误发生在 Triton JIT 编译过程中，由 FlashInfer 的 `call_begin_forward` 在 CUDA 图捕获时触发。崩溃链路如下：

```
cuda_graph_runner.capture_one_batch_size
  → flashinfer_backend.init_forward_metadata_capture_cuda_graph
    → update_single_wrapper → call_begin_forward
      → triton jit.run → _do_compile → ast_to_ttir   ← 此处段错误
```

这不是 OOM 问题（你同时存在另一个真实的 OOM 问题——见下文）。该段错误是已知的 **FlashInfer + Triton + CUDA 图捕获不兼容**问题，通常由以下原因引起：Triton 版本与 SGLang 期望的 FlashInfer 内核不匹配、过时的 Triton 自动调优/JIT 缓存，或 FlashInfer 的图捕获路径触发了 Triton 代码生成错误。错误在构建 IR 时发生在 `code_generator.__init__` 内部（而非运行时），指向编译器而非你的模型。

以下是按修复难度排序的解决方案：

**1. 禁用 CUDA 图捕获（最快的确认方法 + 临时方案）：**

```bash
python -m sglang.launch_server --model <MODEL> --disable-cuda-graph
```

如果服务器正常启动，则确认图捕获路径是罪魁祸首。虽然会损失图回放的吞吐量，但服务器可以正常运行。

**2. 切换注意力后端，不使用 FlashInfer：**

```bash
python -m sglang.launch_server --model <MODEL> --attention-backend triton
# 或
--attention-backend torch_native
```

FlashInfer 的图捕获路径会触发有问题的 Triton 编译。纯 Triton 后端完全绕过了 `flashinfer_backend.py`。

**3. 清除 Triton 缓存（过时的缓存会直接导致此类段错误）：**

```bash
rm -rf ~/.triton/cache
```

**4. 对齐 FlashInfer / Triton / SGLang 版本。** 如果段错误发生在 `triton/compiler/code_generator.py` 内部，几乎总是意味着已安装的 `triton` 版本与你的 `flashinfer` 轮子所依赖的版本不一致：

```bash
pip show sglang flashinfer-python triton torch | grep -E 'Name|Version'
```

然后对照 SGLang 版本需求文件中锁定的版本进行匹配，而不是依赖 pip 自动解析的版本。

**另外——你此次运行时确实存在内存问题。** 查看追踪信息：

```
Load weight end ... avail mem=8.11 GB
KV Cache allocated ... K 3.28 GB + V 3.28 GB
Memory pool end. avail mem=0.97 GB
Capture cuda graph begin ... avail mem=0.39 GB
```

一个 3.09 GB 的 safetensors 模型 `Qwen2ForCausalLM`（约 1.5B，bf16 精度）运行在你的 RTX 4070 12 GB 上。到图捕获开始时，可用显存仅剩 **0.39 GB**，而捕获过程需要 FlashInfer 封装器的额外空间。即使修复了 Triton 崩溃，图捕获仍可能因 OOM 失败。建议收紧参数：

```bash
--mem-fraction-static 0.80 \
--max-running-requests 8 \
--cuda-graph-max-bs 4   # 你目前仅捕获 bs [1,2,4,8]
```

另外注意 `Load weight end. elapsed=945.52 s`——加载一个 3 GB 的检查点花费了 15 分钟以上，说明权重数据通过慢速存储或交换分区传输；建议检查 `dmesg` 中是否有 OOM 杀手或磁盘抖动，这本身也可能表现为段错误。

推荐操作顺序：`rm -rf ~/.triton/cache` → 使用 `--attention-backend triton --disable-cuda-graph` 重新启动。如果运行稳定，则重新启用图捕获；如果再次崩溃，则是步骤 4 中的版本不匹配问题。

如果你能提供 `pip show sglang flashinfer-python triton torch` 的输出以及确切的启动命令，我可以帮你确定具体的版本冲突。

参考文档：

- [SGLang 服务器参数](https://docs.sglang.ai/backend/server_arguments.html)
- [SGLang 问题 — FlashInfer CUDA 图捕获段错误](https://github.com/sgl-project/sglang/issues)
- [FlashInfer 仓库](https://github.com/flashinfer-ai/flashinfer)
