---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 垃圾进，垃圾出
translated: true
type: note
---

这就是结果——完全是一堆垃圾。空格、HTML片段、随机符号。

如果你想自己运行并尝试不同的提示和温度参数，可以使用以下命令：

```
cd /mnt/data/nanoGPT && python3 sample.py \
  --out_dir=out-github-code-124m \
  --num_samples=3 \
  --max_new_tokens=300 \
  --temperature=0.8 \
  --top_k=40 \
  --start="def quicksort(arr):
"
```

更改 `--start=` 来尝试不同的提示。但无论如何输出都会很糟糕——模型学会了输出空格和HTML片段，因为46%的训练数据是噪声（HTML文档、许可证头部、配置存根）。只有54%是实际代码。

解决办法是清洗数据并重新训练。需要我编写一个过滤脚本吗？