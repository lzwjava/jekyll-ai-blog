---
audio: false
date: 2025-09-06
generated: true
image: false
lang: zh
layout: post
title: LSTM实现中的错误与修复
translated: true
type: note
---

明白了——这是一个清晰的端到端说明，展示了这个从零实现的LSTM脚本在做什么，以及那些会破坏训练的细微错误及其修复方法。我将保持线性结构便于阅读（不使用宽表格）。

# 代码试图实现的功能

你正在用NumPy实现一个极简的字符/词级LSTM语言模型：

1. **设置与维度**

* `hidden_size`、`vocab_size`、数据集（`training_set`、`validation_set`、`test_set`）、标记↔索引映射，以及`sigmoid`、`tanh`、`softmax`、`one_hot_encode_sequence`等函数预期来自`data.py` / `utils.py`。
* 每个时间步的输入是一个one-hot向量`x ∈ R^{vocab_size×1}`。
* 你将先前的隐藏状态与当前输入拼接：
  `z = [h_{t-1}; x_t] ∈ R^{(hidden_size+vocab_size)×1}`。
  这就是为什么`W_f, W_i, W_g, W_o ∈ R^{hidden_size×(hidden_size+vocab_size)}`。

2. **参数初始化**

* `init_lstm(...)`为四个门（遗忘门f、输入门i、候选门g、输出门o）分配权重，外加输出投影`W_v`到词汇表。
* `init_orthogonal`使每个权重矩阵正交归一化（通过QR分解）。这对RNN/LSTM来说是一个不错的选择。

3. **前向传播（每个序列）**
   对于每个时间步：

* 构建`z = [h_prev; x]`。
* 计算门控：

  * `f_t = σ(W_f z + b_f)`
  * `i_t = σ(W_i z + b_i)`
  * `g_t = tanh(W_g z + b_g)`
  * `C_t = f_t ⊙ C_{t-1} + i_t ⊙ g_t`
  * `o_t = σ(W_o z + b_o)`
  * `h_t = o_t ⊙ tanh(C_t)`
* 投影到词汇表并应用softmax：

  * `v_t = W_v h_t + b_v`
  * `ŷ_t = softmax(v_t)`
* 代码存储了许多中间变量（`z_s, f_s, i_s, g_s, C_s, o_s, h_s, v_s, output_s`）用于反向传播。

4. **损失函数**

* 每个时间步与one-hot目标的交叉熵：
  `L_t = − log ŷ_t[target]`
  （代码使用了逐元素的`-mean(log(ŷ)*one_hot)`，这等价于`-log(ŷ[target])`，仅相差一个常数缩放因子。）

5. **反向传播（通过LSTM的BPTT）**

* 经典的LSTM梯度，从`t = T−1 → 0`累积。
* 裁剪全局梯度范数，然后进行SGD更新。

6. **训练循环**

* 对于每个周期：在验证集上评估（仅计算损失），然后在训练集上训练（损失 + 梯度 + 更新）。最后，绘制训练/验证损失曲线。

---

# 关键问题（这些问题会静默地破坏学习）

## 1) 反向传播中 `h` 和 `C` 的索引偏移错误

在`forward`中，你首先压入*初始*状态：

* `h_s[0] = h_init`，然后在步骤0之后追加`h_0` → 因此`h_s`的长度为`T+1`，且`h_s[t+1] = h_t`。
* `C_s`同理：`C_s[0] = C_init`，然后`C_s[t+1] = C_t`。

但在`backward(...)`中，你使用`h[t]`和`C[t]`，好像它们就是`h_t`和`C_t`。其实不是；它们偏移了1。

**修复（简单的经验法则）：**

* 在你想要`h_t`的地方使用`h[t+1]`。
* 在你想要`C_t`的地方使用`C[t+1]`。
* 对于“先前的细胞状态”，你需要`C_prev = C[t]`（而不是`C[t-1]`）。

所以在`for t in reversed(range(T)):`循环内部：

* 当前状态：`h_t = h[t+1]`，`C_t = C[t+1]`
* 先前状态：`C_{t-1} = C[t]`

你当前的代码行：

```python
C_prev = C[t - 1]
```

对于`t==0`是错误的（会绕到最后一个元素），并且总体上偏移了1。它必须是：

```python
C_prev = C[t]       # 先前的细胞状态
# 并使用 C_t = C[t+1] 作为"当前"
```

并且，任何你使用`h[t]`意图表示当前隐藏状态的地方，都应改为`h[t+1]`。

## 2) 几个门控的导数计算错误

你有时重复应用了非线性函数而不是其导数，或者忘记了导数标志。

* **细胞状态路径：**
  正确：
  `dC_t += dh_t ⊙ o_t ⊙ (1 - tanh(C_t)^2)`
  你的代码：

  ```python
  dC += dh * o[t] * tanh(tanh(C[t]), derivative=True)
  ```

  这里应用了两次`tanh`。应替换为：

  ```python
  dC += dh * o_t * (1 - np.tanh(C_t)**2)
  ```

* **遗忘门：**
  正确：`df = dC_t ⊙ C_{t-1} ⊙ f_t ⊙ (1 - f_t)`
  你的代码：

  ```python
  df = dC * C_prev
  df = sigmoid(f[t]) * df
  ```

  缺少了导数项。应该是：

  ```python
  df = dC * C_prev
  df *= f[t] * (1 - f[t])      # 如果 f[t] 存储的是 σ 激活前的输出
  ```

* **输入门：**
  你做了：

  ```python
  di = dC * g[t]
  di = sigmoid(i[t], True) * di
  ```

  如果`sigmoid(x, True)`返回的是 σ’(x) *而不是* σ(x)，那么这是可以的。更稳健的做法（与你存储`i[t]`作为门控输出的方式匹配）是：

  ```python
  di = dC * g[t]
  di *= i[t] * (1 - i[t])
  ```

* **候选门：**
  你做了：

  ```python
  dg = dC * i[t]
  dg = tanh(g[t], derivative=True) * dg
  ```

  如果`g[t]`存储的是`tanh(preact)`，那么`tanh’(preact) = 1 - g[t]^2`。所以：

  ```python
  dg = dC * i[t]
  dg *= (1 - g[t]**2)
  ```

* **输出门：**
  你做了：

  ```python
  do = dh * tanh(C[t])
  do = sigmoid(o[t], derivative=True) * do
  ```

  结合索引修复（`C_t = C[t+1]`，`o_t = o[t]`）和上述的导数计算：

  ```python
  do = dh * np.tanh(C_t)
  do *= o[t] * (1 - o[t])
  ```

* **下一个细胞梯度：**
  正确：

  ```python
  dC_next = dC * f[t]
  ```

## 3) 使用 `h[0]` / `C[0]` 来调整 `dh_next` 和 `dC_next` 的大小

你需要的是*当前* h/C（序列末尾）的形状，而不是初始的零向量。使用：

```python
dh_next = np.zeros_like(h[-1])
dC_next = np.zeros_like(C[-1])
```

## 4) 交叉熵的数值稳定性

如果`softmax`内部进行了截断/加epsilon处理，那么`loss += -np.mean(np.log(outputs[t]) * targets[t])`是没问题的。如果没有，添加一个小的epsilon：

```python
eps = 1e-12
loss += -np.sum(targets[t] * np.log(outputs[t] + eps))
```

## 5) 训练稳定性调整

* **遗忘门偏置：** 将`b_f`初始化为一个正值（例如，`1.0`），以便在训练早期LSTM倾向于保留记忆：

  ```python
  b_f = np.ones((hidden_size, 1)) * 1.0
  ```

* **学习率：** 使用原始SGD时，`lr=1e-1`过于激进。从`1e-2`开始或使用Adam。
* **梯度裁剪：** 很好。如果需要，可以考虑按矩阵范数进行裁剪。

---

# 反向传播循环的修正核心代码

这个草图展示了索引和导数的修正。它假设`f[t], i[t], g[t], o[t]`是它们非线性函数的*输出*（如你的前向传播中所示）：

```python
T = len(outputs)
dh_next = np.zeros_like(h[-1])
dC_next = np.zeros_like(C[-1])

for t in reversed(range(T)):
    # 使用正确索引的简短变量名
    y_hat = outputs[t]                 # softmax 输出
    y_true = targets[t]
    h_t   = h[t+1]
    C_t   = C[t+1]
    C_tm1 = C[t]

    # 输出层
    dv = y_hat.copy()
    dv[np.argmax(y_true)] -= 1
    W_v_d += dv @ h_t.T
    b_v_d += dv

    # 反向传播到 h
    dh = W_v.T @ dv
    dh += dh_next

    # 输出门
    do = dh * np.tanh(C_t)
    do *= o[t] * (1 - o[t])
    W_o_d += do @ z[t].T
    b_o_d += do

    # 细胞状态
    dC = dC_next + dh * o[t] * (1 - np.tanh(C_t)**2)

    # 候选门 (g), 输入门 (i), 遗忘门 (f)
    dg = dC * i[t]
    dg *= (1 - g[t]**2)               # 因为 g[t] = tanh(preact)

    di = dC * g[t]
    di *= i[t] * (1 - i[t])

    df = dC * C_tm1
    df *= f[t] * (1 - f[t])

    # 累积门控权重/偏置梯度
    W_g_d += dg @ z[t].T;  b_g_d += dg
    W_i_d += di @ z[t].T;  b_i_d += di
    W_f_d += df @ z[t].T;  b_f_d += df

    # 传播到 z 并分割到 h_{t-1} 部分
    dz = (W_f.T @ df) + (W_i.T @ di) + (W_g.T @ dg) + (W_o.T @ do)
    dh_next = dz[:hidden_size, :]
    dC_next = dC * f[t]
```

---

# 较小但重要的细节与建议

* **正交初始化：** 对循环权重很好。对于输入部分，你也可以按`1/√fan_in`进行缩放。这里不关键。
* **批处理：** 代码一次训练1个序列（无批处理）。对于清晰度来说很好，但速度慢/噪声大。小批量处理需要仔细的形状更改。
* **教师强制：** 你使用真实的下一个标记作为目标；很好。如果你将来进行自由运行生成，请从`softmax`输出中采样并反馈给模型。
* **损失报告：** 你在序列间累加每个时间步的损失，然后按数据集长度平均；如果序列长度不同，这会混合尺度。考虑按总标记数进行归一化。
* **绘图：** 在本地工作。在无头环境中，记得切换后端或使用savefig。

---

# 你现在应该立即进行的修复总结

1. **索引**：在反向传播中，将每个`h[t]`替换为`h[t+1]`，每个`C[t]`替换为`C[t+1]`，并设置`C_prev = C[t]`。
2. **导数**：

   * 对细胞状态路径使用`(1 - tanh(C_t)**2)`。
   * 对σ门使用`gate * (1 - gate)`，因为你存储的是门控输出。
   * 对候选门使用`(1 - g[t]**2)`，因为`g[t]=tanh(preact)`。
3. **初始化**：将`b_f`设置为约`1.0`。
4. **学习率**：降至`1e-2`（或切换到Adam）。
5. **稳定性**：在`log`中添加`eps`。

进行这些更改后，你的损失应该开始以更合理的方式下降。如果你愿意，可以粘贴你更新后的`backward(...)`代码，我会帮你检查一下。
