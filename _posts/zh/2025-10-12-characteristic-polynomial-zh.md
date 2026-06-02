---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 特征多项式定义与性质
translated: true
type: note
---

在线性代数中，**特征多项式**是描述方阵 \\( A \\)（大小为 \\( n \times n \\)）特征值信息的多项式。其定义为：

\\[
p(\lambda) = \det(A - \lambda I)
\\]

其中：
- \\( A \\) 是 \\( n \times n \\) 矩阵
- \\( \lambda \\) 是标量（多项式变量）
- \\( I \\) 是 \\( n \times n \\) 单位矩阵
- \\( \det \\) 表示行列式

### 核心特性
1. **形式**：特征多项式是首一 \\( n \\) 次多项式，即 \\( \lambda^n \\) 项的系数为 1
   - 对于 \\( 2 \times 2 \\) 矩阵 \\( A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \\)，特征多项式为：
     \\[
     p(\lambda) = \det \begin{bmatrix} a - \lambda & b \\ c & d - \lambda \end{bmatrix} = \lambda^2 - (a + d)\lambda + (ad - bc)
     \\]
     其中 \\( a + d \\) 是迹，\\( ad - bc \\) 是行列式

2. **特征值**：特征方程 \\( p(\lambda) = 0 \\) 的根即为矩阵 \\( A \\) 的特征值，这些根可以是实数或复数

3. **系数关系**：多项式系数与矩阵性质相关：
   - \\( \lambda^{n-1} \\) 的系数为 \\( -\text{trace}(A) \\)
   - 常数项为 \\( (-1)^n \det(A) \\)
   - 其他系数由 \\( A \\) 的主子式之和确定

4. **不变性**：特征多项式在相似变换下保持不变。若 \\( B = P^{-1}AP \\)，则 \\( A \\) 与 \\( B \\) 具有相同的特征多项式

5. **凯莱-哈密顿定理**：矩阵 \\( A \\) 满足其自身的特征多项式，即若 \\( p(\lambda) \\) 是特征多项式，则 \\( p(A) = 0 \\)（零矩阵）

### 示例
对于矩阵 \\( A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \\)：
- 计算 \\( A - \lambda I = \begin{bmatrix} 1 - \lambda & 2 \\ 3 & 4 - \lambda \end{bmatrix} \\)
- 特征多项式为：
  \\[
  p(\lambda) = \det \begin{bmatrix} 1 - \lambda & 2 \\ 3 & 4 - \lambda \end{bmatrix} = (1 - \lambda)(4 - \lambda) - 6 = \lambda^2 - 5\lambda - 2
  \\]
- 通过解方程 \\( \lambda^2 - 5\lambda - 2 = 0 \\) 可得特征值

### 应用场景
- **特征值计算**：通过求解 \\( p(\lambda) = 0 \\) 获得特征值
- **矩阵性质分析**：用于判断矩阵的可对角化性、可逆性等性质
- **微分方程**：在线性微分方程组中用于求解

如需具体示例或进一步说明，请随时告知！
