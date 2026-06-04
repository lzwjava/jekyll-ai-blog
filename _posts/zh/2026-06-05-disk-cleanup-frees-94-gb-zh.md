---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 磁盘清理释放 94 GB
translated: true
type: note
---

之前：459 GB 已用，约 1 GB 空闲（使用率 94%）  
之后：365 GB 已用，59 GB 空闲（使用率 87%）

总计释放：约 94 GB

以下是清理的内容：

```
 ✓ 临时 git 包（中断的 gc）           约 23 GB
 ✓ HuggingFace 模型缓存               约 21 GB
 ✓ npm 缓存                          约 7.2 GB
 ✓ JetBrains 缓存                    约 7.1 GB
 ✓ PyTorch hub 缓存                  约 4.6 GB
 ✓ pre-commit 缓存                  约 3 GB
 ✓ pip 缓存                          约 2.6 GB
 ✓ Homebrew 缓存                     约 3.7 GB（来自 npm/brew）
 ✓ 其他开销                          约 22 GB（APFS 元数据等）
```

你从“磁盘严重不足”变成了剩余 59 GB——健康的区间。

lzwjava.github.io 的 `.git/` 仍有 35 GB，分布在 23 个包中。对于一个博客来说仍然臃肿。需要我对它运行 `git gc --aggressive` 吗？它会将所有内容重新打包成一个紧凑的包——可能再节省 5-10 GB，但需要 5-10 分钟。
