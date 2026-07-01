---
audio: false
generated: true
lang: zh
layout: post
title: 线性变换
translated: true
type: note
---

**定义、示例、矩阵表示、核、像、性质（单射性、满射性）**

线性变换是线性代数中的基础概念，在向量空间与矩阵之间架起了桥梁。本教程涵盖：

- 线性变换的**定义**
- 常见线性变换的**示例**
- 线性变换的**矩阵表示**
- **核（零空间）**与**像（值域）**
- **性质**：单射性（一对一）与满射性（满射）

---

## **1. 线性变换的定义**

设 \\( V \\) 和 \\( W \\) 是域 \\( \mathbb{F} \\)（通常为 \\( \mathbb{R} \\) 或 \\( \mathbb{C} \\)）上的两个向量空间，**线性变换**（或线性映射）\\( T: V \to W \\) 是一个满足以下条件的函数：

1. **可加性**：
   \\[
   T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v}) \quad \forall \mathbf{u}, \mathbf{v} \in V
   \\]
2. **齐次性（标量乘法）**：
   \\[
   T(c \mathbf{v}) = c T(\mathbf{v}) \quad \forall c \in \mathbb{F}, \mathbf{v} \in V
   \\]

**核心思想**：线性变换保持向量加法与标量乘法。

---

## **2. 线性变换示例**

### **(a) 零变换**

- 对所有 \\( \mathbf{v} \in V \\)，\\( T(\mathbf{v}) = \mathbf{0} \\)。

### **(b) 恒等变换**

- 对所有 \\( \mathbf{v} \in V \\)，\\( T(\mathbf{v}) = \mathbf{v} \\)。

### **(c) \\( \mathbb{R}^2 \\) 中的旋转**

- 将向量旋转角度 \\( \theta \\)：
  \\[
  T \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix}
  \\]

### **(d) 微分（多项式空间）**

- \\( T: P_n \to P_{n-1} \\)，其中 \\( T(p(x)) = p'(x) \\)。

### **(e) 矩阵乘法**

- 对于固定的 \\( m \times n \\) 矩阵 \\( A \\)，\\( T: \mathbb{R}^n \to \mathbb{R}^m \\) 定义为 \\( T(\mathbf{x}) = A\mathbf{x} \\)。

---

## **3. 线性变换的矩阵表示**

每个线性变换 \\( T: \mathbb{R}^n \to \mathbb{R}^m \\) 都可以用一个 \\( m \times n \\) 矩阵 \\( A \\) 表示，使得：
\\[
T(\mathbf{x}) = A\mathbf{x}
\\]

### **如何求矩阵 \\( A \\)**

1. 将 \\( T \\) 作用于 \\( \mathbb{R}^n \\) 的标准基向量 \\( \mathbf{e}_1, \mathbf{e}_2, \dots, \mathbf{e}_n \\)。
2. \\( A \\) 的列即为 \\( T(\mathbf{e}_1), T(\mathbf{e}_2), \dots, T(\mathbf{e}_n) \\)。

**示例**：
设 \\( T: \mathbb{R}^2 \to \mathbb{R}^2 \\) 定义为：
\\[
T \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 2x + y \\ x - 3y \end{pmatrix}
\\]

- 计算 \\( T(\mathbf{e}_1) = T(1, 0) = (2, 1) \\)
- 计算 \\( T(\mathbf{e}_2) = T(0, 1) = (1, -3) \\)
- 因此，矩阵 \\( A \\) 为：
  \\[
  A = \begin{pmatrix} 2 & 1 \\ 1 & -3 \end{pmatrix}
  \\]

---

## **4. 核（零空间）与像（值域）**

### **(a) 核（零空间）**

\\( T \\) 的**核**是 \\( V \\) 中所有映射到 \\( \mathbf{0} \\) 的向量集合：
\\[
\ker(T) = \{ \mathbf{v} \in V \mid T(\mathbf{v}) = \mathbf{0} \}
\\]

**性质**：

- \\( \ker(T) \\) 是 \\( V \\) 的子空间。
- \\( T \\) 是**单射（一对一）**当且仅当 \\( \ker(T) = \{ \mathbf{0} \} \\)。

**示例**：
对于 \\( T(\mathbf{x}) = A\mathbf{x} \\)，其中 \\( A = \begin{pmatrix} 1 & 2 \\ 3 & 6 \end{pmatrix} \\)，
\\[
\ker(T) = \text{Span} \left\{ \begin{pmatrix} -2 \\ 1 \end{pmatrix} \right\}
\\]

### **(b) 像（值域）**

\\( T \\) 的**像**是 \\( W \\) 中所有输出的集合：
\\[
\text{Im}(T) = \{ T(\mathbf{v}) \mid \mathbf{v} \in V \}
\\]

**性质**：

- \\( \text{Im}(T) \\) 是 \\( W \\) 的子空间。
- \\( T \\) 是**满射（满射）**当且仅当 \\( \text{Im}(T) = W \\)。

**示例**：
对于 \\( T(\mathbf{x}) = A\mathbf{x} \\)，其中 \\( A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{pmatrix} \\)，
\\[
\text{Im}(T) = \text{Span} \left\{ \begin{pmatrix} 1 \\ 0 \\ 1 \end{pmatrix}, \begin{pmatrix} 0 \\ 1 \\ 1 \end{pmatrix} \right\}
\\]

---

## **5. 性质：单射性与满射性**

### **(a) 单射性（一对一）**

线性变换 \\( T \\) 是**单射**，如果：
\\[
T(\mathbf{u}) = T(\mathbf{v}) \implies \mathbf{u} = \mathbf{v}
\\]
**检验方法**：

- \\( T \\) 是单射 \\( \iff \ker(T) = \{ \mathbf{0} \} \\)。
- 若 \\( \dim(V) < \dim(W) \\)，则 \\( T \\) 可能不是单射。

### **(b) 满射性（满射）**

线性变换 \\( T \\) 是**满射**，如果：
\\[
\forall \mathbf{w} \in W, \exists \mathbf{v} \in V \text{ 使得 } T(\mathbf{v}) = \mathbf{w}
\\]
**检验方法**：

- \\( T \\) 是满射 \\( \iff \text{Im}(T) = W \\)。
- 若 \\( \dim(V) > \dim(W) \\)，则 \\( T \\) 可能不是满射。

### **(c) 秩-零化度定理**

对于 \\( T: V \to W \\)，
\\[
\dim(V) = \dim(\ker(T)) + \dim(\text{Im}(T))
\\]

- **秩** \\( = \dim(\text{Im}(T)) \\)
- **零化度** \\( = \dim(\ker(T)) \\)

**示例**：
若 \\( T: \mathbb{R}^3 \to \mathbb{R}^2 \\) 满足 \\( \dim(\ker(T)) = 1 \\)，则 \\( \dim(\text{Im}(T)) = 2 \\)。

---

## **总结**

| 概念 | 定义 | 关键性质 |
| ------ | ------ | ---------- |
| **线性变换** | \\( T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v}) \\) 且 \\( T(c\mathbf{v}) = cT(\mathbf{v}) \\) | 保持线性结构 |
| **矩阵表示** | \\( T(\mathbf{x}) = A\mathbf{x} \\)，其中 \\( A \\) 的列为 \\( T(\mathbf{e}_i) \\) | 编码变换 |
| **核** | \\( \ker(T) = \{ \mathbf{v} \mid T(\mathbf{v}) = \mathbf{0} \} \\) | 衡量单射性 |
| **像** | \\( \text{Im}(T) = \{ T(\mathbf{v}) \mid \mathbf{v} \in V \} \\) | 衡量满射性 |
| **单射性** | \\( \ker(T) = \{ \mathbf{0} \} \\) | 一对一 |
| **满射性** | \\( \text{Im}(T) = W \\) | 满射 |

---

## **练习题**

1. 求 \\( T(x, y, z) = (2x - y, y + 3z) \\) 的矩阵表示。
2. 判断 \\( T(\mathbf{x}) = \begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix} \mathbf{x} \\) 是否为单射/满射。
3. 计算 \\( T(x, y) = (x + y, 2x - y, x) \\) 的 \\( \ker(T) \\) 和 \\( \text{Im}(T) \\)。

---

本教程涵盖了本科线性代数课程中通常教授的线性变换核心概念。如需进一步说明或更多示例，请告知！
