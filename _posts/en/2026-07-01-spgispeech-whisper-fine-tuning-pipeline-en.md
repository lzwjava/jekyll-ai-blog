---
audio: false
generated: true
image: false
lang: en
layout: post
title: SPGISpeech Whisper Fine-Tuning Pipeline
translated: false
type: note
---

Here's the full breakdown of what was built and why.

---

## SPGISpeech Whisper Fine-Tuning Pipeline

### 1. Dataset: SPGISpeech S Config

SPGISpeech is a corpus of financial earnings call transcripts produced by Kensho Technologies. The **S (small)** config is a clean 155,718 utterance subset:

| Split | Shards | Samples | Size |
|---|---|---|---|
| train | 6 parquet files | 77,073 | ~22 GB |
| validation | 3 parquet files | 39,304 | ~11 GB |
| test | 3 parquet files | 39,341 | ~11 GB |

**Data format** — Each parquet file has ~12,800 rows across ~13 row groups. Schema:

```
wav_filename: string          # hash/name.wav
audio: struct<bytes: binary, path: string>  # raw WAV bytes embedded inline
wav_filesize: int32           # bytes
transcript: string            # English text
```

**Audio properties** — Extracted by reading the WAV header from the `bytes` field:
- Sample rate: 16 kHz (confirmed via WAV header bytes `\x80\x3e` = 16000 LE)
- Bit depth: 16-bit PCM
- Channels: 1 (mono)
- Duration: 2-30 seconds (earnings call utterances, typically 5-15s)
- Data size: ~350 KB per second of audio (16-bit × 16000 Hz = 32 KB/s, compressed in WAV with PCM no compression = ~32 KB/s × duration)

**Why not download from disk files?** — The dataset ships audio as WAV bytes inside Arrow struct columns. This is actually *better* for training: no separate file I/O, no file-system walk, the audio travels with the parquet row in a single binary blob. The HuggingFace Hub `snapshot_download` with `allow_patterns='S/*'` pulled only the S config (~42 GB total).

### 2. The Data Pipeline Architecture

The core design problem: **how to iterate 77K audio samples without loading 42 GB into RAM, and without the HF `datasets` library's broken torchcodec dependency.**

**Solution: a custom `SPGISpeechDataset` (PyTorch `Dataset` subclass) backed by pyarrow's row-group reader.**

```
SPGISpeechDataset
├── index: [(shard_idx, row_group, offset), ...]  → 77,073 entries
├── _load_row_group(si, rg): load+decode 1 RG (~1000 samples), cache it
├── __getitem__(idx): resolve index → read from cached RG → extract WAV → soundfile → feature extractor
└── clear_cache(): GC when memory pressure
```

Key details:
- Each parquet file has multiple **row groups** (~13, each ~1000 rows). `read_row_group(0)` reads 1000 rows, not the entire 12K-row file.
- The cache holds the most recently accessed row group in decoded form (numpy arrays + strings). On a 77K-epoch, the cache cycles through all ~78 row groups (6 shards × 13 RG each). This means ~78 full RG reads per epoch → the same file gets read 13 times per epoch. I could optimize with a proper LRU, but for a one-off training run it's fine — total I/O is ~78 × 1000 × 100KB = ~7.8 GB read per epoch, dominated by compute anyway.
- `dataloader_num_workers=0` is required because the dataset uses shared state (the cache dict). Multi-process dataloaders would pickle the cache, defeating the purpose.

**Why not HF `datasets`?** — The `datasets` library's `Audio` feature type depends on `torchcodec.decoders.AudioDecoder`, which was introduced and then removed/renamed across torchcodec versions, making it a no-go for reliable runs. The custom pyarrow approach is cleaner and has zero external dependencies besides `soundfile` + `pyarrow`.

### 3. Whisper Model & Fine-Tuning Setup

**Model choice: `openai/whisper-small` (244M params)**

| Model | Params | VRAM (batch 16) | Est time/epoch | Notes |
|---|---|---|---|---|
| tiny | 37M | ~2 GB | ~2h | Fast but mediocre WER |
| **small** | **244M** | **~7 GB** | **~10h** | **Best accuracy/speed tradeoff** |
| medium | 769M | ~12 GB | ~24h | Fits on 12GB with batch 8 |
| large-v3 | 1.5B | >12 GB | N/A | Won't fit on RTX 4070 |

**Why small?** — It's the sweet spot for 12GB VRAM. medium would need batch 8 and would take 2-3x longer. For financial transcript data, whisper-small already has strong English ASR. The fine-tuning primarily adapts the model to the financial jargon domain — not learning new phonetics, just vocabulary distribution shift.

**Training configuration (the `Seq2SeqTrainingArguments`):**

```
per_device_train_batch_size: 16
gradient_accumulation_steps: 2
→ effective batch size: 32

fp16: true                    # half precision = 2x throughput, minimal accuracy loss
gradient_checkpointing: true  # recompute activations in backward pass instead of storing them
                              # ~1.3x slower but saves ~60% VRAM → allows batch 16 vs 6

learning_rate: 1e-5           # standard for fine-tuning Whisper (warmup first 100 steps)
num_train_epochs: 3           # enough for domain adaptation; more risks overfitting 77K samples
predict_with_generate: true   # use actual autoregressive decoding for WER eval (not teacher-forcing)
generation_max_length: 225    # max 225 tokens (~30s of speech at 2.5 tok/s Whisper rate)
```

**Freeze encoder option** (`--freeze-encoder`): Useful for rapid experiments. The Whisper encoder is already strong on English audio. Freezing it means only the decoder cross-attention and language-model head get fine-tuned → 2x faster, slightly lower accuracy.

### 4. Tokenizer & Decoding Strategy

```
processor.tokenizer.set_prefix_tokens("en")
model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")
model.config.suppress_tokens = []
```

This is critical: Whisper is multilingual by default. Without forcing `language="en"`, the model wastes capacity on language ID tokens. The `forced_decoder_ids` pins the first decoder token to `<|en|><|transcribe|><|notimestamps|>`, making it strictly English transcription with no timestamps — exactly what SPGISpeech needs (clean transcripts, no alignment).

The data collator handles the `labels` tensor:
1. Pad all label sequences to same length with `pad_token_id`
2. Replace padding positions with `-100` (PyTorch CrossEntropyLoss ignores these)
3. Strip leading `bos_token_id` (Whisper internal generation prepends it)

### 5. Training Dynamics

**For 77K samples with effective batch 32:**

```
Steps per epoch: 77,073 / 32 = ~2,409
Total steps (3 epochs): ~7,226
Time per step (whisper-small, batch 16, fp16): ~12-18s
Total wall time: 7,226 × 15s = ~108,000s = ~30h
```

The eval loop (`predict_with_generate=True`) adds ~2 min per 500-step eval (generating 500 full transcripts autoregressively). With 14 eval checkpoints over 3 epochs, that's ~28 min of eval overhead.

**WER baseline (without fine-tuning):**
- whisper-small on clean English: ~8-9% WER (LibriSpeech clean)
- SPGISpeech is financial earnings calls — heavier accent/terminology — baseline ~15-20%
- After 3 epochs: target ~8-12% WER

### 6. Code Structure

```
/mnt/data/zz/spgispeech/
├── data/S/                                    # 12 parquet files, 42 GB
│   ├── train-00000-of-00006.parquet (~3.7 GB) # 6 shards × ~12,846 rows
│   ├── ...
│   ├── validation-0000*-of-00003.parquet      # 3 shards × ~13,101 rows
│   └── test-0000*-of-00003.parquet            # 3 shards × ~13,114 rows
├── .venv/                                     # venv (Python 3.12, torch 2.6, CUDA 12.4)
├── explore.py                                 # Data exploration helper (already in git)
├── train_whisper.py                           # Main training script (14.7 KB)
├── train_cmd.sh                               # Convenience launcher
├── train_log.json                             # Run log (appended)
└── checkpoints/                               # Model checkpoints + tensorboard logs
```

### 7. How to Monitor

```
# Training progress
tail -f train_small.log

# Loss curves
tensorboard --logdir /mnt/data/zz/spgispeech/checkpoints --bind_all

# GPU utilization
watch -n 2 nvidia-smi

# After training: test WER logged to train_log.json
cat train_log.json | python3 -m json.tool
```
