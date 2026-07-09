---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI驱动的实验追踪价值
translated: true
type: note
---

问题：在 nanoGPT/nanochat 训练中，我们为什么需要 MLflow？它值得使用吗？如果我们已经有像 Hermes 这样的 AI 智能体可以分析日志，我们还需要 MLflow 吗？

回答：

简短的回答是：**MLflow 并非必需**，但一旦你运行大量实验，它会变得非常有价值。

可以把技术栈想象成这样：

```
训练脚本
    |
    +--> stdout/log.txt          (人类可读)
    +--> TensorBoard             (损失曲线)
    +--> Weights & Biases        (托管仪表盘)
    +--> MLflow                  (实验数据库)
```

对于只训练一个 GPT-2 模型的人来说：

```
python train.py
```

MLflow 可能显得多余。

但对于进行 500 次实验的人来说：

```
124M
286M
760M
1.3B

lr = 3e-4
lr = 6e-4
lr = 1e-3

batch = 64
batch = 128
batch = 256

FineWeb
FineWeb-Edu
SEC
Python
Code
...
```

这时 MLflow 就开始节省大量时间。

---

## MLflow 实际存储的内容

不仅仅是

```
step 12000
loss 2.83
```

而是存储

```
Run #381

git commit:
4e3bc91

model:
GPT2-124M

dataset:
SEC-EDGAR

tokens:
15.5B

learning_rate:
3e-4

batch_size:
512

optimizer:
AdamW

validation loss:
2.281

checkpoint:
step_18000.pt

training time:
7h54m
```

现在每个实验都是可搜索的。

---

## 为什么 OpenAI、Anthropic、DeepMind 需要这个

想象一下每天运行

```
2000 次实验
```

如果没有实验追踪：

```
哪个 checkpoint 产生了图 5？

……

不知道。
```

有了 MLflow：

```
SELECT *
WHERE
dataset="FineWeb"
AND lr=3e-4
AND val_loss<2.3
```

搞定。

---

## Hermes 智能体 + MLflow

这里实际上变得有趣了。

不再是人类打开仪表盘：

```
MLflow
      ↑
Hermes Agent
      ↑
LLM
```

智能体可以自动查询实验。

示例提示：

```
比较所有使用余弦学习率的运行。

为什么运行 381 优于运行 412？

建议三个新的超参数。
```

智能体会获取

```
损失曲线
GPU 利用率
学习率调度
梯度范数
验证损失
```

并生成一份报告。

因此 MLflow 成为了智能体的结构化记忆。

---

## 甚至比 MLflow 更好

对于 AI 原生工作流，我会将所有内容存储在 SQL 数据库中。

示例模式：

```
experiments

id
git_hash
dataset
tokens
lr
batch
optimizer
val_loss
train_loss
wall_time
checkpoint
notes
```

然后 Hermes 只需执行

```sql
SELECT *
FROM experiments
ORDER BY val_loss
LIMIT 20;
```

将结果输入 LLM。

不需要仪表盘。

---

## 我会构建什么

鉴于你的工作流（nanoGPT/nanochat，大量小模型实验，CLI 智能体），我会构建类似这样的东西：

```
nanochat
    |
    +--> checkpoint
    |
    +--> metrics.json
    |
    +--> sqlite/postgres
             |
             +--> Hermes
                     |
                     +--> "比较最近 50 次运行"
                     +--> "找出不稳定的运行"
                     +--> "生成训练报告"
                     +--> "预测最佳学习率"
```

这感觉比手动打开 MLflow 更 AI 原生。

---

## 我的建议

对于你目前的规模：

* **<20 次实验：** 简单的 JSON 日志 + TensorBoard 就足够了。
* **20–200 次实验：** MLflow 开始提供真正的价值。
* **数百或数千次实验并配合 AI 智能体：** 我会将 MLflow（或等效的 SQL 支持的实验存储）作为后端，让 Hermes 作为前端。智能体成为查询、比较和分析实验的界面，而不是人类浏览仪表盘。

许多研究实验室正朝着这个方向发展：实验追踪系统仍然是事实来源，而 LLM 智能体位于其之上，自动进行分析、总结趋势并提出下一组实验。

参考资料：

* MLflow 文档：[https://mlflow.org/docs/latest/](https://mlflow.org/docs/latest/)
* nanoGPT：[https://github.com/karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
* TensorBoard：[https://www.tensorflow.org/tensorboard](https://www.tensorflow.org/tensorboard)
