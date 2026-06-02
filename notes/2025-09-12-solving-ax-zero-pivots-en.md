---
audio: false
date: 2025-09-12
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: Solving Ax Equals Zero Pivot Variables
translated: false
type: note
---

This video is **Lecture 7** from **MIT's *18.06 Linear Algebra* course (Spring 2005)**, taught by **Professor Gilbert Strang**. The topic is:

### **"Solving \\( A\mathbf{x} = \mathbf{0} \\): Pivot Variables and Special Solutions"**

---

### **Key Concepts Covered in the Lecture:**

1. **Homogeneous Systems (\\( A\mathbf{x} = \mathbf{0} \\))**
   - A system of linear equations where the right-hand side is the zero vector.
   - Always has at least the **trivial solution** \\( \mathbf{x} = \mathbf{0} \\).
   - If there are **free variables**, there are infinitely many solutions.

2. **Pivot Variables vs. Free Variables**
   - **Pivot variables**: Correspond to columns with pivots (nonzero leading entries) in the **row reduced echelon form (RREF)** of \\( A \\).
   - **Free variables**: Correspond to columns **without pivots** (can take any value).
   - The number of free variables = number of columns − rank of \\( A \\).

3. **Special Solutions (Basis for the Nullspace)**
   - For each free variable, set it to **1** and the others to **0**, then solve for the pivot variables.
   - These solutions form a **basis** for the **nullspace** of \\( A \\) (all solutions to \\( A\mathbf{x} = \mathbf{0} \\)).
   - The nullspace is a **subspace** of \\( \mathbb{R}^n \\).

4. **Rank and the Nullspace**
   - If \\( A \\) is an \\( m \times n \\) matrix with rank \\( r \\):
     - Number of pivot variables = \\( r \\).
     - Number of free variables = \\( n - r \\).
     - Dimension of the nullspace = \\( n - r \\).

5. **Example Walkthrough**
   - Strang works through an example (likely a matrix with rank < number of columns) to illustrate:
     - Finding the RREF.
     - Identifying pivot and free variables.
     - Constructing special solutions.
     - Expressing the general solution as a linear combination of special solutions.

6. **Geometric Interpretation**
   - The nullspace represents all vectors \\( \mathbf{x} \\) that are "collapsed" to zero when multiplied by \\( A \\).
   - For a 3×3 matrix with rank 2, the nullspace is a **line** through the origin.

---

### **Why This Lecture Matters:**

- Introduces the **nullspace** (a fundamental subspace in linear algebra).
- Connects **row reduction (elimination)** to the structure of solutions.
- Lays the groundwork for understanding **linear independence**, **bases**, and **dimension** in later lectures.
- Essential for solving systems, understanding transformations, and applications like **differential equations** or **machine learning**.

---

### **Where to Find More:**

- **Full course materials**: [MIT OCW 18.06](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
- **Textbook**: Strang’s *"Introduction to Linear Algebra"* (Chapter 2 covers this topic).
- **Follow-up lectures**: Next lectures discuss **solving \\( A\mathbf{x} = \mathbf{b} \\)** (non-homogeneous systems) and the **column space**.

---

### **Summary in One Sentence:**

This lecture teaches how to find **all solutions** to \\( A\mathbf{x} = \mathbf{0} \\) by identifying pivot/free variables and constructing a basis for the nullspace using special solutions.
