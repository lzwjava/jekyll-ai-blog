---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分词器训练内存修复已验证
translated: true
type: note
---

完成。以下是摘要：

## ✅ 已修复、已修补并验证

### 对 `scripts/train_tokenizer.py` 的更改
- 新增 **`--max-bytes N`** 选项（默认 `None` = 不限制，因此除非传入该参数，否则行为不变）。
- 将 `tok.train(files=...)` 切换为 **`tok.train_from_iterator(...)`**，使用流式生成器**逐行**读取文件，并在消费约 `N` 字节后停止——这样语料库永远不会被完整加载到内存中。

### 在 2 GB 文件上的安全测试
使用 `--max-bytes 200000000`（200 MB）加内存监视器运行：

| 指标 | 之前（2 GB，无上限） | 之后（200 MB 上限） |
|---|---|---|
| 峰值 RSS | ~35 GB 且持续上升（被杀死） | **~9.1 GB** |
| 系统可用内存 | 崩溃（54→13 GB 然后冻结） | 稳定在 ~42 GB，健康 |
| 结果 | 从未完成（挂起） | **完成，词表大小 65536** |

输出写入 `/tmp/toktest/out2/`（`vocab.json` 1.2 MB + `merges.txt` 783 KB），特殊 token 完整保留：
```
<|endoftext|> <|lang_en|> <|lang_zh|> <|mix_0|> <|mix_25|> <|mix_50|> <|mix_75|> <|mix_100|>
```

### 建议
- 对于在完整 11.5 GB `mixed.txt` 上的实际运行，请将 `--max-bytes` 设置为 **~150–200 MB**（65k BPE 不需要更多；这正是我们刚刚验证过的）。这应该会将峰值 RSS 限制在约 ~9–10 GB——远低于你的 62 GB。
- 当前机器状态：可用 49 GB，swap 回落到已用 6.5 GB（之前的压力测试导致），一切正常。

之前的冻结**不是代码 bug**——而是 `tok.train()` 将整个 2 GB 语料库加载到 Rust trainer 中（约占文件大小 18 倍的内存），导致机器内存抖动并进入 OOM。现在这已经可以避免。