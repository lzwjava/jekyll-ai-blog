---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-2精细网络训练总结
translated: true
type: note
---

以下是此文件夹中的训练内容：

| 文件夹                         | 架构                       | 大小                | 数据集                        | 迭代次数  | 最佳验证损失 |
| ------------------------------ | ---------------------------- | -------------------- | ----------------------------- | ------ | ------------- |
| `out-fineweb/ckpt.pt`          | 12L / 12H / 768d，块大小 1024 | **GPT-2 124M**       | FineWeb                       | 11,500 | 3.32          |
| `out-wikipedia/ckpt.pt`        | 6L / 6H / 384d，块大小 512    | ~30M                 | Wikipedia (openwebtext_local) | 18,000 | 4.05          |
| `out-helloworld/ckpt.pt`       | 6L / 6H / 384d，块大小 256    | ~10M（字符词汇表 65） | shakespeare_char              | 500    | 1.77          |
| `out-shakespeare-char/ckpt.pt` | 6L / 6H / 384d，块大小 256    | ~10M（字符词汇表 65） | shakespeare_char              | 500    | 1.71          |
| `out-shakespeare/`             | 空                           | —                    | —                             | —      | —             |

因此 **是的** —— `out-fineweb/ckpt.pt` 是一个 GPT-2 124M 架构（12 层，12 个头，嵌入维度 768，块大小 1024，词汇表 50304），在 FineWeb 上从头训练至迭代 11,500 次。其 1.4 GB 的大小与包含优化器状态的 124M 参数模型保存文件相符。

Shakespeare-char 和 helloworld 检查点是小型 10M 字符级模型，而 wikipedia 检查点是一个约 30M 的中等规模模型 —— 两者均非 GPT-2 124M。