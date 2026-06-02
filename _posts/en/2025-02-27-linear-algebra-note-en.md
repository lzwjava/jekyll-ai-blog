---
audio: true
generated: true
layout: post
title: Linear Algebra Note
type: note
---

## Example

Consider the quadratic form in two variables \\( x \\) and \\(y\\):

\\[ Q(x, y) = 2x^2 + 4xy + 3y^2 \\]

### Step-by-Step Transformation to Canonical Form

1. **Matrix Representation:**
   - Write the quadratic form as a matrix equation. The matrix \\(A\\) associated with this quadratic form is:

\\[
A = \begin{pmatrix}
2 & 2 \\
2 & 3
\end{pmatrix}
\\]

   Note that the off-diagonal elements are half of the coefficient of the \\(xy\\) term.

2. **Find Eigenvalues and Eigenvectors:**
   - Compute the eigenvalues of \\(A\\) by solving the characteristic equation \\( \det(A - \lambda I) = 0 \\).
   - For each eigenvalue, find the corresponding eigenvector.

3. **Diagonalization:**
   - Construct a matrix \\(P\\) whose columns are the eigenvectors of \\(A\\).
   - Compute \\(D = P^TAP\\), which will be a diagonal matrix with the eigenvalues of \\(A\\) on the diagonal.

4. **Change of Variables:**
   - Define new variables \\(u\\) and \\(v\\) such that:

\\[
\begin{pmatrix}
x \\
y
\end{pmatrix} = P \begin{pmatrix}
u \\
v
\end{pmatrix}
\\]

   - Substitute these into the original quadratic form to get a new form in terms of \\(u\\) and \\(v\\).

5. **Canonical Form:**
   - The resulting quadratic form will be in the canonical form, which is a sum of squares:

\\[
Q(u, v) = \lambda_1 u^2 + \lambda_2 v^2
\\]

   where \\(\lambda_1\\) and \\(\lambda_2\\) are the eigenvalues of \\(A\\).

### Interpretation

- The canonical form reveals the geometric nature of the quadratic form.
- If both eigenvalues are positive, the form is positive definite.
- If both are negative, it is negative definite.
- If they have different signs, the form is indefinite.

This process simplifies the quadratic form and makes it easier to analyze its properties.

---

In the context of quadratic forms, the term "二次型的规范形" translates to "canonical form of a quadratic form" in English. Understanding this concept involves recognizing how a quadratic form can be simplified or transformed into a standard form through linear algebra techniques.

### Quadratic Forms
A quadratic form is a homogeneous polynomial of degree two in several variables. For example, in two variables \\(x\\) and \\(y\\), a quadratic form might look like:

\\[ Q(x, y) = ax^2 + bxy + cy^2 \\]

### Canonical Form
The canonical form of a quadratic form is a simplified version that reveals essential properties, such as the rank and signature (the number of positive, negative, and zero eigenvalues). To achieve this form, we typically perform a change of variables, often through diagonalization or other orthogonal transformations.

#### Steps to Find the Canonical Form:
1. **Matrix Representation:** Represent the quadratic form as a symmetric matrix \\(A\\). For the above example, the matrix would be:
\\[
A = \begin{pmatrix}
a & \frac{b}{2} \\
\frac{b}{2} & c
\end{pmatrix}
\\]

2. **Diagonalization:** Find an orthogonal matrix \\(P\\) such that \\(P^TAP\\) is a diagonal matrix \\(D\\). This process involves finding the eigenvalues and eigenvectors of \\(A\\).

3. **Change of Variables:** Use the matrix \\(P\\) to change variables, transforming the original quadratic form into a sum of squares, each corresponding to an eigenvalue.

4. **Canonical Form:** The resulting diagonal matrix \\(D\\) represents the canonical form of the quadratic form, where each diagonal entry is an eigenvalue of \\(A\\).

The canonical form helps in analyzing the properties of the quadratic form, such as determining whether it is positive definite, negative definite, or indefinite, which is crucial in optimization and other mathematical applications.

---

The **normal form of a quadratic form** refers to the simplified standard representation of a quadratic form after applying an appropriate change of variables. This transformation makes the structure of the quadratic form clearer and easier to analyze.

---

### **1. Definition of a Quadratic Form**
A **quadratic form** in \\( n \\) variables is a function of the form:

\\[
Q(x) = x^T A x
\\]

where:
- \\( x = (x_1, x_2, \dots, x_n)^T \\) is an \\( n \\)-dimensional column vector,
- \\( A \\) is an \\( n \times n \\) symmetric matrix.

The goal is to transform this quadratic form into a simpler, standardized form.

---

### **2. Finding the Normal Form**
To simplify the quadratic form, we use an orthogonal change of variables:

1. **Find the Eigenvalues and Eigenvectors of \\( A \\):**
   - Compute the eigenvalues \\( \lambda_1, \lambda_2, \dots, \lambda_n \\).
   - Find an orthonormal basis of eigenvectors.

2. **Diagonalization of \\( A \\):**
   - Since \\( A \\) is symmetric, it can be diagonalized as \\( A = P D P^T \\), where:
     - \\( P \\) is an orthogonal matrix (whose columns are eigenvectors of \\( A \\)).
     - \\( D \\) is a diagonal matrix with eigenvalues \\( \lambda_1, \lambda_2, \dots, \lambda_n \\) on the diagonal.

3. **Change of Variables:**
   - Define a new variable \\( y = P^T x \\), then:

\\[
Q(x) = x^T A x = (P y)^T A (P y) = y^T (P^T A P) y = y^T D y
\\]

   - Since \\( D \\) is diagonal, the quadratic form simplifies to:

\\[
Q(y) = \lambda_1 y_1^2 + \lambda_2 y_2^2 + \dots + \lambda_n y_n^2
\\]

   This is the **normal form of the quadratic form**.

---

### **3. Interpretation of the Normal Form**
- The normal form expresses the quadratic form as a sum of squared terms, weighted by the eigenvalues.
- The **signs of the eigenvalues** determine the nature of the quadratic form:
  - If all eigenvalues are positive, the form is **positive definite**.
  - If all are negative, it is **negative definite**.
  - If there are mixed signs, it is **indefinite**.

This process is essential in **conic sections, optimization, and differential equations**, as it helps classify quadratic surfaces and functions.

Would you like a more detailed example?
