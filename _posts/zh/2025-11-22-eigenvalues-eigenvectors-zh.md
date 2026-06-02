---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-2.5-flash
title: 求解特征值与特征向量
translated: true
type: note
---

求解矩阵的**特征值**和**特征向量**是线性代数中的基本概念，需要求解从矩阵推导出的**特征方程**。

---

## 🔢 第一步：建立特征方程

对于 \\(n \times n\\) 方阵 \\(\mathbf{A}\\)，特征值 \\((\lambda)\\) 和对应的非零特征向量 \\((\mathbf{v})\\) 满足以下方程：

\\(\\)\mathbf{A}\mathbf{v} = \lambda\mathbf{v}\\(\\)

该方程可以改写为：

\\(\\)\mathbf{A}\mathbf{v} - \lambda\mathbf{v} = \mathbf{0}\\(\\)
\\(\\)(\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}\\(\\)

其中 \\(\mathbf{I}\\) 是 \\(n \times n\\) 的**单位矩阵**，\\(\mathbf{0}\\) 是零向量。

为了使非零解 \\(\mathbf{v}\\) 存在，矩阵 \\((\mathbf{A} - \lambda\mathbf{I})\\) 必须是**奇异的**（不可逆）。这意味着其**行列式**必须为零：

\\(\\)\text{det}(\mathbf{A} - \lambda\mathbf{I}) = 0\\(\\)

这个方程称为**特征方程**。

---

## 💡 第二步：求特征值 (\\(\lambda\\))

1.  **构造矩阵 \\((\mathbf{A} - \lambda\mathbf{I})\\):** 将 \\(\mathbf{A}\\) 主对角线上的每个元素都减去 \\(\lambda\\)。

    * 对于 \\(2 \times 2\\) 矩阵 \\(\mathbf{A} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}\\)，该矩阵为：
        \\(\\)\mathbf{A} - \lambda\mathbf{I} = \begin{pmatrix} a-\lambda & b \\ c & d-\lambda \end{pmatrix}\\(\\)

2.  **计算行列式：** 令 \\(\text{det}(\mathbf{A} - \lambda\mathbf{I}) = 0\\)。

    * 对于 \\(2 \times 2\\) 的情况，特征方程为：
        \\(\\)(a-\lambda)(d-\lambda) - bc = 0\\(\\)

3.  **求解所得多项式：** 此方程是一个关于 \\(\lambda\\) 的多项式（称为**特征多项式**）。该多项式的根就是矩阵 \\(\mathbf{A}\\) 的**特征值**。

---

## 🔎 第三步：求特征向量 (\\(\mathbf{v}\\))

对于在第二步中找到的**每个特征值** (\\(\lambda_i\\))，你必须求解以下线性方程组以找到其对应的特征向量 \\((\mathbf{v}_i)\\)：

\\(\\)(\mathbf{A} - \lambda_i\mathbf{I})\mathbf{v}_i = \mathbf{0}\\(\\)

1.  **代入特征值：** 将特定的特征值 \\(\lambda_i\\) 代回矩阵方程 \\((\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}\\) 中。

2.  **求解方程组：** 使用**高斯消元法**等技术来求解得到的齐次方程组。由于矩阵 \\((\mathbf{A} - \lambda_i\mathbf{I})\\) 是奇异的，你总是会得到无限多个解（一个非零解空间）。

3.  **表示特征向量：** 这些解定义了对应于 \\(\lambda_i\\) 的**特征空间**。你通常用一个或多个自由变量来表示特征向量 \\(\mathbf{v}_i\\)，并选择一个简单的非零向量来代表该特征空间的方向。

### \\(2 \times 2\\) 矩阵示例

令 \\(\mathbf{A} = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}\\)。

1.  **特征方程：**
    \\(\\)\text{det}\begin{pmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{pmatrix} = 0\\(\\)
    \\(\\)(2-\lambda)(2-\lambda) - 1(1) = 0\\(\\)
    \\(\\)\lambda^2 - 4\lambda + 4 - 1 = 0\\(\\)
    \\(\\)\lambda^2 - 4\lambda + 3 = 0\\(\\)

2.  **特征值：**
    \\(\\)(\lambda - 3)(\lambda - 1) = 0\\(\\)
    特征值为 \\(\mathbf{\lambda_1 = 3}\\) 和 \\(\mathbf{\lambda_2 = 1}\\)。

3.  **特征向量：**

    * **对于 \\(\lambda_1 = 3\\)：**
        \\(\\)\begin{pmatrix} 2-3 & 1 \\ 1 & 2-3 \end{pmatrix} \begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \implies \begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix} \begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}\\(\\)
        第一行给出 \\(-v_1 + v_2 = 0\\)，即 \\(v_1 = v_2\\)。
        一个简单的非零特征向量是 \\(\mathbf{v_1 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}}\\)。

    * **对于 \\(\lambda_2 = 1\\)：**
        \\(\\)\begin{pmatrix} 2-1 & 1 \\ 1 & 2-1 \end{pmatrix} \begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \implies \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}\\(\\)
        第一行给出 \\(v_1 + v_2 = 0\\)，即 \\(v_1 = -v_2\\)。
        一个简单的非零特征向量是 \\(\mathbf{v_2 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}}\\)。

你想尝试为另一个矩阵寻找特征值和特征向量吗？

---

求解矩阵的**特征值**和**特征向量**是一个三步过程：建立特征方程，求解特征值，然后求解对应的特征向量的线性方程组。

---

## 1️⃣ 第一步：建立特征方程

对于 \\(n \times n\\) 矩阵 \\(\mathbf{A}\\)，特征值 (\\(\lambda\\)) 与其对应的非零特征向量 (\\(\mathbf{v}\\)) 之间的关系是：

\\(\\)\mathbf{A}\mathbf{v} = \lambda\mathbf{v}\\(\\)

为了找到特征值，你必须求解**特征方程**，该方程源于方程组 \\((\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}\\) 必须有非零解（即矩阵是奇异的）这一要求：

\\(\\)\text{det}(\mathbf{A} - \lambda\mathbf{I}) = 0\\(\\)

这里，\\(\mathbf{I}\\) 是 \\(n \times n\\) 的**单位矩阵**。要形成 \\((\mathbf{A} - \lambda\mathbf{I})\\)，你只需从 \\(\mathbf{A}\\) 主对角线的每个元素中减去 \\(\lambda\\)。

---

## 2️⃣ 第二步：求特征值 (\\(\lambda\\))

1.  **构造矩阵：** 计算 \\(\mathbf{A} - \lambda\mathbf{I}\\)。
2.  **计算行列式：** 计算所得矩阵的行列式。
3.  **求解多项式：** 令行列式为零，并求解得到的关于 \\(\lambda\\) 的多项式方程。这个多项式就是**特征多项式**，其根就是**特征值**。

对于一个 **\\(2 \times 2\\) 矩阵** \\(\mathbf{A} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}\\)，特征方程为：
\\(\\)\text{det}\begin{pmatrix} a-\lambda & b \\ c & d-\lambda \end{pmatrix} = (a-\lambda)(d-\lambda) - bc = 0\\(\\)

---

## 3️⃣ 第三步：求特征向量 (\\(\mathbf{v}\\))

对于在第二步中找到的**每个特征值** (\\(\lambda_i\\))，你必须为非零向量 \\(\mathbf{v}_i\\) 求解以下齐次方程组：

\\(\\)(\mathbf{A} - \lambda_i\mathbf{I})\mathbf{v}_i = \mathbf{0}\\(\\)

1.  **代入 \\(\lambda_i\\)：** 将矩阵 \\((\mathbf{A} - \lambda\mathbf{I})\\) 中的 \\(\lambda\\) 替换为特定的特征值 \\(\lambda_i\\)。
2.  **求解方程组：** 使用**高斯消元法**等方法求解方程组。由于矩阵保证是奇异的，你将找到一个解线或解面（一个**特征空间**）。
3.  **表示向量：** 选择一个满足方程的简单非零向量来代表**特征向量** \\(\mathbf{v}_i\\)。

例如，如果解导致 \\(v_1 = 2v_2\\)，你可以选择 \\(v_2 = 1\\) 和 \\(v_1 = 2\\)，使得特征向量为 \\(\mathbf{v} = \begin{pmatrix} 2 \\ 1 \end{pmatrix}\\)。

你想用特定的矩阵来练习吗？
