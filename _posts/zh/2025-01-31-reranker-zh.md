---
audio: true
generated: false
image: false
lang: zh
layout: post
title: 排序器
translated: true
type: post
---

[bge-reranker](https://huggingface.co/BAAI/bge-reranker-v2-m3)

```python
from FlagEmbedding import FlagReranker
reranker = FlagReranker('BAAI/bge-reranker-base', use_fp16=True) # 将 use_fp16 设置为 True 可以加速计算，但会有一定的性能下降

score = reranker.compute_score(['query', 'passage'])
print(score) # -5.65234375

# 可以通过设置 "normalize=True" 将分数映射到 0-1 范围内，这将对分数应用一个 sigmoid 函数。
score = reranker.compute_score(['query', 'passage'], normalize=True)
print(score) # 0.003497010252573502

scores = reranker.compute_score([['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']])
print(scores) # [-8.1875, 5.26171875]

# 可以通过设置 "normalize=True" 将分数映射到 0-1 范围内，这将对分数应用一个 sigmoid 函数。
scores = reranker.compute_score([['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']], normalize=True)
print(scores) # [0.00027803096387751553, 0.9948403768236574]
```

错误

```bash
(mpsFileLoc): /AppleInternal/Library/BuildRoots/b11baf73-9ee0-11ef-b7b4-7aebe1f78c73/Library/Caches/com.apple.xbs/Sources/MetalPerformanceShadersGraph/mpsgraph/MetalPerformanceShadersGraph/Core/Files/MPSGraphUtilities.mm:233:0: error: 'mps.add' 操作需要所有操作数和结果具有相同的元素类型
(mpsFileLoc): /AppleInternal/Library/BuildRoots/b11baf73-9ee0-11ef-b7b4-7aebe1f78c73/Library/Caches/com.apple.xbs/Sources/MetalPerformanceShadersGraph/mpsgraph/MetalPerformanceShadersGraph/Core/Files/MPSGraphUtilities.mm:233:0: note: 查看当前操作：%10 = "mps.add"(%8, %9) : (tensor<1x7x1xf16>, tensor<1xf32>) -> tensor<*xf32>
```

[FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding)
