---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 测试FlashAttention 2验证
translated: true
type: note
---

问题：这段代码如何测试 FlashAttention 2 是否正常工作？

答案：

你的脚本执行了**三级验证**：

### 1. 确认 PyTorch 识别 GPU

```python
import torch
print('torch:', torch.__version__)
print('GPU:', torch.cuda.get_device_name(0))
```

这一步确认：

* PyTorch 已安装。
* CUDA/HIP 后端正常运行。
* 显卡可见。

示例输出：

```text
torch: 2.8.0+rocm
GPU: AMD Instinct MI300X
```

如果这一步失败，FlashAttention 无法工作，因为 PyTorch 本身无法访问 GPU。

---

### 2. 确认 FlashAttention 2 成功导入

```python
import flash_attn
print('flash_attn version:', flash_attn.__version__)

from flash_attn import flash_attn_func
print('flash_attn_func imported OK')
```

这一步检查：

* FlashAttention 包已安装。
* C++/CUDA/ROCm 扩展编译正确。
* Python 能加载编译后的共享库。

成功时的典型输出：

```text
flash_attn version: 2.8.3
flash_attn_func imported OK
```

失败时的典型输出：

```text
ImportError: cannot import name flash_attn_func
```

或

```text
undefined symbol ...
```

通常表示构建时出现问题。

---

### 3. 执行真实的 FlashAttention 内核

这是最重要的一步。

```python
q = torch.randn(2, 1024, 12, 128,
                device='cuda',
                dtype=torch.bfloat16)

k = torch.randn(2, 1024, 12, 128,
                device='cuda',
                dtype=torch.bfloat16)

v = torch.randn(2, 1024, 12, 128,
                device='cuda',
                dtype=torch.bfloat16)

out = flash_attn_func(q, k, v, causal=True)
```

形状含义：

| 维度       | 值   | 含义           |
| ---------- | ---- | -------------- |
| Batch      | 2    | 两条序列       |
| Seq Len    | 1024 | 上下文长度     |
| Heads      | 12   | 注意力头数     |
| Head Dim   | 128  | 头维度         |

FlashAttention 2 计算：

[
\text{softmax}(QK^T)V
]

使用融合内核。

成功输出：

```text
FA2 forward pass: OK, shape torch.Size([2, 1024, 12, 128])
```

证明：

* ROCm 内核已加载。
* 内核在 MI300X 上成功执行。
* 输出形状正确。

---

### 4. 测试滑动窗口注意力

```python
out_sw = flash_attn_func(
    q, k, v,
    causal=True,
    window_size=(256, 0)
)
```

这一步验证 FlashAttention 的额外功能。

每个 token 不再关注全部 1024 个 token，而只关注：

```text
左侧 256 个 token
右侧 0 个 token
```

成功输出：

```text
FA2 sliding window: OK, shape torch.Size([2, 1024, 12, 128])
```

确认：

* 窗口注意力内核正常工作。
* NanoChat 的局部注意力模式应该可用。

---

### 5. 确认 NanoChat 检测到 FlashAttention

```python
from nanochat.flash_attention import (
    flash_attn as fa,
    USE_FA2,
    HAS_FA2,
    USE_FA3
)
```

这些标志决定 NanoChat 实际使用的实现。

在 MI300X 上预期输出：

```text
HAS_FA2: True
USE_FA2: True
USE_FA3: False
```

含义：

| 标志    | 含义                     |
| ------- | ------------------------ |
| HAS_FA2 | FlashAttention 2 已安装  |
| USE_FA2 | NanoChat 将使用 FA2      |
| USE_FA3 | FlashAttention 3 已激活  |

对于目前的 MI300X，看到：

```text
HAS_FA2: True
USE_FA2: True
USE_FA3: False
```

是最理想的结果。

---

### 额外基准测试（建议）

你的测试只验证了正确性，未验证速度。

要确认融合内核实际高效运行：

```python
import time
import torch

torch.cuda.synchronize()

start = time.time()

for _ in range(100):
    out = flash_attn_func(q, k, v, causal=True)

torch.cuda.synchronize()

elapsed = time.time() - start

print("100 iterations:", elapsed)
print("ms/iter:", elapsed * 1000 / 100)
```

与 PyTorch 的标准注意力对比：

```python
torch.nn.functional.scaled_dot_product_attention
```

在 MI300X 上，对于长序列，FlashAttention 2 通常明显更快且占用更少内存。

---

如果以下所有步骤都成功：

```text
flash_attn_func imported OK
FA2 forward pass: OK
FA2 sliding window: OK
HAS_FA2: True
USE_FA2: True
```

则表明 FlashAttention 2 不仅已安装，而且实际上已在你的 MI300X 上成功执行注意力内核，并且 NanoChat 可以在训练期间使用它。