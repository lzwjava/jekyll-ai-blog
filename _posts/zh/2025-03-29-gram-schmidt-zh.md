---
audio: false
generated: true
lang: zh
layout: post
title: Gram-Schmidt正交化方法
translated: true
type: note
---

**Gram-Schmidt 正交化方法**是线性代数中的一种方法，用于将一组线性无关的向量转换为生成相同子空间的正交归一向量组。这在许多应用中特别有用，例如 QR 分解、求解最小二乘问题以及简化向量空间中的计算。

### **关键概念**

- **线性无关向量**：不能表示为彼此线性组合的向量。
- **正交向量**：彼此垂直的向量，即它们的点积为零。
- **正交归一集**：一组既正交又为单位长度（范数等于 1）的向量。

### **Gram-Schmidt 过程的目的**

- **正交化**：将一组向量转换为其中每个向量都与其他向量正交的集合。
- **归一化**：调整每个向量的长度，使其成为单位向量。
- **简化**：在向量空间中的投影、分解和变换中促进更简便的计算。

### **过程详解**

给定内积空间（如 \\( \mathbb{R}^n \\)）中的一组线性无关向量 \\( \{ \mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_n \} \\)，Gram-Schmidt 过程按照以下步骤构建一个正交归一集 \\( \{ \mathbf{q}_1, \mathbf{q}_2, \ldots, \mathbf{q}_n \} \\)：

1. **初始化第一个向量**：
   \\[
   \mathbf{u}_1 = \mathbf{v}_1
   \\]
   归一化得到：
   \\[
   \mathbf{q}_1 = \frac{\mathbf{u}_1}{\| \mathbf{u}_1 \|}
   \\]

2. 对 \\( k = 2 \\) 到 \\( n \\) 进行**迭代正交化与归一化**：
   - **正交化**：
     \\[
     \mathbf{u}_k = \mathbf{v}_k - \sum_{j=1}^{k-1} \text{proj}_{\mathbf{q}_j} \mathbf{v}_k
     \\]
     其中投影 \\( \text{proj}_{\mathbf{q}_j} \mathbf{v}_k \\) 计算如下：
     \\[
     \text{proj}_{\mathbf{q}_j} \mathbf{v}_k = (\mathbf{v}_k \cdot \mathbf{q}_j) \mathbf{q}_j
     \\]
   - **归一化**：
     \\[
     \mathbf{q}_k = \frac{\mathbf{u}_k}{\| \mathbf{u}_k \|}
     \\]

### **详细步骤**

1. **计算 \\( \mathbf{u}_1 \\) 和 \\( \mathbf{q}_1 \\)**：
   - \\( \mathbf{u}_1 = \mathbf{v}_1 \\)
   - \\( \mathbf{q}_1 = \frac{\mathbf{u}_1}{\| \mathbf{u}_1 \|} \\)

2. **对于每个后续向量 \\( \mathbf{v}_k \\)**：
   - **减去在所有先前 \\( \mathbf{q}_j \\) 上的投影**：
     \\[
     \mathbf{u}_k = \mathbf{v}_k - \sum_{j=1}^{k-1} (\mathbf{v}_k \cdot \mathbf{q}_j) \mathbf{q}_j
     \\]
   - **归一化 \\( \mathbf{u}_k \\) 得到 \\( \mathbf{q}_k \\)**：
     \\[
     \mathbf{q}_k = \frac{\mathbf{u}_k}{\| \mathbf{u}_k \|}
     \\]

### **示例**

让我们将 Gram-Schmidt 过程应用于 \\( \mathbb{R}^2 \\) 中的向量 \\( \mathbf{v}_1 = [1, 1] \\) 和 \\( \mathbf{v}_2 = [1, 0] \\)。

1. **第一个向量**：
   - \\( \mathbf{u}_1 = \mathbf{v}_1 = [1, 1] \\)
   - 归一化：
     \\[
     \| \mathbf{u}_1 \| = \sqrt{1^2 + 1^2} = \sqrt{2}
     \\]
     \\[
     \mathbf{q}_1 = \frac{[1, 1]}{\sqrt{2}} = \left[ \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}} \right]
     \\]

2. **第二个向量**：
   - 计算 \\( \mathbf{v}_2 \\) 在 \\( \mathbf{q}_1 \\) 上的投影：
     \\[
     \text{proj}_{\mathbf{q}_1} \mathbf{v}_2 = (\mathbf{v}_2 \cdot \mathbf{q}_1) \mathbf{q}_1
     \\]
     \\[
     \mathbf{v}_2 \cdot \mathbf{q}_1 = [1, 0] \cdot \left[ \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}} \right] = \frac{1}{\sqrt{2}}
     \\]
     \\[
     \text{proj}_{\mathbf{q}_1} \mathbf{v}_2 = \frac{1}{\sqrt{2}} \left[ \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}} \right] = \left[ \frac{1}{2}, \frac{1}{2} \right]
     \\]
   - 减去投影：
     \\[
     \mathbf{u}_2 = \mathbf{v}_2 - \text{proj}_{\mathbf{q}_1} \mathbf{v}_2 = [1, 0] - \left[ \frac{1}{2}, \frac{1}{2} \right] = \left[ \frac{1}{2}, -\frac{1}{2} \right]
     \\]
   - 归一化 \\( \mathbf{u}_2 \\)：
     \\[
     \| \mathbf{u}_2 \| = \sqrt{\left( \frac{1}{2} \right)^2 + \left( -\frac{1}{2} \right)^2} = \frac{1}{\sqrt{2}}
     \\]
     \\[
     \mathbf{q}_2 = \frac{\left[ \frac{1}{2}, -\frac{1}{2} \right]}{\frac{1}{\sqrt{2}}} = \left[ \frac{\sqrt{2}}{2}, -\frac{\sqrt{2}}{2} \right]
     \\]

### **结果**

正交归一集为：
\\[
\mathbf{q}_1 = \left[ \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}} \right], \quad \mathbf{q}_2 = \left[ \frac{\sqrt{2}}{2}, -\frac{\sqrt{2}}{2} \right]
\\]

这些向量是正交的 (\\( \mathbf{q}_1 \cdot \mathbf{q}_2 = 0 \\))，并且是单位长度 (\\( \| \mathbf{q}_1 \| = \| \mathbf{q}_2 \| = 1 \\))。

### **应用**

- **QR 分解**：将矩阵分解为正交矩阵 \\( Q \\) 和上三角矩阵 \\( R \\)。
- **最小二乘问题**：为超定系统寻找最佳近似解。
- **数值方法**：提高计算算法的稳定性和效率。

### **总结**

Gram-Schmidt 过程是在内积空间中对一组向量进行正交归一化的系统方法，确保新向量集更易于处理，同时保持原始向量的生成空间。它是线性代数的基础，在数学、物理和工程领域具有广泛的应用。
