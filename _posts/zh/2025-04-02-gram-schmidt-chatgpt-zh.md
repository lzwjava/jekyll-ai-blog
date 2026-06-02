---
audio: false
generated: true
lang: zh
layout: post
title: Gram-Schmidt正交化方法
translated: true
type: note
---

**Gram-Schmidt 正交化方法** 是一种在内积空间（通常为 \\(\mathbb{R}^n\\) 或 \\(\mathbb{C}^n\\)）中将一组线性无关向量标准正交化的方法。它将给定基转换为**标准正交基**，使得向量彼此正交且长度为 1。

---

### **算法：Gram-Schmidt 正交化过程**

给定内积空间中一组**线性无关**的向量 \\( \{v_1, v_2, \dots, v_n\} \\)，我们按以下步骤构建**标准正交基** \\( \{u_1, u_2, \dots, u_n\} \\)：

1. **步骤 1：计算第一个标准正交向量**
   \\[
   u_1 = \frac{v_1}{\|v_1\|}
   \\]

2. **步骤 2：使第二个向量与第一个正交并归一化**
   \\[
   v_2' = v_2 - \text{proj}_{u_1}(v_2) = v_2 - \frac{\langle v_2, u_1 \rangle}{\langle u_1, u_1 \rangle} u_1
   \\]
   \\[
   u_2 = \frac{v_2'}{\|v_2'\|}
   \\]

3. **步骤 3：对其余向量重复此过程**
   对于 \\( k = 3, \dots, n \\)：
   \\[
   v_k' = v_k - \sum_{j=1}^{k-1} \frac{\langle v_k, u_j \rangle}{\langle u_j, u_j \rangle} u_j
   \\]
   \\[
   u_k = \frac{v_k'}{\|v_k'\|}
   \\]

其中，\\( \text{proj}_{u_j}(v_k) = \frac{\langle v_k, u_j \rangle}{\langle u_j, u_j \rangle} u_j \\) 表示 \\( v_k \\) 在 \\( u_j \\) 上的投影。

---

### **示例：在 \\(\mathbb{R}^3\\) 中应用 Gram-Schmidt 方法**

给定向量：

\\[
v_1 = (1, 1, 0), \quad v_2 = (1, 0, 1), \quad v_3 = (0, 1, 1)
\\]

#### **步骤 1：归一化 \\( v_1 \\)**

\\[
u_1 = \frac{v_1}{\|v_1\|} = \frac{(1,1,0)}{\sqrt{2}} = \left(\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, 0\right)
\\]

#### **步骤 2：将 \\( v_2 \\) 相对于 \\( u_1 \\) 正交化**

\\[
\text{proj}_{u_1}(v_2) = \frac{\langle v_2, u_1 \rangle}{\langle u_1, u_1 \rangle} u_1
\\]

\\[
= \frac{(1,0,1) \cdot (1/\sqrt{2}, 1/\sqrt{2}, 0)}{1} \cdot (1/\sqrt{2}, 1/\sqrt{2}, 0)
\\]

\\[
= \frac{1 \cdot 1/\sqrt{2} + 0 \cdot 1/\sqrt{2} + 1 \cdot 0}{1} \cdot (1/\sqrt{2}, 1/\sqrt{2}, 0)
\\]

\\[
= \frac{1/\sqrt{2}}{1} \cdot (1/\sqrt{2}, 1/\sqrt{2}, 0) = \left(\frac{1}{2}, \frac{1}{2}, 0\right)
\\]

\\[
v_2' = v_2 - \text{proj}_{u_1}(v_2) = \left(1,0,1\right) - \left(\frac{1}{2}, \frac{1}{2}, 0\right) = \left(\frac{1}{2}, -\frac{1}{2}, 1\right)
\\]

\\[
u_2 = \frac{v_2'}{\|v_2'\|}
\\]

\\[
= \frac{\left(\frac{1}{2}, -\frac{1}{2}, 1\right)}{\sqrt{\left(\frac{1}{2}\right)^2 + \left(-\frac{1}{2}\right)^2 + (1)^2}}
\\]

\\[
= \frac{\left(\frac{1}{2}, -\frac{1}{2}, 1\right)}{\sqrt{\frac{1}{4} + \frac{1}{4} + 1}} = \frac{\left(\frac{1}{2}, -\frac{1}{2}, 1\right)}{\sqrt{\frac{3}{2}}}
\\]

#### **步骤 3：将 \\( v_3 \\) 相对于 \\( u_1 \\) 和 \\( u_2 \\) 正交化**

对 \\( v_3 \\) 遵循相同步骤，先投影到 \\( u_1 \\) 和 \\( u_2 \\) 上，然后归一化。

---

### **总结**

**Gram-Schmidt 正交化方法** 通过逐步将一组线性无关向量转换为**标准正交基**，确保每个向量与之前的所有向量正交且具有单位长度。该方法在以下应用中具有基础性作用：

- 数值线性代数中的 QR 分解。
- 傅里叶分析中为函数空间构建标准正交基。
- 提高计算算法的数值稳定性。

如需我详细演示完整示例或澄清任何部分，请告诉我！🚀
