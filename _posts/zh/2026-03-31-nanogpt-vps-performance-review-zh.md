---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 廉价 VPS 上的 nanoGPT 性能评测
translated: true
type: note
---

这是完整的审查报告，老板：

---

## 🦞 nanoGPT on VPS — 综合评测

### Server Specs
- **CPU**: DO-Regular (DigitalOcean droplet), 1 vCPU
- **RAM**: 458 MB (在没有 swap 的情况下会出现 OOM — 已添加 1GB swap file)
- **Disk**: 总计 8.7 GB，安装后剩余 4.0 GB

### Model
- **Architecture**: 6-layer, 6-head, 384-embedding GPT (character-level)
- **Parameters**: 10.65M
- **Vocab**: 65 tokens (Shakespeare 字符集)
- **Context window**: 256 tokens
- **Checkpoint**: ~124 MB

### Training Status
- **Dataset**: Shakespeare character-level (1.06 MB 原始文本)
- **Trained**: 2,000 / 5,000 iterations (完成 40%)
- **Best val loss**: 1.4716 (表现尚可，进一步训练仍有提升空间)
- **Config**: batch 64, lr 0.001, dropout 0.2, weight decay 0.1

### Inference Performance (CPU)

| Tokens | Time | Speed |
|--------|------|-------|
| 50 | 1.28s | 39.1 tok/s |
| 100 | 3.56s | 28.1 tok/s |
| 200 | 11.27s | 17.7 tok/s |

生成的序列越长，速度下降越明显（KV cache 增长，受限于该微型主机的 memory-bound 瓶颈）。

### Memory Usage
- **Model load**: 310 MB RSS (在 458MB 内存的机器上必须使用 swap)
- **Swap used**: 推理期间占用 89 MB — 虽然处于可控范围，但并不理想

### Output Quality
生成的文本具有明显的 Shakespeare 风格 — 包含正确的角色名称（CORIOLANUS, VOLUMNIA, JULIET）以及符合时代的用词。但在 40% 的训练进度和仅 10M parameters 的情况下，文本在约 30-40 个字符后会变得缺乏逻辑。增加训练量会有所改善。

### Verdict
可以运行，但该 VPS 配置对于任何严肃的应用来说都性能不足。作为 demo 或学习用途尚可。如果需要更好的输出效果，建议：
1. **继续训练** (完成剩余的 3,000 iters — 在 CPU 上大约需要 1-2 小时)
2. **提升硬件配置** — 即使是 2GB RAM 也能消除对 swap 的依赖
