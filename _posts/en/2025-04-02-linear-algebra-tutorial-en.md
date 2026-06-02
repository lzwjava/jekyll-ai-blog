---
audio: false
generated: true
lang: en
layout: post
title: Linear Algebra Tutorial
translated: false
type: note
---

## 1. Introduction
### Definition & Importance
Linear algebra is the branch of mathematics concerning vector spaces and linear mappings between them. It is fundamental in engineering, physics, computer science, and economics.

### Scalars, Vectors, and Matrices
- **Scalars**: Single numbers (e.g., real or complex numbers)
- **Vectors**: Ordered lists of numbers, representing magnitude and direction
- **Matrices**: Rectangular arrays of numbers representing transformations or systems

### Applications
- Physics (quantum mechanics, relativity)
- Engineering (control systems, circuits)
- Economics (optimization, game theory)
- Data Science & Machine Learning

## 2. Systems of Equations
### Representation
A system of linear equations can be written in matrix form as:
\\[ Ax = b \\]
where \\( A \\) is a matrix, \\( x \\) is a vector of variables, and \\( b \\) is a constant vector.

### Solution Methods
- **Gaussian Elimination**: Converts the system to row echelon form to solve for unknowns.
- **Row Reduction (Reduced Row Echelon Form, RREF)**: Further reduces the matrix to identify solutions.
- **Solution Types**:
  - **Unique solution**: One intersection point
  - **Infinite solutions**: Multiple intersections
  - **No solution**: Parallel lines (inconsistent system)
- **Homogeneous vs. Non-Homogeneous**:
  - Homogeneous: \\( Ax = 0 \\) (always has at least one solution)
  - Non-homogeneous: \\( Ax = b \\)

## 3. Matrices and Operations
### Notation & Types
- **Square Matrix**: Same number of rows and columns
- **Identity Matrix (I)**: Diagonal elements are 1, others are 0
- **Zero Matrix (0)**: All elements are zero

### Operations
- **Addition & Subtraction**: Element-wise
- **Scalar Multiplication**: Multiply each element by a scalar
- **Matrix Multiplication**: \\( (AB)_{ij} = \sum_{k} A_{ik} B_{kj} \\)
- **Transpose**: Flipping rows and columns
- **Inverse (A\\(^-1\\))**: Exists only if determinant is nonzero

## 4. Determinants
### Definition
A scalar value associated with a square matrix, useful in solving linear equations and understanding matrix properties.

### Computation
- **2×2 Matrix**: \\( \text{det} \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc \\)
- **3×3 Matrix**: Use cofactor expansion or Sarrus’ Rule
- **Higher-Order Matrices**: Use row expansion or Laplace expansion

### Properties & Applications
- **Cramer’s Rule**: Uses determinants to solve systems \\( Ax = b \\)
- **Singular vs. Nonsingular Matrices**: Determinant \\( = 0 \\) means non-invertible

## 5. Vector Spaces
### Definition
A set of vectors that can be added together and multiplied by scalars while remaining within the set.

### Key Concepts
- **Subspaces**: A subset of a vector space satisfying closure properties
- **Basis**: A minimal set of linearly independent vectors spanning a space
- **Dimension**: The number of basis vectors
- **Linear Independence**: A set of vectors where no vector is a linear combination of others
- **Span**: All possible linear combinations of a given set of vectors
- **Change of Basis**: Transition between different vector space representations

## 6. Linear Transformations
### Definition
A function \\( T: V \to W \\) that preserves vector addition and scalar multiplication.

### Representation
Every linear transformation can be represented as a matrix.

### Properties
- **Kernel (Null Space)**: Set of vectors mapped to zero
- **Image (Range)**: Set of output vectors
- **Injectivity (One-to-One)**: \\( \text{Ker}(T) = \{0\} \\)
- **Surjectivity (Onto)**: Image spans the entire codomain

## 7. Eigenvalues and Eigenvectors
### Definitions
- **Eigenvalues (λ)**: Scalars where \\( Av = \lambda v \\)
- **Eigenvectors (v)**: Nonzero vectors satisfying \\( Av = \lambda v \\)

### Computation
- Solve the characteristic equation \\( \det(A - \lambda I) = 0 \\)
- Find corresponding eigenvectors from \\( (A - \lambda I)v = 0 \\)

### Applications
- Stability analysis
- Markov processes
- Principal Component Analysis (PCA) in machine learning

## 8. Inner Product Spaces
### Dot Product & Norms
- **Dot Product**: \\( a \cdot b = \sum a_i b_i \\)
- **Norm (Magnitude)**: \\( \|v\| = \sqrt{v \cdot v} \\)

### Orthogonality & Orthonormal Bases
- **Orthogonal Vectors**: Dot product = 0
- **Orthonormal Basis**: Basis where all vectors are orthogonal and have unit length
- **Gram-Schmidt Process**: Converts a basis into an orthonormal one

## 9. Applications
### Real-World Problems
- **Network Flows**: Optimization using linear algebra
- **Data Fitting**: Regression techniques using least squares

### Computational Methods
- **Matrices in Programming**: Used in Python, MATLAB, and NumPy for scientific computing
