---
audio: false
generated: true
lang: zh
layout: post
title: 线性独立性证明
translated: true
type: note
---

23. 已知向量 \\( \alpha_1, \alpha_2, \alpha_3 \\) 线性无关，且向量 \\( \beta_1 = \alpha_1 + 2\alpha_2 \\)，\\( \beta_2 = -\alpha_1 + \alpha_2 - 3\alpha_3 \\)，\\( \beta_3 = 3\alpha_1 + 6\alpha_3 \\)。证明向量 \\( \beta_1, \beta_2, \beta_3 \\) 线性相关。

### 解答

要证明向量 \\( \beta_1, \beta_2, \beta_3 \\) 线性相关，需证明存在不全为零的标量 \\( c_1, c_2, c_3 \\) 使得：

\\[ c_1 \beta_1 + c_2 \beta_2 + c_3 \beta_3 = 0 \\]

已知：
\\[ \beta_1 = \alpha_1 + 2\alpha_2 \\]
\\[ \beta_2 = -\alpha_1 + \alpha_2 - 3\alpha_3 \\]
\\[ \beta_3 = 3\alpha_1 + 6\alpha_3 \\]

需找到常数 \\( c_1, c_2, c_3 \\) 使得：

\\[ c_1 (\alpha_1 + 2\alpha_2) + c_2 (-\alpha_1 + \alpha_2 - 3\alpha_3) + c_3 (3\alpha_1 + 6\alpha_3) = 0 \\]

整理得：

\\[ (c_1 - c_2 + 3c_3)\alpha_1 + (2c_1 + c_2)\alpha_2 + (-3c_2 + 6c_3)\alpha_3 = 0 \\]

由于 \\( \alpha_1, \alpha_2, \alpha_3 \\) 线性无关，\\( \alpha_1, \alpha_2, \alpha_3 \\) 的系数必须均为零：

1. \\( c_1 - c_2 + 3c_3 = 0 \\)
2. \\( 2c_1 + c_2 = 0 \\)
3. \\( -3c_2 + 6c_3 = 0 \\)

解此方程组：

由方程2得：
\\[ 2c_1 + c_2 = 0 \implies c_2 = -2c_1 \\]

由方程3得：
\\[ -3c_2 + 6c_3 = 0 \implies -3(-2c_1) + 6c_3 = 0 \implies 6c_1 + 6c_3 = 0 \implies c_3 = -c_1 \\]

将 \\( c_2 = -2c_1 \\) 和 \\( c_3 = -c_1 \\) 代入方程1：
\\[ c_1 - (-2c_1) + 3(-c_1) = 0 \implies c_1 + 2c_1 - 3c_1 = 0 \implies 0 = 0 \\]

此式对任意 \\( c_1 \\) 均成立。取 \\( c_1 = 1 \\)：

则：
\\[ c_2 = -2 \\]
\\[ c_3 = -1 \\]

因此存在常数 \\( c_1 = 1, c_2 = -2, c_3 = -1 \\) 使得：

\\[ 1 \cdot \beta_1 - 2 \cdot \beta_2 - 1 \cdot \beta_3 = 0 \\]

这证明了向量 \\( \beta_1, \beta_2, \beta_3 \\) 线性相关。
