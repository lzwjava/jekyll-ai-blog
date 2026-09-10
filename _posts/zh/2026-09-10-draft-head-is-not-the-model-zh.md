---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 草案负责人并非模型
translated: true
type: note
---

构建已完成。但有一个硬性阻塞点需要明确说明，且我已通过实际测试验证：

## `Qwen3.8-27B-Uncensored-draft-Q8_0.gguf` **并非**模型本体

而是**MTP草稿头**（3.2 GB），属于27B目标模型的推测解码辅助组件。验证如下：

```
$ ./build/bin/llama-server -m models/Qwen3.8-27B-Uncensored-draft-Q8_0.gguf
loading model 'models/Qwen3.8-27B-Uncensored-draft-Q8_0.gguf'
timeout: the monitored command dumped core     <-- 无transformer模块可运行
```

其元数据显示 `qwen35.block_count = 65`，但文件仅包含**18个张量**，全部为 `blk.64.*` 及 `blk.64.nextn.*`：

```
qwen35.nextn_predict_layers = 1
  blk.64.attn_q.weight          Q8_0  [5120, 12288]
  blk.64.nextn.eh_proj.weight   Q8_0  [10240, 5120]   <- MTP融合投影
  blk.64.nextn.enorm.weight     F32   [5120]
  blk.64.nextn.hnorm.weight     F32   [5120]
  output.weight / token_embd.weight ...
```

其中缺失了第0至63区块。单独使用时无法生成任何token。该文件源自**`JonathanColetti/Qwen3.8-27B-Uncensored-GGUF`**，真正的模型本体就在同一仓库中。

## 构建结果（已完成）

`/mnt/data/llama.cpp/build/bin/llama-server` — CUDA 13.2，sm_89（Ada架构），耗时2分44秒。

## 后续所需操作

以下两种方案均来自同一仓库。您的12GB RTX 4070（约9.4GB可用）存在限制，`-ngl auto --fit on` 可自动处理显存分配。

**方案A - 融合版（更简洁，MTP头内联，容量16.8 GB）：**

```bash
hf download JonathanColetti/Qwen3.8-27B-Uncensored-GGUF \
  Qwen3.8-27B-Uncensored-Q4_K_M.gguf --local-dir /mnt/data/llama.cpp/models

./build/bin/llama-server \
  -m models/Qwen3.8-27B-Uncensored-Q4_K_M.gguf \
  --spec-type draft-mtp --spec-draft-n-max 2 \
  -c 32768 -ngl auto --fit on --host 127.0.0.1 --port 8080
```

**方案B - 复用现有草稿文件（16.5 + 3.2 GB）：**

```bash
hf download JonathanColetti/Qwen3.8-27B-Uncensored-GGUF \
  Qwen3.8-27B-Uncensored-noMTP-Q4_K_M.gguf --local-dir /mnt/data/llama.cpp/models

./build/bin/llama-server \
  -m models/Qwen3.8-27B-Uncensored-noMTP-Q4_K_M.gguf \
  -md models/Qwen3.8-27B-Uncensored-draft-Q8_0.gguf \
  --spec-type draft-mtp --spec-draft-n-max 2 \
  -c 32768 -ngl auto --fit on --host 127.0.0.1 --port 8080
```

随后在浏览器中打开 `http://127.0.0.1:8080` 即可访问Web界面。

注意：此构建版本已关闭 `LLAMA_CURL=OFF`（您的系统缺少libcurl开发头文件），因此服务器端无法使用 `-hf` 参数——请使用上述命令中的 `hf` CLI工具进行下载。

是否需要我现在开始下载方案A的16.8GB文件？请指示，我将立即获取并启动服务器。
