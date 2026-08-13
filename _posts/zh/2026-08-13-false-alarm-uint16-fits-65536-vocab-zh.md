---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 误报：uint16可容纳65536个词汇
translated: true
type: note
---

该警告是**虚惊一场——它已经过时，与实际不符**。以下是完整说明：

## 警告的*声称内容*

它指出你的模型拥有超过 65535 个 token，因此 `prepare.py` 必须使用 `uint32`，导致 `.bin` 文件体积翻倍（每个 token 占 4 字节而非 2 字节）。

## 实际为何错误

`vocab_size = 65536` 意味着 token **id 从 0 到 65535**——最大 id 恰好是 `65535`。而 `numpy.uint16` 的最大值正好是 `65535`。因此所有内容都能完美适配 `uint16`。

`prepare.py`（实际写入 `.bin` 文件的脚本）清楚这一点——查看其逻辑：

```python
# numpy uint16 最大值为 65535；tokenizer 上限为 65536。
# 如果 vocab_size 恰好为 65536，我们仍可用 uint16（最大 id 为 65535），
# 但一旦超过该值，则需安全起见。
dtype = np.uint16 if vocab_size <= 65536 else np.uint32
```

因此，使用 `--vocab-size 65536` 时：

- `prepare.py` **将使用 `uint16`**（紧凑，每个 token 占 2 字节）
- 你的 `train.bin` 保持较小体积
- **不会使用 uint32，文件也不会变大**

`train_tokenizer.py` 中的 `WARNING` 存在差一错误（使用了 `> 65535` 而非 `> 65536`），与 `prepare.py` 矛盾。这纯粹是表面问题——你可以忽略它。

需要我修复 `scripts/train_tokenizer.py` 中过时的警告，使其与 `prepare.py` 一致（即仅在词表实际超过 65536 时发出警告）吗？只需修改一行：

```python
if tok.get_vocab_size() > 65536:   # 原为 > 65535
```

说一声，我就打补丁。
