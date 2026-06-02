---
audio: false
generated: true
lang: en
layout: post
title: Gram-Schmidt Process
translated: false
type: note
---

The **Gram-Schmidt process** is a method for orthonormalizing a set of linearly independent vectors in an inner product space (typically \\(\mathbb{R}^n\\) or \\(\mathbb{C}^n\\)). It converts a given basis into an **orthonormal basis**, where the vectors are mutually orthogonal and have unit length.

---

### **Algorithm: Gram-Schmidt Process**

Given a set of **linearly independent** vectors \\( \{v_1, v_2, \dots, v_n\} \\) in an inner product space, we construct an **orthonormal basis** \\( \{u_1, u_2, \dots, u_n\} \\) as follows:

1. **Step 1: Compute the first orthonormal vector**
   \\[
   u_1 = \frac{v_1}{\|v_1\|}
   \\]

2. **Step 2: Make the second vector orthogonal to the first and normalize it**
   \\[
   v_2' = v_2 - \text{proj}_{u_1}(v_2) = v_2 - \frac{\langle v_2, u_1 \rangle}{\langle u_1, u_1 \rangle} u_1
   \\]
   \\[
   u_2 = \frac{v_2'}{\|v_2'\|}
   \\]

3. **Step 3: Repeat for the remaining vectors**
   For \\( k = 3, \dots, n \\):
   \\[
   v_k' = v_k - \sum_{j=1}^{k-1} \frac{\langle v_k, u_j \rangle}{\langle u_j, u_j \rangle} u_j
   \\]
   \\[
   u_k = \frac{v_k'}{\|v_k'\|}
   \\]

Here, \\( \text{proj}_{u_j}(v_k) = \frac{\langle v_k, u_j \rangle}{\langle u_j, u_j \rangle} u_j \\) represents the projection of \\( v_k \\) onto \\( u_j \\).

---

### **Example: Applying Gram-Schmidt to \\(\mathbb{R}^3\\)**

Given the vectors:

\\[
v_1 = (1, 1, 0), \quad v_2 = (1, 0, 1), \quad v_3 = (0, 1, 1)
\\]

#### **Step 1: Normalize \\( v_1 \\)**

\\[
u_1 = \frac{v_1}{\|v_1\|} = \frac{(1,1,0)}{\sqrt{2}} = \left(\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, 0\right)
\\]

#### **Step 2: Orthogonalize \\( v_2 \\) against \\( u_1 \\)**

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

#### **Step 3: Orthogonalize \\( v_3 \\) against \\( u_1 \\) and \\( u_2 \\)**

Follow the same procedure for \\( v_3 \\), projecting onto \\( u_1 \\) and \\( u_2 \\), then normalizing.

---

### **Summary**

The **Gram-Schmidt process** transforms a set of linearly independent vectors into an **orthonormal basis** step by step, ensuring each vector is orthogonal to the previous ones and has unit length. This process is fundamental in applications such as:

- QR decomposition in numerical linear algebra.
- Constructing orthonormal bases for function spaces in Fourier analysis.
- Improving numerical stability in computational algorithms.

Let me know if you'd like me to work through the full example explicitly or clarify any part! 🚀
