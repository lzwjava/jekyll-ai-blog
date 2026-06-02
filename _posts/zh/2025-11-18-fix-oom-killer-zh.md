---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复FineWeb脚本中的OOM Killer问题
translated: true
type: note
---

出现「Killed」提示且无 Python 错误回溯，意味着 Linux OOM（内存不足）终结进程。这种情况发生在 `data/fineweb/prepare.py` 脚本中，因为它试图通过类似 `open(...).read()` 的方式一次性将整个约 15 GB 的拼接文本文件 (`train_fineweb.txt`) 加载到内存中再进行标记化。

尽管 FineWeb-Edu 设计为流式处理（官方下载器使用 Hugging Face `datasets` 并按约 1 亿标记的分片逐块处理，无需全量加载内存），但 nanoGPT 的 fineweb 文件夹使用了自定义本地文件路径，这对大文件而言内存效率低下。

### 快速解决方案（任选其一）

1. **最佳推荐：使用官方流式 FineWeb-Edu 下载器替代本地文件**
   完全不要使用 nanoGPT 的 `data/fineweb/prepare.py`。
   使用 Karpathy 专为 FineWeb-Edu 100 亿标记（或更大规模）编写的新脚本：

   ```bash
   # 在 nanoGPT 根目录（或任意位置）执行
   wget https://raw.githubusercontent.com/karpathy/build-nanogpt/master/fineweb.py
   python fineweb.py
   ```

   该脚本通过 `datasets.load_dataset(..., streaming=True)` 和多进程流式下载并标记化 FineWeb-Edu sample-10BT（100 亿标记，原始数据约 15-20 GB）。它永远不会将完整数据集加载到内存中，并会在类似 `edu_fineweb10B/` 的文件夹中生成 nanoGPT 预期格式的 `.bin` 分片文件。
   该脚本可在 32-64 GB 内存的机器上正常运行（如果减少脚本中的 `num_proc_load_dataset` 和 `num_proc` 参数，甚至可在更小内存环境中运行）。

   如需处理完整 100B 或 1T 版本，只需将 `remote_name = "sample-10BT"` 改为 `"100BT"` 或所需版本即可。

2. **如需保留本地 10 个 parquet → txt 文件**
   修改 `data/fineweb/prepare.py` 使其分块处理文本而非全量加载：

   打开脚本并将 `with open(local_file, 'r', encoding='utf-8') as f: data = f.read()` 代码块替换为：

   ```python
   from tqdm import tqdm
   import tiktoken
   enc = tiktoken.get_encoding("gpt2")

   chunk_size = 1_000_000  # 每块字符数，可按需调整
   tokens = []
   with open(local_file, "r", encoding="utf-8") as f:
       while True:
           chunk = f.read(chunk_size)
           if not chunk:
               break
           tokens.extend(enc.encode_ordinary(chunk))  # 或 enc.encode(chunk)
           print(f"当前已标记化: {len(tokens)/1e6:.1f}M 个标记")
   tokens = np.array(tokens, dtype=np.uint16)
   ```

   这样即使处理 15 GB 文件也能将峰值内存控制在约 10-15 GB。

3. **硬件临时解决方案（非理想方案）**
   - 增加大量交换空间（例如 64-128 GB 交换文件）。开始交换后会极其缓慢，但可能完成处理。

     ```bash
     sudo fallocate -l 64G /swapfile
     sudo chmod 600 /swapfile
     sudo mkswap /swapfile
     sudo swapon /swapfile
     ```

   - 在内存 ≥64 GB 的机器/实例上运行（例如 AWS r6i.4xlarge 或更高配置）。

### 总结

直接运行 build-nanogpt 中的官方 `fineweb.py` 是最简洁的解决方案，也是目前处理 FineWeb 的通用方法。问题根源在于您拼接的 15 GB txt 文件，而非 FineWeb 本身。

[官方 FineWeb-Edu 下载脚本](https://raw.githubusercontent.com/karpathy/build-nanogpt/master/fineweb.py)
[FineWeb-Edu 数据集页面](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
