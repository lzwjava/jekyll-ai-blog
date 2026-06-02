---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-2 分词后的 FineWeb 分片脚本
translated: true
type: note
---

新脚本位于 `scripts/extract/tokenize_fineweb_gpt3.py`。原始的 `extract_fineweb_gpt3.py` 保持不变。

**功能说明**
- 通过 `pq.iter_batches` 流式处理 parquet 分片（内存占用与修复后的提取脚本一致——平坦驻留集）。
- 使用 GPT-2 BPE 分词器，通过 `multiprocessing.Pool` 进行分词（默认使用 `cpu_count//2` 个工作进程，块大小为 16）。
- 每个文档以 `<|endoftext|>` 标记 ID（50256）作为整数前缀，而非纯文本形式——修复了旧 `.txt` 流水线中分隔符被重新按字符分词的问题。
- 打包为 1 亿 token 的 uint16 分片，通过 `np.save` 保存为 `edufineweb_val_000000.npy`（第一个分片）和 `edufineweb_train_NNNNNN.npy`（其余分片）——与 `nanoGPT/data/fineweb/prepare_fineweb.py` 生成的精确文件名模式一致，因此训练加载器无需修改即可使用。

**输出**
- 默认输出目录：`/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B/`
- 可通过 `--input-dir`、`--output-dir`、`--shard-size`、`--nprocs` 参数覆盖。

**运行方式**
```
python3.11 scripts/extract/tokenize_fineweb_gpt3.py
```

**注意事项**
- 不支持运行中途恢复——若进程中断，将从第 0 个分片重新开始（会发出警告并覆盖）。如需断点续传功能，请告知我，我将添加 `--start-doc` 偏移量或分片跳过逻辑。
- 分词为 CPU 密集型任务；在此 62 GB 内存主机上使用 `os.cpu_count()//2` 个工作进程，预计端到端速度比纯文本文件路径快一个数量级（且无需 TB 级中间磁盘占用）。
