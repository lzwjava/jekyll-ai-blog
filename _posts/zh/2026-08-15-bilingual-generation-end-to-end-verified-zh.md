---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 端到端验证的双语生成
translated: true
type: note
---

生成模型是端到端工作的。以下是完整图景：

## 如何从检查点生成

我在 `/mnt/data/nanoGPT/` 中编写了 `generate_bilingual.py`（它能处理仓库自带的 `scripts/generate.py` 会报错的 `_orig_mod.` 编译前缀，并使用双语分词器和语言控制旋钮）：

```bash
cd /mnt/data/nanoGPT

# 中文模式
./venv/bin/python generate_bilingual.py --lang zh --prompt "机器学习是什么？" --max-new-tokens 200

# 英文模式
./venv/bin/python generate_bilingual.py --lang en --prompt "Machine learning is" --max-new-tokens 200

# 调参旋钮
./venv/bin/python generate_bilingual.py --lang zh --prompt "如何学习编程？" \
    --temperature 0.9 --top-k 200 --num-samples 3 --seed 42
```

## 我在生成前/生成时验证的内容

- **检查点**：迭代 4500/5000，最佳验证损失 4.368，参数 2.32 亿，保存时间 17:12:56。⚠️ **当前没有训练进程在运行**——GPU 空闲（10.6 GB 可用）。它在大约 19:40 的预计完成时间前停止了。如果你想要最后 500 次迭代，运行 `./venv/bin/python train.py --init_from=resume --out_dir=out-bilingual` 将从第 4500 步继续。
- **一致性检查（重要）**：控制标记*并非*单个词表条目——当分词器以 `vocab.json`+`merges.txt` 格式保存时，特殊标记注册表会丢失，因此 `<|lang_zh|>` 会被编码为字节 BPE 片段 `[510, 730, 70, 1126, 509]`。我确认 `train.bin` 中恰好包含这些片段序列（32 万中文+12.7 万英文标记），因此训练和生成看到的 ID 完全相同→旋钮有效，只是作为一个较弱的 5 标记信号而不是单个控制标记。如果你将来重新训练，请通过 `save_pretrained()` 保存分词器来修复此问题（保留特殊标记元数据）。

## 示例输出（全部来自第 4500 次迭代检查点，真实生成）

- **中文标记 + "机器学习是什么？"** → 流利的中文问答（"机器学习是一个从无到有的过程…最终形成科学的知识体系…"）
- **英文标记 + "Machine learning is"** → 关于机器学习算法的连贯英文文章
- **旋钮演示——相同英文提示，两个标记**：两者都继续用英文（提示语言占主导），但中文标记转向了故事/小说风格，而英文标记产生了技术文章。对于中文提示，中文标记产生虚构类文本，英文标记产生文章/营销文案。
- 2GB 语料库以中文为主（标记比例约 2.7:1），因此模糊提示倾向于中文。

**结论**：双语模型能用两种语言生成连贯文本，并带有可用的（尽管是软性的）语言旋钮。主要遗留问题是训练运行被截断（4500/5000）以及分词器的特殊标记错误（供将来重新训练时注意）。
