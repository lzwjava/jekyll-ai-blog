---
audio: false
date: 2025-09-06
generated: true
image: false
lang: zh
layout: post
title: 模型形状修复与改进
translated: true
type: note
---

以下是你的脚本逐段执行的内容，以及你可能需要进行的几项重要修正。

# 模型结构

* 你定义了一个微型的**字符/词级下一词元预测器**：

  * `nn.LSTM(input_size=vocab_size, hidden_size=50, num_layers=1)` 处理一个独热向量序列（尺寸 = `vocab_size`），并在每个时间步生成一个大小为50的隐藏状态。
  * `nn.Linear(50, vocab_size, bias=False)` 将每个时间步的隐藏状态映射到**词汇表上的逻辑值**。

# 预期的张量形状（关键）

由于你没有设置 `batch_first=True`，PyTorch LSTM的默认输入形状是 **(seq\_len, batch\_size, input_size)**。

* 对于批次大小为1的单个序列：

  * 输入LSTM的形状应为 `(seq_len, 1, vocab_size)`。
  * LSTM输出 `x` 的形状为 `(seq_len, 1, hidden_size)`。
  * 然后你使用 `view(-1, hidden_size)` → `(seq_len, hidden_size)`，这样线性层会生成 `(seq_len, vocab_size)`。
  * `CrossEntropyLoss` 期望：

    * `outputs`：`(N, C)` = `(seq_len, vocab_size)`
    * `targets`：`(N,)` = `(seq_len,)` 词元索引

# 你的代码可能出错的地方（形状）

你执行了：

```python
inputs_one_hot = inputs_one_hot.permute(0, 2, 1)
```

如果 `one_hot_encode_sequence` 返回 `(batch, seq_len, vocab)`，那么对于默认的LSTM，正确的置换是 **`permute(1, 0, 2)`**（以得到 `(seq_len, batch, vocab)`）。你当前的 `permute(0,2,1)` 会给出 `(batch, vocab, seq_len)`，这将导致不匹配，如果之前的形状与假设不同，要么会出错，要么会静默地学习无意义的内容。

两个简洁的选项（选择其一）：

**A) 保持默认的LSTM（批次第二）：**

```python
# 需要 (seq_len, batch, input_size)
inputs_one_hot = inputs_one_hot.permute(1, 0, 2)  # (seq_len, 1, vocab_size)
```

**B) 使其批次优先（通常更简单）：**

```python
self.lstm = nn.LSTM(input_size=vocab_size, hidden_size=50, batch_first=True)
# 需要 (batch, seq_len, input_size)
# 然后 不要 置换；保持为 (1, seq_len, vocab_size)
```

# 训练循环逻辑

* 你为每个周期保留两个运行总和：`epoch_training_loss` 和 `epoch_validation_loss`。
* **验证阶段**（`net.eval()` + 无梯度步骤）：

  * 对于 `validation_set` 中的每个 (inputs, targets)：

    * 对输入进行独热编码，将目标转换为索引
    * 前向传播 → 逻辑值 `(seq_len, vocab_size)`（假设形状已固定）
    * 针对形状为 `(seq_len,)` 的目标索引计算CE损失
    * 累积损失
* **训练阶段**（`net.train()`）：

  * 相同的预处理
  * 前向传播 → 损失 → `optimizer.zero_grad()` → `loss.backward()` → `optimizer.step()`
* 你记录平均损失并每5个周期打印一次。

# 推理与打印输出

* 你从 `test_set` 中选取一个样本，运行模型，获取每个时间步的逻辑值，对每个时间步取 `argmax` → 预测的词元。
* 你打印输入词、目标词和预测词。
* 你绘制训练损失与验证损失随周期的变化图。

# 小型但高影响力的改进

1. **修正输入形状**（最重要）。使用上述A或B选项之一。如果你选择批次优先，将前向传播改为：

   ```python
   x, (h, c) = self.lstm(x)         # x: (batch, seq, hidden)
   x = x.reshape(-1, self.lstm.hidden_size)  # (batch*seq, hidden)
   ```

2. **在评估/推理时使用 `with torch.no_grad()`** 以避免跟踪梯度，并提高速度/内存效率：

   ```python
   net.eval()
   with torch.no_grad():
       outputs = net(inputs_one_hot)
       loss = criterion(outputs, targets_idx)
   ```

   以及用于numpy转换：

   ```python
   outputs = net(inputs_one_hot).detach().numpy()
   ```

3. **也为PyTorch设置随机种子** 以确保可复现性：

   ```python
   torch.manual_seed(42)
   ```

4. **设备处理**（如果你使用GPU）：

   ```python
   device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
   net.to(device)
   inputs_one_hot = inputs_one_hot.to(device)
   targets_idx = targets_idx.to(device)
   ```

5. **目标对齐**：确保 `targets` 是与每个输入时间步对齐的**下一词元**。如果你的数据集以这种方式配对 `(inputs, targets)`，那就没问题。否则，创建 `targets = inputs[1:]` 并丢弃最后一个输入或类似操作。
6. **除非有理由，否则去掉 `.bias=False`**；输出层上的偏置通常是无害/有帮助的。
7. **填充/可变长度**（可选）：如果序列长度不同，考虑使用 `pack_padded_sequence` 以避免在填充词元上训练。
8. **监控**：在下一词元预测上的准确率比仅看损失更易解释——在验证集上计算 `% correct argmax`。

# 最小修正代码片段（批次优先版本）

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=vocab_size, hidden_size=50, num_layers=1, batch_first=True)
        self.l_out = nn.Linear(50, vocab_size)

    def forward(self, x):
        # x: (batch, seq, vocab_size)
        x, _ = self.lstm(x)                    # (batch, seq, hidden)
        x = x.reshape(-1, self.lstm.hidden_size)  # (batch*seq, hidden)
        x = self.l_out(x)                      # (batch*seq, vocab)
        return x

# ... 在你的循环中，移除置换；确保 inputs_one_hot 是 (batch, seq, vocab)
# 验证/推理使用 `with torch.no_grad()` 和 `.detach()`
```

如果你分享 `one_hot_encode_sequence` 返回的确切形状（例如，`(seq, vocab)` 与 `(1, seq, vocab)`），我可以为你的情况精确调整置换/重塑行。
