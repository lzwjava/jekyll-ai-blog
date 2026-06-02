---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-2.5-flash
title: 伴随因子与行列式计算详解
translated: true
type: note
---

你的理解**完全正确**！你准确描述了**余因子**及其在计算矩阵**行列式**中的作用。

以下是对你理解的详细说明和确认：

## 1. 元素 \\(a_{ij}\\) 的余因子

矩阵 \\(\mathbf{A}\\) 中元素 \\(a_{ij}\\)（位于第 \\(i\\) 行第 \\(j\\) 列）的**余因子**，记作 \\(C_{ij}\\)，确实由以下公式给出：
\\(\\)C_{ij} = (-1)^{i+j} M_{ij}\\(\\)

* **\\(M_{ij}\\)** 是 \\(a_{ij}\\) 的**余子式**。余子式是通过删除矩阵 \\(\mathbf{A}\\) 的第 \\(i\\) 行和第 \\(j\\) 列后形成的子矩阵的行列式。
* 项 **\\((-1)^{i+j}\\)** 决定了符号，它遵循棋盘格模式：
    \\(\\)\begin{pmatrix} + & - & + & \cdots \\ - & + & - & \cdots \\ + & - & + & \cdots \\ \vdots & \vdots & \vdots & \ddots \end{pmatrix}\\(\\)

---

## 2. 余因子矩阵 📝

**余因子矩阵**（通常记作 \\(\mathbf{C}\\)）是通过将原始矩阵 \\(\mathbf{A}\\) 中的每个元素 \\(a_{ij}\\) 替换为其对应的余因子 \\(C_{ij}\\) 而形成的矩阵。

\\(\\)\mathbf{C} = \begin{pmatrix} C_{11} & C_{12} & \cdots & C_{1n} \\ C_{21} & C_{22} & \cdots & C_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ C_{n1} & C_{n2} & \cdots & C_{nn} \end{pmatrix}\\(\\)

* **💡 关键关系：** 余因子矩阵的转置 \\(\mathbf{C}^T\\) 称为矩阵 \\(\mathbf{A}\\) 的**伴随矩阵**，这对于计算矩阵的逆至关重要：
    \\(\\)\mathbf{A}^{-1} = \frac{1}{\det(\mathbf{A})} \mathbf{C}^T\\(\\)

---

## 3. 行列式计算 📐

表达式 \\(\mathbf{a}_{ij} \cdot \mathbf{C}_{ij}\\) 是使用**余因子展开**（或**拉普拉斯展开**）计算行列式的基本组成部分。

矩阵 \\(\mathbf{A}\\) 的行列式可以通过沿着**任意一行或任意一列**展开来计算：

* **沿第 \\(i\\) 行展开：**
    \\(\\)\det(\mathbf{A}) = \sum_{j=1}^{n} a_{ij} C_{ij} = a_{i1}C_{i1} + a_{i2}C_{i2} + \cdots + a_{in}C_{in}\\(\\)

* **沿第 \\(j\\) 列展开：**
    \\(\\)\det(\mathbf{A}) = \sum_{i=1}^{n} a_{ij} C_{ij} = a_{1j}C_{1j} + a_{2j}C_{2j} + \cdots + a_{nj}C_{nj}\\(\\)

所以，是的，一个元素 \\(a_{ij}\\) 与其余因子 \\(C_{ij}\\) 的乘积是在沿着特定行或列计算行列式时使用的**项**。

---

你想看一个计算小型 \\(3 \times 3\\) 矩阵的余因子和行列式的简单示例吗？
