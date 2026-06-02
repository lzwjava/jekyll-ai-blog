---
audio: false
generated: true
lang: en
layout: post
title: Gram-Schmidt Process
translated: false
type: note
---

The **Gram-Schmidt process** is a method in linear algebra used to convert a set of linearly independent vectors into an orthonormal set of vectors that span the same subspace. This is particularly useful in various applications such as QR decomposition, solving least squares problems, and simplifying computations in vector spaces.

### **Key Concepts**

- **Linearly Independent Vectors**: Vectors that cannot be expressed as a linear combination of each other.
- **Orthogonal Vectors**: Vectors that are perpendicular to each other, meaning their dot product is zero.
- **Orthonormal Set**: A set of vectors that are both orthogonal and of unit length (norm equals 1).

### **Purpose of the Gram-Schmidt Process**

- **Orthogonalization**: Transforming a set of vectors into a set where each vector is orthogonal to the others.
- **Normalization**: Adjusting the length of each vector to make it a unit vector.
- **Simplification**: Facilitating easier computations in projections, decompositions, and transformations within vector spaces.

### **The Process Explained**

Given a set of linearly independent vectors \\( \{ \mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_n \} \\) in an inner product space (like \\( \mathbb{R}^n \\)), the Gram-Schmidt process constructs an orthonormal set \\( \{ \mathbf{q}_1, \mathbf{q}_2, \ldots, \mathbf{q}_n \} \\) following these steps:

1. **Initialize the First Vector**:
   \\[
   \mathbf{u}_1 = \mathbf{v}_1
   \\]
   Normalize to get:
   \\[
   \mathbf{q}_1 = \frac{\mathbf{u}_1}{\| \mathbf{u}_1 \|}
   \\]

2. **Iterative Orthogonalization and Normalization** for \\( k = 2 \\) to \\( n \\):
   - **Orthogonalize**:
     \\[
     \mathbf{u}_k = \mathbf{v}_k - \sum_{j=1}^{k-1} \text{proj}_{\mathbf{q}_j} \mathbf{v}_k
     \\]
     where the projection \\( \text{proj}_{\mathbf{q}_j} \mathbf{v}_k \\) is calculated as:
     \\[
     \text{proj}_{\mathbf{q}_j} \mathbf{v}_k = (\mathbf{v}_k \cdot \mathbf{q}_j) \mathbf{q}_j
     \\]
   - **Normalize**:
     \\[
     \mathbf{q}_k = \frac{\mathbf{u}_k}{\| \mathbf{u}_k \|}
     \\]

### **Detailed Steps**

1. **Compute \\( \mathbf{u}_1 \\) and \\( \mathbf{q}_1 \\)**:
   - \\( \mathbf{u}_1 = \mathbf{v}_1 \\)
   - \\( \mathbf{q}_1 = \frac{\mathbf{u}_1}{\| \mathbf{u}_1 \|} \\)

2. **For each subsequent vector \\( \mathbf{v}_k \\)**:
   - **Subtract the projections onto all previous \\( \mathbf{q}_j \\)**:
     \\[
     \mathbf{u}_k = \mathbf{v}_k - \sum_{j=1}^{k-1} (\mathbf{v}_k \cdot \mathbf{q}_j) \mathbf{q}_j
     \\]
   - **Normalize \\( \mathbf{u}_k \\) to get \\( \mathbf{q}_k \\)**:
     \\[
     \mathbf{q}_k = \frac{\mathbf{u}_k}{\| \mathbf{u}_k \|}
     \\]

### **Example**

Let's apply the Gram-Schmidt process to vectors \\( \mathbf{v}_1 = [1, 1] \\) and \\( \mathbf{v}_2 = [1, 0] \\) in \\( \mathbb{R}^2 \\).

1. **First Vector**:
   - \\( \mathbf{u}_1 = \mathbf{v}_1 = [1, 1] \\)
   - Normalize:
     \\[
     \| \mathbf{u}_1 \| = \sqrt{1^2 + 1^2} = \sqrt{2}
     \\]
     \\[
     \mathbf{q}_1 = \frac{[1, 1]}{\sqrt{2}} = \left[ \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}} \right]
     \\]

2. **Second Vector**:
   - Compute the projection of \\( \mathbf{v}_2 \\) onto \\( \mathbf{q}_1 \\):
     \\[
     \text{proj}_{\mathbf{q}_1} \mathbf{v}_2 = (\mathbf{v}_2 \cdot \mathbf{q}_1) \mathbf{q}_1
     \\]
     \\[
     \mathbf{v}_2 \cdot \mathbf{q}_1 = [1, 0] \cdot \left[ \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}} \right] = \frac{1}{\sqrt{2}}
     \\]
     \\[
     \text{proj}_{\mathbf{q}_1} \mathbf{v}_2 = \frac{1}{\sqrt{2}} \left[ \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}} \right] = \left[ \frac{1}{2}, \frac{1}{2} \right]
     \\]
   - Subtract the projection:
     \\[
     \mathbf{u}_2 = \mathbf{v}_2 - \text{proj}_{\mathbf{q}_1} \mathbf{v}_2 = [1, 0] - \left[ \frac{1}{2}, \frac{1}{2} \right] = \left[ \frac{1}{2}, -\frac{1}{2} \right]
     \\]
   - Normalize \\( \mathbf{u}_2 \\):
     \\[
     \| \mathbf{u}_2 \| = \sqrt{\left( \frac{1}{2} \right)^2 + \left( -\frac{1}{2} \right)^2} = \frac{1}{\sqrt{2}}
     \\]
     \\[
     \mathbf{q}_2 = \frac{\left[ \frac{1}{2}, -\frac{1}{2} \right]}{\frac{1}{\sqrt{2}}} = \left[ \frac{\sqrt{2}}{2}, -\frac{\sqrt{2}}{2} \right]
     \\]

### **Result**

The orthonormal set is:
\\[
\mathbf{q}_1 = \left[ \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}} \right], \quad \mathbf{q}_2 = \left[ \frac{\sqrt{2}}{2}, -\frac{\sqrt{2}}{2} \right]
\\]

These vectors are orthogonal (\\( \mathbf{q}_1 \cdot \mathbf{q}_2 = 0 \\)) and of unit length (\\( \| \mathbf{q}_1 \| = \| \mathbf{q}_2 \| = 1 \\)).

### **Applications**

- **QR Decomposition**: Decomposing a matrix into an orthogonal matrix \\( Q \\) and an upper triangular matrix \\( R \\).
- **Least Squares Problems**: Finding the best approximation solution to overdetermined systems.
- **Numerical Methods**: Enhancing stability and efficiency in computational algorithms.

### **Summary**

The Gram-Schmidt process is a systematic method for orthonormalizing a set of vectors in an inner product space, ensuring that the new set is easier to work with while preserving the span of the original vectors. It is fundamental in linear algebra and has wide-ranging applications in mathematics, physics, and engineering.
