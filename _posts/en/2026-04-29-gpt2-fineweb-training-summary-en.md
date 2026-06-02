---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 FineWeb Training Summary
translated: false
type: note
---

Here's what's trained in this folder:

| Folder                         | Architecture                 | Size                 | Dataset                       | Iters  | Best val loss |
| ------------------------------ | ---------------------------- | -------------------- | ----------------------------- | ------ | ------------- |
| `out-fineweb/ckpt.pt`          | 12L / 12H / 768d, block 1024 | **GPT-2 124M**       | FineWeb                       | 11,500 | 3.32          |
| `out-wikipedia/ckpt.pt`        | 6L / 6H / 384d, block 512    | ~30M                 | Wikipedia (openwebtext_local) | 18,000 | 4.05          |
| `out-helloworld/ckpt.pt`       | 6L / 6H / 384d, block 256    | ~10M (char-vocab 65) | shakespeare_char              | 500    | 1.77          |
| `out-shakespeare-char/ckpt.pt` | 6L / 6H / 384d, block 256    | ~10M (char-vocab 65) | shakespeare_char              | 500    | 1.71          |
| `out-shakespeare/`             | empty                        | —                    | —                             | —      | —             |

So **yes** — `out-fineweb/ckpt.pt` is a GPT-2 124M architecture (12 layers, 12 heads, 768 embed, 1024 block, vocab 50304), trained from scratch on FineWeb to iter 11,500. The 1.4 GB size matches a 124M-param model saved with optimizer state.

The Shakespeare-char and helloworld checkpoints are the small 10M character-level models, and the wikipedia one is a ~30M mid-size model — neither is GPT-2 124M.
