---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 80/10/10数据划分详解
translated: true
type: note
---

问题：能否解释nanoGPT和nanochat中使用的80/10/10训练/验证/测试划分，以及这种分离为何重要？

回答：

是的，完全正确。**8/1/1划分**（80%训练、10%验证、10%测试）是nanoGPT/nanochat中的标准做法。以下是其原理和实现方式：

## 为何需要三个数据集？

**训练集（80%）**：学习参数。梯度更新仅在此处进行。

**验证集（10%）**：调整超参数并检测过拟合。训练过程中（每隔N步）在验证集上评估，观察训练集与验证集之间的损失差异——这就是过拟合的信号。

**测试集（10%）**：最终评估。在所有超参数调整锁定后，*仅一次*在测试集上进行评估。这能提供泛化性能的无偏估计。

关键点在于：**验证集和测试集必须与训练集完全分离**。如果在训练过程中使用测试集（例如用于选择超参数），就会泄露信息，导致最终结果失去意义。

## nanoGPT中的实现

```python
# nanoGPT中的典型划分
data = np.memmap('data.bin', dtype=np.uint16, mode='r')
n = len(data)

train_data = data[:int(0.8*n)]      # 80%用于训练
val_data = data[int(0.8*n):int(0.9*n)]   # 10%用于验证
test_data = data[int(0.9*n):]       # 10%用于测试

def get_batch(split, batch_size=32):
    """训练期间采样一个批次"""
    if split == 'train':
        ix = torch.randint(len(train_data) - context_length, (batch_size,))
        x = torch.stack([torch.from_numpy((train_data[i:i+context_length]).astype(np.int64)) for i in ix])
        y = torch.stack([torch.from_numpy((train_data[i+1:i+1+context_length]).astype(np.int64)) for i in ix])
    else:  # val 或 test
        ix = torch.randint(len(val_data) - context_length, (batch_size,))
        x = torch.stack([torch.from_numpy((val_data[i:i+context_length]).astype(np.int64)) for i in ix])
        y = torch.stack([torch.from_numpy((val_data[i+1:i+1+context_length]).astype(np.int64)) for i in ix])
    return x, y
```

## 训练循环模式

```python
for iter in range(max_iters):
    # 从训练集采样，计算损失，反向传播
    logits, loss = model(get_batch('train'))
    loss.backward()
    optimizer.step()

    # 每 eval_interval 步，检查验证损失（无梯度）
    if iter % eval_interval == 0:
        with torch.no_grad():
            val_loss = estimate_loss('val')  # 仅在验证集上前向传播
        print(f"iter {iter}: train_loss {train_loss:.4f}, val_loss {val_loss:.4f}")
```

**验证损失告诉你是否过拟合**：
- 如果 `val_loss >> train_loss`：模型记住了训练数据，没有泛化能力
- 如果两者同步下降：泛化良好，继续训练

## 针对语言模型的特殊考量

在大规模场景下，划分理念略有变化：

1. **对于小模型（nanoGPT规模）**：8/1/1划分即可。验证集和测试集规模相当。

2. **对于大模型**：验证集比测试集更重要：
   - 训练过程中在验证集上进行的评估步骤多10-100倍（影响梯度决策）
   - 测试集仅在最后评估一次（不用于调参）
   - 有些团队使用9/0.5/0.5甚至更大的训练集比例，因为更多数据总是有益的

3. **对于生产模型**：可能会使用一个保留的**测试分布**（不同领域/时间段），以捕捉验证集未能发现的分布偏移。

## 大数据集的实际考量

如果你在数十亿token上训练（就像你正在用MI300X探索的那样），10%的验证/测试集可能达到GB级别。你可以更激进地划分：

```python
# 对于数十亿token的数据集，5%验证/5%测试是可以接受的
train_split = 0.90
val_split = 0.95  # 5%验证，5%测试
```

验证/测试集的绝对大小比百分比更重要——你需要足够的token来获得稳定的损失估计，但超过约1GB的验证数据后，收益递减。

---

**总结**：严格分离验证集和测试集。在训练过程中使用验证损失来检测过拟合并调整学习率/dropout等超参数。在所有参数锁定后，仅一次使用测试集。如果你的结果要具有可信度，这一点不容妥协。