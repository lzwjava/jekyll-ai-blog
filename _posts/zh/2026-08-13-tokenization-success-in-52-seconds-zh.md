---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 52秒内的代币化成功
translated: true
type: note
---

完成——在 **52 秒**内干净利落地结束（无 OOM，无挂起）。

## 结果
- **输出：** `tok_mixed/`（`vocab.json` + `merges.txt`）
- **词表大小：** 65536
- **特殊标记**无损保留：`<|endoftext|>`、`<|lang_en|>`、`<|lang_zh|>`、`<|mix_0|>`、…、`<|mix_100|>`

```bash
ls -la tok_mixed/
```

## 备注
- `WARNING: vocab > 65535` 是正常的——它只是意味着 `prepare.py` 会使用 `uint32` 并生成稍大的 `.bin` 文件。如果你想要更紧凑的 `uint16` 二进制文件，请重新运行并指定 `--vocab-size 65536`……等等，这跟之前一样。要保持在 65535，你需要使用 `--vocab-size 65535`（或更低）。这纯粹是文件大小上的权衡，不影响正确性。
- 200 MB 的数据使得运行非常快速且内存占用低。如果你之后发现合并结果对稀有子词训练不足，可以升级到 2 GB 样本——这只是一个内存与质量的调优问题。

需要我检查词表中是否包含正确的中文字符合并（对联合 BPE 进行完整性检查），或者修复 uint32/uint16 警告吗？