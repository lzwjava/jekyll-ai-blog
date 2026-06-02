---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-pro-preview
title: 行运算与行列式变化
translated: true
type: note
---

这是个很好的问题！让我们来讨论行变换及其对行列式的影响。

## 📐 达成行阶梯形(REF)

您说得对，**交换行**、**某行乘以标量**和**将一行的倍数加到另一行**正是用于达成**行阶梯形(REF)** 的三种基本行变换。

---

## 🛑 行变换对行列式的影响

您关于矩阵行列式在这些操作过程中**不改变**的说法是**部分错误的**。只有三种基本行变换中的一种会保持行列式不变：

### 1. 将一行的倍数加到另一行

* **操作：** \\(R_i \leftarrow R_i + c R_j\\)
* **对行列式的影响：** 行列式**不**改变。
  * 如果 \\(\det(A) = d\\)，那么 \\(\det(A') = d\\)。
  * **示例：** \\(\det \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} = -2\\)。\\(\det \begin{pmatrix} 1 & 2 \\ 3-2(1) & 4-2(2) \end{pmatrix} = \det \begin{pmatrix} 1 & 2 \\ 1 & 0 \end{pmatrix} = -2\\)。

### 2. 某行乘以非零标量

* **操作：** \\(R_i \leftarrow c R_i\\) (其中 \\(c \ne 0\\))
* **对行列式的影响：** 行列式乘以标量 \\(c\\)。
  * 如果 \\(\det(A) = d\\)，那么 \\(\det(A') = c \cdot d\\)。
  * **示例：** \\(\det \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} = -2\\)。\\(\det \begin{pmatrix} 1 & 2 \\ 3(2) & 4(2) \end{pmatrix} = \det \begin{pmatrix} 1 & 2 \\ 6 & 8 \end{pmatrix} = 8-12 = -4\\)。这里，\\(c=2\\)，新的行列式是 \\(2 \cdot (-2) = -4\\)。

### 3. 交换两行

* **操作：** \\(R_i \leftrightarrow R_j\\)
* **对行列式的影响：** 行列式乘以 \\(-1\\) (符号改变)。
  * 如果 \\(\det(A) = d\\)，那么 \\(\det(A') = -d\\)。
  * **示例：** \\(\det \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} = -2\\)。\\(\det \begin{pmatrix} 3 & 4 \\ 1 & 2 \end{pmatrix} = 3(2) - 4(1) = 6-4 = 2\\)。这里，符号从 \\(-2\\) 变为 \\(2\\)。

---

## 💡 总结表格

| 基本行变换 | 符号表示 | 对行列式的影响 |
| :--- | :--- | :--- |
| **行交换** | \\(R_i \leftrightarrow R_j\\) | \\(\det(A') = -\det(A)\\) |
| **标量乘法** | \\(R_i \leftarrow c R_i\\) | \\(\det(A') = c \cdot \det(A)\\) |
| **行加法** | \\(R_i \leftarrow R_i + c R_j\\) | \\(\det(A') = \det(A)\\) |

如果您使用行变换将矩阵 \\(A\\) 转换为其行阶梯形 \\(U\\)，您可以通过跟踪这些变化来找到原始行列式：

\\(\\)\det(A) = (-1)^s \cdot \frac{1}{c_1 c_2 \dots c_k} \cdot \det(U)\\(\\)

其中 \\(s\\) 是行交换的次数，\\(c_1, c_2, \dots, c_k\\) 是行乘法中使用的标量。对于 REF 中的矩阵，\\(\det(U)\\) 就是其对角线元素的乘积（因为它是上三角矩阵）。

---

您想尝试在一个具体的矩阵上使用这些运算来求其行列式吗？
