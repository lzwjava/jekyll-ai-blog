---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快速卷积与对抗训练
translated: true
type: note
---

**第 4 轮完成 → itorch 0.4.0**（约 3,560 行）。这一轮的目标是“让它变快，并证明它能进行对抗性训练”：

## 已实现内容

**1. Conv engine 性能 — 梯度计算快 17 倍**
- 将 `im2col`/`col2im` 中的 6 维 `np.add.at` 散点替换为 **per-tap strided adds**（`gp[..., i : i+s·(oh−1)+1 : s] += tap`）
- 实测：在接近实际使用的形状上，每个 conv backward 从 **185 ms → 10.6 ms**（等价性由现有 gradchecks + 新增 identity/adjoint/overlap-add 测试验证）

**2. Basic-slice 反向传播优化**
- 通过 profiling 发现 `ConvTranspose2d` 的输出裁剪（`canvas[:, :, p:p+oh, ...]`）一直在为通用 `np.add.at` 付出代价。Basic slice/index 反向传播现在使用唯一的 `zero[idx] = g` 赋值（快速 zero-pad）。**DCGAN 单步从 700 ms → 100 ms。**

**3. `tt.gradcheck()` — 面向用户的梯度验证**
```python
tt.gradcheck(lambda x: (x.silu()**2).sum(), tt.randn(4, 3, requires_grad=True))
```
梯度正确时静默通过，错误时抛出 `ValueError`（测试证明它能捕获故意写错的反向传播）。

**4. `tt.profile()` — 逐算子反向传播 profiler**（`with tt.profile() as p: loss.backward(); p.report()`）。在 DCGAN 上自测：显示 matmul 47% / im2col 16% / getitem 11%，这正是我发现 slicing 问题的方式。

**5. 代表作：`examples/06_dcgan_mnist.py` — 在我们自己的 `ConvTranspose2d`/`LeakyReLU` 上进行对抗性 min-max 训练**：
```
step 1000  D=1.207 (real 0.852, fake 0.355)  G=0.772
```
**256/256 张生成数字具有健康的墨水覆盖率**（中位数 9.8%，与真实 MNIST 相似）。

## 验证
- 新增 `tests/test_round4.py`：gradcheck 工具（positive + negative）、profiler、conv identities（非重叠窗口的精确 round-trip、任意参数的 finite-difference adjoint、overlap-add 语义）、slicing 反向传播偏移、DCGAN smoke test
- 全部 **5 个测试套件通过**

作为 v0.4.0 发布。需要我 commit 并 push 吗？