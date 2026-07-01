---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SPGISpeech Whisper微调流水线
translated: true
type: note
---

以下是构建内容的完整分解及原因说明。

---

## SPGISpeech Whisper 微调管道

### 1. 数据集：SPGISpeech S 配置

SPGISpeech 是由 Kensho Technologies 制作的金融财报电话会议转录语料库。**S（小型）** 配置是一个包含 155,718 个话语的干净子集：

| 拆分 | 分片数 | 样本数 | 大小 |
| --- | --- | --- | --- |
| 训练集 | 6 个 parquet 文件 | 77,073 | ~22 GB |
| 验证集 | 3 个 parquet 文件 | 39,304 | ~11 GB |
| 测试集 | 3 个 parquet 文件 | 39,341 | ~11 GB |

**数据格式** — 每个 parquet 文件约有 12,800 行，分布在约 13 个行组中。模式如下：

```
wav_filename: string          # 哈希/名称.wav
audio: struct<bytes: binary, path: string>  # 原始 WAV 字节内嵌
wav_filesize: int32           # 字节数
transcript: string            # 英文文本
```

**音频属性** — 通过从 `bytes` 字段读取 WAV 头部提取：

- 采样率：16 kHz（通过 WAV 头部字节 `\x80\x3e` 确认，即 16000 小端序）
- 位深：16-bit PCM
- 声道：1（单声道）
- 时长：2-30 秒（财报电话会议话语，通常为 5-15 秒）
- 数据大小：约 350 KB 每秒音频（16-bit × 16000 Hz = 32 KB/s，WAV 中 PCM 无压缩 = ~32 KB/s × 时长）

**为什么不从磁盘文件下载？** — 该数据集将音频作为 Arrow 结构体列中的 WAV 字节提供。这实际上对训练*更有利*：无需单独的文件 I/O，无需遍历文件系统，音频在单个二进制 blob 中随 parquet 行一起传输。HuggingFace Hub 的 `snapshot_download` 配合 `allow_patterns='S/*'` 只拉取了 S 配置（总计 ~42 GB）。

### 2. 数据管道架构

核心设计问题：**如何在不将 42 GB 加载到 RAM 且不依赖 HF `datasets` 库中损坏的 torchcodec 依赖的情况下，迭代 77K 个音频样本。**

**解决方案：一个由 pyarrow 行组读取器支撑的自定义 `SPGISpeechDataset`（PyTorch `Dataset` 子类）。**

```
SPGISpeechDataset
├── index: [(shard_idx, row_group, offset), ...]  → 77,073 条目
├── _load_row_group(si, rg): 加载+解码 1 个行组（约 1000 样本），缓存
├── __getitem__(idx): 解析索引 → 从缓存行组读取 → 提取 WAV → soundfile → 特征提取器
└── clear_cache(): 内存压力时进行垃圾回收
```

关键细节：

- 每个 parquet 文件有多个**行组**（约 13 个，每组约 1000 行）。`read_row_group(0)` 读取 1000 行，而非整个 12K 行文件。
- 缓存以解码形式（numpy 数组 + 字符串）保存最近访问的行组。在一个 77K 样本的 epoch 中，缓存循环遍历所有约 78 个行组（6 个分片 × 13 个行组）。这意味着每个 epoch 约 78 次完整的行组读取 → 同一个文件每个 epoch 被读取 13 次。我可以用合适的 LRU 进行优化，但对于一次性训练运行来说可以接受——每个 epoch 的总 I/O 约为 78 × 1000 × 100KB = ~7.8 GB，主要由计算主导。
- `dataloader_num_workers=0` 是必需的，因为数据集使用共享状态（缓存字典）。多进程数据加载器会 pickle 缓存，从而破坏目的。

**为什么不用 HF `datasets`？** — `datasets` 库的 `Audio` 特征类型依赖于 `torchcodec.decoders.AudioDecoder`，该模块在 torchcodec 版本中引入后又被移除/重命名，导致无法用于可靠运行。自定义 pyarrow 方法更干净，除了 `soundfile` + `pyarrow` 外没有外部依赖。

### 3. Whisper 模型及微调设置

**模型选择：`openai/whisper-small`（244M 参数）**

| 模型 | 参数 | 显存（batch 16） | 估计每 epoch 时间 | 备注 |
| --- | --- | --- | --- | --- |
| tiny | 37M | ~2 GB | ~2h | 快速但 WER 一般 |
| **small** | **244M** | **~7 GB** | **~10h** | **最佳精度/速度权衡** |
| medium | 769M | ~12 GB | ~24h | 12GB 显卡可用 batch 8 |
| large-v3 | 1.5B | >12 GB | 不适用 | 无法在 RTX 4070 上运行 |

**为什么选 small？** — 它是 12GB 显存的甜点区。medium 需要 batch 8，且耗时 2-3 倍。对于金融转录数据，whisper-small 已经具有很强的英文 ASR 能力。微调主要使模型适应金融术语领域——不是学习新的语音，而是词汇分布偏移。

**训练配置（`Seq2SeqTrainingArguments`）：**

```
per_device_train_batch_size: 16
gradient_accumulation_steps: 2
→ 有效 batch size: 32

fp16: true                    # 半精度 = 2 倍吞吐量，精度损失极小
gradient_checkpointing: true  # 在反向传播中重新计算激活而非存储
                              # 速度慢约 1.3 倍，但节省约 60% 显存 → 允许 batch 16 而非 6

learning_rate: 1e-5           # Whisper 微调的标准学习率（前 100 步 warmup）
num_train_epochs: 3           # 领域适应足够；更多 epoch 可能对 77K 样本过拟合
predict_with_generate: true   # 使用实际自回归解码进行 WER 评估（而非教师强制）
generation_max_length: 225    # 最多 225 个 token（约 30 秒语音，Whisper 速率 2.5 tok/s）
```

**冻结编码器选项**（`--freeze-encoder`）：适用于快速实验。Whisper 编码器在英文音频上已经很强。冻结它意味着只微调解码器交叉注意力和语言模型头部 → 速度快 2 倍，精度略低。

### 4. 分词器与解码策略

```
processor.tokenizer.set_prefix_tokens("en")
model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")
model.config.suppress_tokens = []
```

这一点至关重要：Whisper 默认是多语言的。如果不强制 `language="en"`，模型会在语言 ID token 上浪费能力。`forced_decoder_ids` 将第一个解码器 token 固定为 `<|en|><|transcribe|><|notimestamps|>`，使其严格进行英文转录且不带时间戳——这正是 SPGISpeech 所需要的（干净的转录，无对齐）。

数据整理器处理 `labels` 张量：

1. 将所有标签序列用 `pad_token_id` 填充到相同长度
2. 将填充位置替换为 `-100`（PyTorch 的 CrossEntropyLoss 忽略这些位置）
3. 去除开头的 `bos_token_id`（Whisper 内部生成会预先添加）

### 5. 训练动态

**对于 77K 样本，有效 batch 32：**

```
每 epoch 步数：77,073 / 32 = ~2,409
总步数（3 epoch）：~7,226
每一步耗时（whisper-small, batch 16, fp16）：~12-18s
总计时长：7,226 × 15s = ~108,000s = ~30h
```

评估循环（`predict_with_generate=True`）每 500 步增加约 2 分钟（自回归生成 500 个完整转录）。3 个 epoch 中有 14 个评估检查点，评估开销约 28 分钟。

**未微调的 WER 基线：**

- whisper-small 在干净英文上：约 8-9% WER（LibriSpeech clean）
- SPGISpeech 是金融财报电话会议——口音/术语更重——基线约 15-20%
- 3 个 epoch 后：目标约 8-12% WER

### 6. 代码结构

```
/mnt/data/zz/spgispeech/
├── data/S/                                    # 12 个 parquet 文件，42 GB
│   ├── train-00000-of-00006.parquet (~3.7 GB) # 6 个分片 × ~12,846 行
│   ├── ...
│   ├── validation-0000*-of-00003.parquet      # 3 个分片 × ~13,101 行
│   └── test-0000*-of-00003.parquet            # 3 个分片 × ~13,114 行
├── .venv/                                     # 虚拟环境（Python 3.12, torch 2.6, CUDA 12.4）
├── explore.py                                 # 数据探索辅助工具（已加入 git）
├── train_whisper.py                           # 主要训练脚本（14.7 KB）
├── train_cmd.sh                               # 便捷启动脚本
├── train_log.json                             # 运行日志（追加）
└── checkpoints/                               # 模型检查点 + tensorboard 日志
```

### 7. 如何监控

```
# 训练进度
tail -f train_small.log

# 损失曲线
tensorboard --logdir /mnt/data/zz/spgispeech/checkpoints --bind_all

# GPU 利用率
watch -n 2 nvidia-smi

# 训练后：测试 WER 记录在 train_log.json 中
cat train_log.json | python3 -m json.tool
```
