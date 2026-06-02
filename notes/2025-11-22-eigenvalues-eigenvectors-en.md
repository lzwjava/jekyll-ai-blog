---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-2.5-flash
title: Finding Eigenvalues and Eigenvectors
translated: false
type: note
---

Finding the **eigenvalues** and **eigenvectors** of a matrix is a fundamental concept in linear algebra. It involves solving the **characteristic equation** derived from the matrix.

---

## 🔢 Step 1: Set up the Characteristic Equation

For an \\(n \times n\\) square matrix \\(\mathbf{A}\\), the eigenvalues \\((\lambda)\\) and the corresponding non-zero eigenvectors \\((\mathbf{v})\\) satisfy the equation:

\\(\\)\mathbf{A}\mathbf{v} = \lambda\mathbf{v}\\(\\)

This equation can be rewritten as:

\\(\\)\mathbf{A}\mathbf{v} - \lambda\mathbf{v} = \mathbf{0}\\(\\)
\\(\\)(\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}\\(\\)

where \\(\mathbf{I}\\) is the \\(n \times n\\) **identity matrix** and \\(\mathbf{0}\\) is the zero vector.

For a non-zero solution \\(\mathbf{v}\\) to exist, the matrix \\((\mathbf{A} - \lambda\mathbf{I})\\) must be **singular** (not invertible). This means its **determinant** must be equal to zero:

\\(\\)\text{det}(\mathbf{A} - \lambda\mathbf{I}) = 0\\(\\)

This equation is called the **characteristic equation**.

---

## 💡 Step 2: Find the Eigenvalues (\\(\lambda\\))

1. **Form the matrix \\((\mathbf{A} - \lambda\mathbf{I})\\):** Subtract \\(\lambda\\) from each element on the main diagonal of \\(\mathbf{A}\\).

    * For a \\(2 \times 2\\) matrix \\(\mathbf{A} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}\\), the matrix is:
        \\(\\)\mathbf{A} - \lambda\mathbf{I} = \begin{pmatrix} a-\lambda & b \\ c & d-\lambda \end{pmatrix}\\(\\)

2. **Calculate the determinant:** Set \\(\text{det}(\mathbf{A} - \lambda\mathbf{I}) = 0\\).

    * For the \\(2 \times 2\\) case, the characteristic equation is:
        \\(\\)(a-\lambda)(d-\lambda) - bc = 0\\(\\)

3. **Solve the resulting polynomial:** This equation will be a polynomial in \\(\lambda\\) (called the **characteristic polynomial**). The roots of this polynomial are the **eigenvalues** of the matrix \\(\mathbf{A}\\).

---

## 🔎 Step 3: Find the Eigenvectors (\\(\mathbf{v}\\))

For **each eigenvalue** (\\(\lambda_i\\)) found in Step 2, you must solve the following system of linear equations to find its corresponding eigenvector \\((\mathbf{v}_i)\\):

\\(\\)(\mathbf{A} - \lambda_i\mathbf{I})\mathbf{v}_i = \mathbf{0}\\(\\)

1. **Substitute the eigenvalue:** Substitute the specific eigenvalue \\(\lambda_i\\) back into the matrix equation \\((\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}\\).

2. **Solve the system:** Use techniques like **Gaussian elimination** to solve the resulting homogeneous system of equations. Since the matrix \\((\mathbf{A} - \lambda_i\mathbf{I})\\) is singular, you will always get an infinite number of solutions (a non-zero solution space).

3. **Express the eigenvector:** The solutions define the **eigenspace** corresponding to \\(\lambda_i\\). You express the eigenvector \\(\mathbf{v}_i\\) in terms of one or more free variables, and usually choose a simple, non-zero vector to represent the direction of the eigenspace.

### Example for a \\(2 \times 2\\) Matrix

Let \\(\mathbf{A} = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}\\).

1. **Characteristic Equation:**
    \\(\\)\text{det}\begin{pmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{pmatrix} = 0\\(\\)
    \\(\\)(2-\lambda)(2-\lambda) - 1(1) = 0\\(\\)
    \\(\\)\lambda^2 - 4\lambda + 4 - 1 = 0\\(\\)
    \\(\\)\lambda^2 - 4\lambda + 3 = 0\\(\\)

2. **Eigenvalues:**
    \\(\\)(\lambda - 3)(\lambda - 1) = 0\\(\\)
    The eigenvalues are \\(\mathbf{\lambda_1 = 3}\\) and \\(\mathbf{\lambda_2 = 1}\\).

3. **Eigenvectors:**

    * **For \\(\lambda_1 = 3\\):**
        \\(\\)\begin{pmatrix} 2-3 & 1 \\ 1 & 2-3 \end{pmatrix} \begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \implies \begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix} \begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}\\(\\)
        The first row gives \\(-v_1 + v_2 = 0\\), or \\(v_1 = v_2\\).
        A simple, non-zero eigenvector is \\(\mathbf{v_1 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}}\\).

    * **For \\(\lambda_2 = 1\\):**
        \\(\\)\begin{pmatrix} 2-1 & 1 \\ 1 & 2-1 \end{pmatrix} \begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \implies \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}\\(\\)
        The first row gives \\(v_1 + v_2 = 0\\), or \\(v_1 = -v_2\\).
        A simple, non-zero eigenvector is \\(\mathbf{v_2 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}}\\).

Would you like to try finding the eigenvalues and eigenvectors for a different matrix?Finding the **eigenvalues** and **eigenvectors** of a matrix is a three-step process: setting up the characteristic equation, solving it for the eigenvalues, and then solving a system of linear equations for the corresponding eigenvectors.

---

## 1️⃣ Step 1: Set up the Characteristic Equation

For an \\(n \times n\\) matrix \\(\mathbf{A}\\), the relationship between an eigenvalue (\\(\lambda\\)) and its corresponding non-zero eigenvector (\\(\mathbf{v}\\)) is:

\\(\\)\mathbf{A}\mathbf{v} = \lambda\mathbf{v}\\(\\)

To find the eigenvalues, you must solve the **characteristic equation**, which is derived from the requirement that the system of equations \\((\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}\\) must have non-zero solutions (i.e., the matrix is singular):

\\(\\)\text{det}(\mathbf{A} - \lambda\mathbf{I}) = 0\\(\\)

Here, \\(\mathbf{I}\\) is the \\(n \times n\\) **identity matrix**. To form \\((\mathbf{A} - \lambda\mathbf{I})\\), you simply subtract \\(\lambda\\) from every element on the main diagonal of \\(\mathbf{A}\\).

---

## 2️⃣ Step 2: Find the Eigenvalues (\\(\lambda\\))

1. **Form the Matrix:** Calculate \\(\mathbf{A} - \lambda\mathbf{I}\\).
2. **Calculate the Determinant:** Compute the determinant of the resulting matrix.
3. **Solve the Polynomial:** Set the determinant to zero and solve the resulting polynomial equation in \\(\lambda\\). This polynomial is the **characteristic polynomial**, and its roots are the **eigenvalues**.

For a **\\(2 \times 2\\) matrix** \\(\mathbf{A} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}\\), the characteristic equation is:
\\(\\)\text{det}\begin{pmatrix} a-\lambda & b \\ c & d-\lambda \end{pmatrix} = (a-\lambda)(d-\lambda) - bc = 0\\(\\)

---

## 3️⃣ Step 3: Find the Eigenvectors (\\(\mathbf{v}\\))

For **each eigenvalue** (\\(\lambda_i\\)) found in Step 2, you must solve the following homogeneous system of equations for the non-zero vector \\(\mathbf{v}_i\\):

\\(\\)(\mathbf{A} - \lambda_i\mathbf{I})\mathbf{v}_i = \mathbf{0}\\(\\)

1. **Substitute \\(\lambda_i\\):** Replace \\(\lambda\\) in the matrix \\((\mathbf{A} - \lambda\mathbf{I})\\) with the specific eigenvalue \\(\lambda_i\\).
2. **Solve the System:** Use methods like **Gaussian elimination** to solve the system. Since the matrix is guaranteed to be singular, you will find a line or plane of solutions (an **eigenspace**).
3. **Express the Vector:** Choose a simple, non-zero vector that satisfies the equations to represent the **eigenvector** \\(\mathbf{v}_i\\).

For example, if the solution leads to \\(v_1 = 2v_2\\), you can choose \\(v_2 = 1\\) and \\(v_1 = 2\\), making the eigenvector \\(\mathbf{v} = \begin{pmatrix} 2 \\ 1 \end{pmatrix}\\).

Would you like to practice with a specific matrix?
