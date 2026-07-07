---
audio: false
generated: true
image: false
lang: zh
layout: post
title: H200的GPT-3数据准备指南
translated: true
type: note
---

问题：**在H200上训练GPT-3风格模型，我们应该获取什么数据？FineWeb-Edu 25B token是否足够？**

答案：

对于GPT-3风格的预训练，数据集的选择比GPU更重要。H200只改变**训练速度**，而不改变**你需要什么数据**。

原版NVIDIA H200 Tensor Core GPU可以处理更大的模型/批次，但你的瓶颈通常会是**数据质量 + token数量 + 训练预算**。

你当前的脚本：

```
HuggingFaceFW/fineweb-edu
25B tokens
~100GB parquet
```

是一个不错的**消融数据集**，但不是GPT-3复现数据集。

---

## 1. GPT-3实际训练所用的数据

原始GPT-3大致使用：

| 数据集                |      Token数 | 用途              |
| --------------------- | -----------: | ----------------- |
| Common Crawl过滤版    |        ~410B | 通用网页          |
| WebText2              |         ~19B | 高质量网页        |
| Books1                |         ~12B | 书籍              |
| Books2                |         ~55B | 书籍              |
| Wikipedia             |          ~3B | 百科全书          |
| 总计                  | ~500B tokens |                   |

著名的GPT-3比例：

```
模型参数量 : 训练token数

175B参数 : 300B token
```

大致遵循Chinchilla扩展法则：

```
token数 ≈ 20 × 参数量
```

---

## 2. 如果你今天训练一个小型GPT-3克隆

假设：

### 1B模型

```
参数量 = 1B

推荐token数：
20B tokens
```

### 7B模型

```
参数量 = 7B

推荐token数：
140B tokens
```

### 13B模型

```
参数量 = 13B

推荐token数：
260B tokens
```

### 70B模型

```
参数量 = 70B

推荐token数：
1.4T tokens
```

---

## 3. FineWeb-Edu很好，但不完整

FineWeb-Edu优秀的原因：

* 教育性过滤
* 高质量网页
* 现代爬取
* 宽松许可

但：

```
仅FineWeb-Edu
        |
        v
大部分是网页文本
```

缺少：

```
书籍
代码
论文
Wikipedia
数学
对话
```

更好的混合：

```
FineWeb-Edu          60%
书籍                 15%
代码                 10%
Wikipedia             5%
Arxiv/论文            5%
合成/指令数据         5%
```

---

## 4. 针对你的H200，我会准备这些

对于一个严肃的实验：

```
datasets/

fineweb-edu/
    100B tokens

fineweb/
    100B tokens

starcoder-data/
    20B tokens

wikipedia/
    5B tokens

arxiv/
    5B tokens

books/
    20B tokens
```

总计：

```
~250B tokens
```

足够用于：

```
7B模型
```

---

## 5. 存储计算

你的脚本：

```
25B tokens
≈100GB
```

因为：

```
1 token ≈ 4字节
```

因此：

```
100B tokens
≈400GB raw parquet

250B tokens
≈1TB raw
```

分词后：

```
uint16 token id

250B tokens × 2字节

≈500GB
```

你需要：

```
1-2TB NVMe
```

以便舒适地进行预处理。

---

## 6. 对于H200，我不会训练GPT-3 175B

即使有H200：

175B：

```
权重FP16：
350GB

优化器状态Adam：
~1.4TB

总训练内存：
>2TB
```

需要：

```
8-64块H200 GPU
```

相反，好的H200项目：

### 1.3B

```
token数：
30B

时间：
几小时到几天
```

### 7B

```
token数：
140B

时间：
几天
```

### 13B

```
token数：
260B

时间：
一周以上
```

---

## 7. 你当前的下载器设计

这个：

```python
DEFAULT_TOKENS = 25_000_000_000
```

适合：

```
GPT-3消融实验
```

意思是：

```
能否复现扩展曲线？
架构是否可行？
训练流水线是否可行？
```

但不适合：

```
有竞争力的LLM
```

对于H200，我会改为：

```python
DEFAULT_TOKENS = 100_000_000_000
```

并添加：

```
FineWeb-Edu
+
FineWeb
+
StarCoder
+
Wikipedia
+
Arxiv
```

---

我推荐的首次H200运行：

```
模型：
Llama风格decoder

参数量：
1.3B

数据集：
50B tokens FineWeb-Edu

上下文长度：
4096

分词器：
GPT-NeoX tokenizer

优化器：
AdamW

精度：
BF16

GPU：
1x H200
```

然后扩展：

```
1.3B -> 7B
50B -> 150B tokens
```

这样可以得到一个真正的GPT风格训练流水线，而不会浪费H200的时间。