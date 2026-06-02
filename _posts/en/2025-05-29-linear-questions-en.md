---
audio: false
generated: true
lang: en
layout: post
title: Linear Algebra Questions
translated: false
type: note
---

Okay, I will translate and answer the questions from the image.

**Translations and Answers:**

**18. Let matrices X and A satisfy the relation XA = X + A. If $A = \begin{pmatrix} 1 & -3 & 0 \\\ 2 & 1 & 0 \\\ 0 & 0 & 2 \end{pmatrix}$, find matrix X.**

**Answer:**
We are given the equation $XA = X + A$.
We can rewrite this as $XA - X = A$, so $X(A - I) = A$.
If $(A - I)$ is invertible, then $X = A(A - I)^{-1}$.

First, let's calculate $A - I$:

$A - I = \begin{pmatrix} 1 & -3 & 0 \\\ 2 & 1 & 0 \\\ 0 & 0 & 2 \end{pmatrix} - \begin{pmatrix} 1 & 0 & 0 \\\ 0 & 1 & 0 \\\ 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} 0 & -3 & 0 \\\ 2 & 0 & 0 \\\ 0 & 0 & 1 \end{pmatrix}$.

Next, we find the inverse of $(A - I)$. Let $B = A - I$.
The determinant of B is $\det(B) = 0(0 - 0) - (-3)(2 - 0) + 0(0 - 0) = 6$.
Since $\det(B) \neq 0$, B is invertible.

The adjugate of B is:
$adj(B) = \begin{pmatrix} C_{11} & C_{21} & C_{31} \\\ C_{12} & C_{22} & C_{32} \\\ C_{13} & C_{23} & C_{33} \end{pmatrix}$
$C_{11} = (0)(1) - (0)(0) = 0$
$C_{12} = -((2)(1) - (0)(0)) = -2$
$C_{13} = (2)(0) - (0)(0) = 0$
$C_{21} = -((-3)(1) - (0)(0)) = 3$
$C_{22} = (0)(1) - (0)(0) = 0$
$C_{23} = -((0)(0) - (-3)(0)) = 0$
$C_{31} = (-3)(0) - (0)(0) = 0$
$C_{32} = -((0)(0) - (0)(2)) = 0$
$C_{33} = (0)(0) - (-3)(2) = 6$

So, $adj(B) = \begin{pmatrix} 0 & -(-3) & 0 \\\ -(2) & 0 & -0 \\\ 0 & -0 & 6 \end{pmatrix}^T = \begin{pmatrix} 0 & 3 & 0 \\\ -2 & 0 & 0 \\\ 0 & 0 & 6 \end{pmatrix}^T = \begin{pmatrix} 0 & -2 & 0 \\\ 3 & 0 & 0 \\\ 0 & 0 & 6 \end{pmatrix}$.
No, the adjugate is the transpose of the cofactor matrix:
$adj(B) = \begin{pmatrix} 0 & 3 & 0 \\\ -2 & 0 & 0 \\\ 0 & 0 & 6 \end{pmatrix}$.
Wait, I made a mistake in the cofactor calculation.
$C_{11} = \begin{vmatrix} 0 & 0 \\\ 0 & 1 \end{vmatrix} = 0$
$C_{12} = -\begin{vmatrix} 2 & 0 \\\ 0 & 1 \end{vmatrix} = -2$
$C_{13} = \begin{vmatrix} 2 & 0 \\\ 0 & 0 \end{vmatrix} = 0$
$C_{21} = -\begin{vmatrix} -3 & 0 \\\ 0 & 1 \end{vmatrix} = 3$
$C_{22} = \begin{vmatrix} 0 & 0 \\\ 0 & 1 \end{vmatrix} = 0$
$C_{23} = -\begin{vmatrix} 0 & -3 \\\ 0 & 0 \end{vmatrix} = 0$
$C_{31} = \begin{vmatrix} -3 & 0 \\\ 0 & 0 \end{vmatrix} = 0$
$C_{32} = -\begin{vmatrix} 0 & 0 \\\ 2 & 0 \end{vmatrix} = 0$
$C_{33} = \begin{vmatrix} 0 & -3 \\\ 2 & 0 \end{vmatrix} = 6$

The cofactor matrix is $C = \begin{pmatrix} 0 & -2 & 0 \\\ 3 & 0 & 0 \\\ 0 & 0 & 6 \end{pmatrix}$.
The adjugate matrix is $adj(B) = C^T = \begin{pmatrix} 0 & 3 & 0 \\\ -2 & 0 & 0 \\\ 0 & 0 & 6 \end{pmatrix}$.

Then, $(A - I)^{-1} = \frac{1}{\det(B)} adj(B) = \frac{1}{6} \begin{pmatrix} 0 & 3 & 0 \\\ -2 & 0 & 0 \\\ 0 & 0 & 6 \end{pmatrix} = \begin{pmatrix} 0 & 1/2 & 0 \\\ -1/3 & 0 & 0 \\\ 0 & 0 & 1 \end{pmatrix}$.

Now, we calculate $X = A(A - I)^{-1}$:
$X = \begin{pmatrix} 1 & -3 & 0 \\\ 2 & 1 & 0 \\\ 0 & 0 & 2 \end{pmatrix} \begin{pmatrix} 0 & 1/2 & 0 \\\ -1/3 & 0 & 0 \\\ 0 & 0 & 1 \end{pmatrix}$
$X = \begin{pmatrix} (1)(0) + (-3)(-1/3) + (0)(0) & (1)(1/2) + (-3)(0) + (0)(0) & (1)(0) + (-3)(0) + (0)(1) \\\ (2)(0) + (1)(-1/3) + (0)(0) & (2)(1/2) + (1)(0) + (0)(0) & (2)(0) + (1)(0) + (0)(1) \\\ (0)(0) + (0)(-1/3) + (2)(0) & (0)(1/2) + (0)(0) + (2)(0) & (0)(0) + (0)(0) + (2)(1) \end{pmatrix}$
$X = \begin{pmatrix} 0+1+0 & 1/2+0+0 & 0+0+0 \\\ 0-1/3+0 & 1+0+0 & 0+0+0 \\\ 0+0+0 & 0+0+0 & 0+0+2 \end{pmatrix}$
$X = \begin{pmatrix} 1 & 1/2 & 0 \\\ -1/3 & 1 & 0 \\\ 0 & 0 & 2 \end{pmatrix}$.

**19. Determine the value of k for which the vectors $\alpha_1 = (1, 1, k)^T$, $\alpha_2 = (1, k, 1)^T$, $\alpha_3 = (k, 1, 1)^T$ are linearly dependent. Find a maximal linearly independent set and express the remaining vector(s) as a linear combination of this set.**

**Answer:**
The vectors $\alpha_1, \alpha_2, \alpha_3$ are linearly dependent if the determinant of the matrix formed by these vectors is zero.
Let $A = \begin{pmatrix} 1 & 1 & k \\\ 1 & k & 1 \\\ k & 1 & 1 \end{pmatrix}$.
$\det(A) = 1(k - 1) - 1(1 - k) + k(1 - k^2)$
$= k - 1 - 1 + k + k - k^3$
$= -k^3 + 3k - 2$.
We need to find $k$ such that $-k^3 + 3k - 2 = 0$, or $k^3 - 3k + 2 = 0$.
We can test for integer roots that are divisors of 2 (i.e., $\pm 1, \pm 2$).
If $k=1$, $1^3 - 3(1) + 2 = 1 - 3 + 2 = 0$. So, $(k-1)$ is a factor.
If $k=-2$, $(-2)^3 - 3(-2) + 2 = -8 + 6 + 2 = 0$. So, $(k+2)$ is a factor.
Using polynomial division or synthetic division for $(k^3 - 3k + 2) / (k-1)$:
$(k-1)(k^2+k-2) = 0$
$(k-1)(k+2)(k-1) = 0$
So, the roots are $k=1$ (repeated root) and $k=-2$.
The vectors are linearly dependent if $k=1$ or $k=-2$.

Case 1: $k=1$
$\alpha_1 = (1, 1, 1)^T$, $\alpha_2 = (1, 1, 1)^T$, $\alpha_3 = (1, 1, 1)^T$.
In this case, all three vectors are identical.
A maximal linearly independent set can be $\{\alpha_1\}$.
Then $\alpha_2 = 1 \cdot \alpha_1$ and $\alpha_3 = 1 \cdot \alpha_1$.

Case 2: $k=-2$
$\alpha_1 = (1, 1, -2)^T$, $\alpha_2 = (1, -2, 1)^T$, $\alpha_3 = (-2, 1, 1)^T$.
Let's check if $\alpha_1$ and $\alpha_2$ are linearly independent. They are not scalar multiples of each other, so they are linearly independent. Thus, a maximal linearly independent set can be $\{\alpha_1, \alpha_2\}$.
We want to express $\alpha_3$ as a linear combination of $\alpha_1$ and $\alpha_2$:
$\alpha_3 = c_1 \alpha_1 + c_2 \alpha_2$
$(-2, 1, 1)^T = c_1 (1, 1, -2)^T + c_2 (1, -2, 1)^T$
This gives the system of equations:

1) $c_1 + c_2 = -2$
2) $c_1 - 2c_2 = 1$
3) $-2c_1 + c_2 = 1$
Subtract (2) from (1): $(c_1 + c_2) - (c_1 - 2c_2) = -2 - 1 \Rightarrow 3c_2 = -3 \Rightarrow c_2 = -1$.
Substitute $c_2 = -1$ into (1): $c_1 - 1 = -2 \Rightarrow c_1 = -1$.
Check with (3): $-2(-1) + (-1) = 2 - 1 = 1$. This is consistent.
So, $\alpha_3 = -1 \cdot \alpha_1 - 1 \cdot \alpha_2$.

**20. Solve the system of linear equations { $x_1 - x_2 - 3x_4 = -2$ ; $x_1 + 2x_3 - 2x_4 = -1$ ; $2x_1 - 2x_2 + x_3 - 6x_4 = -5$ ; $-x_1 + 2x_2 + 3x_3 + 4x_4 = 2$ } (Find a particular solution and the fundamental basis of solutions for the corresponding homogeneous system).**

**Answer:**
The augmented matrix is:
$\begin{pmatrix} 1 & -1 & 0 & -3 & | & -2 \\\ 1 & 0 & 2 & -2 & | & -1 \\\ 2 & -2 & 1 & -6 & | & -5 \\\ -1 & 2 & 3 & 4 & | & 2 \end{pmatrix}$

$R_2 \leftarrow R_2 - R_1$
$R_3 \leftarrow R_3 - 2R_1$
$R_4 \leftarrow R_4 + R_1$
$\begin{pmatrix} 1 & -1 & 0 & -3 & | & -2 \\\ 0 & 1 & 2 & 1 & | & 1 \\\ 0 & 0 & 1 & 0 & | & -1 \\\ 0 & 1 & 3 & 1 & | & 0 \end{pmatrix}$

$R_1 \leftarrow R_1 + R_2$
$R_4 \leftarrow R_4 - R_2$
$\begin{pmatrix} 1 & 0 & 2 & -2 & | & -1 \\\ 0 & 1 & 2 & 1 & | & 1 \\\ 0 & 0 & 1 & 0 & | & -1 \\\ 0 & 0 & 1 & 0 & | & -1 \end{pmatrix}$

$R_1 \leftarrow R_1 - 2R_3$
$R_2 \leftarrow R_2 - 2R_3$
$R_4 \leftarrow R_4 - R_3$
$\begin{pmatrix} 1 & 0 & 0 & -2 & | & 1 \\\ 0 & 1 & 0 & 1 & | & 3 \\\ 0 & 0 & 1 & 0 & | & -1 \\\ 0 & 0 & 0 & 0 & | & 0 \end{pmatrix}$

The system is equivalent to:
$x_1 - 2x_4 = 1 \Rightarrow x_1 = 1 + 2x_4$
$x_2 + x_4 = 3 \Rightarrow x_2 = 3 - x_4$
$x_3 = -1$
Let $x_4 = t$ (free variable).
The general solution is:
$x_1 = 1 + 2t$
$x_2 = 3 - t$
$x_3 = -1$
$x_4 = t$
In vector form: $X = \begin{pmatrix} 1 \\\ 3 \\\ -1 \\\ 0 \end{pmatrix} + t \begin{pmatrix} 2 \\\ -1 \\\ 0 \\\ 1 \end{pmatrix}$.

A particular solution is obtained by setting $t=0$: $X_p = \begin{pmatrix} 1 \\\ 3 \\\ -1 \\\ 0 \end{pmatrix}$.

The corresponding homogeneous system has the solution $X_h = t \begin{pmatrix} 2 \\\ -1 \\\ 0 \\\ 1 \end{pmatrix}$.
The fundamental basis of solutions for the homogeneous system is $\{\begin{pmatrix} 2 \\\ -1 \\\ 0 \\\ 1 \end{pmatrix}\}$.

<div>
**21. Let matrix A = \begin{pmatrix} x & 0 & y \\\ 0 & 2 & 0 \\\ y & 0 & -2 \end{pmatrix} have an eigenvalue of -3, and |A| = -12. Find the values of x and y.**
</div>

**Answer:**
The characteristic equation is $\det(A - \lambda I) = 0$.
$A - \lambda I = \begin{pmatrix} x-\lambda & 0 & y \\\ 0 & 2-\lambda & 0 \\\ y & 0 & -2-\lambda \end{pmatrix}$.
$\det(A - \lambda I) = [x-\lambda]((2-\lambda)(-2-\lambda) - 0) - 0 + y[0 - y(2-\lambda)]$
$= (x-\lambda)(2-\lambda)(-2-\lambda) - y^2(2-\lambda)$
$= [2-\lambda]((x-\lambda)(-2-\lambda) - y^2)$
$= [2-\lambda](-2x - x\lambda + 2\lambda + \lambda^2 - y^2) = 0$.
The eigenvalues are $\lambda_1 = 2$, and the roots of $\lambda^2 + (2-x)\lambda - (2x+y^2) = 0$.
We are given that one eigenvalue is -3.
If $2 = -3$, this is false. So, -3 must be a root of $\lambda^2 + (2-x)\lambda - (2x+y^2) = 0$.
Substitute $\lambda = -3$:
$(-3)^2 + (2-x)(-3) - (2x+y^2) = 0$
$9 - 6 + 3x - 2x - y^2 = 0$
$3 + x - y^2 = 0 \Rightarrow x - y^2 = -3$ (Equation 1)

We are also given that $\det(A) = -12$.
$\det(A) = x(2(-2) - 0) - 0 + y(0 - 2y)$
$= -4x - 2y^2 = -12$
Divide by -2: $2x + y^2 = 6$ (Equation 2)

Now we have a system of two equations with x and y:

1) $x - y^2 = -3$
2) $2x + y^2 = 6$
Add Equation 1 and Equation 2:
$(x - y^2) + (2x + y^2) = -3 + 6$
$3x = 3 \Rightarrow x = 1$.
Substitute $x=1$ into Equation 1:
$1 - y^2 = -3$
$-y^2 = -4$
$y^2 = 4 \Rightarrow y = \pm 2$.

So the values are $x=1$ and $y=2$, or $x=1$ and $y=-2$.

Let's check the eigenvalues for both cases.
The characteristic polynomial factors as $[2-\lambda](\lambda^2 + (2-x)\lambda - (2x+y^2)) = 0$.
If $x=1, y=2$:
$[2-\lambda](\lambda^2 + (2-1)\lambda - (2(1)+2^2)) = 0$
$[2-\lambda](\lambda^2 + \lambda - (2+4)) = 0$
$(2-\lambda)(\lambda^2 + \lambda - 6) = 0$
$(2-\lambda)(\lambda+3)(\lambda-2) = 0$.
The eigenvalues are $\lambda = 2, -3, 2$. This is consistent with an eigenvalue being -3.

If $x=1, y=-2$:
$[2-\lambda](\lambda^2 + (2-1)\lambda - (2(1)+(-2)^2)) = 0$
$[2-\lambda](\lambda^2 + \lambda - (2+4)) = 0$
$(2-\lambda)(\lambda^2 + \lambda - 6) = 0$
$(2-\lambda)(\lambda+3)(\lambda-2) = 0$.
The eigenvalues are $\lambda = 2, -3, 2$. This is also consistent.

Both pairs $(x,y) = (1,2)$ and $(x,y) = (1,-2)$ satisfy the conditions.

**22. Let the 3-variable quadratic form $f(x_1, x_2, x_3) = t(x_1^2 + x_2^2 + x_3^2) + 2x_1x_2 + 2x_1x_3 - 2x_2x_3$. Determine for what value(s) of t this quadratic form is positive definite.**

**Answer:**
The matrix of the quadratic form A is:
$A = \begin{pmatrix} t & 1 & 1 \\\ 1 & t & -1 \\\ 1 & -1 & t \end{pmatrix}$.
For the quadratic form to be positive definite, all leading principal minors of A must be positive.

1. The first leading principal minor is $M_1 = t$.
For positive definiteness, $t > 0$.

2. The second leading principal minor is $M_2 = \det \begin{pmatrix} t & 1 \\\ 1 & t \end{pmatrix} = t^2 - 1$.
For positive definiteness, $t^2 - 1 > 0 \Rightarrow t^2 > 1$.
Since we already have $t > 0$, this implies $t > 1$.

3. The third leading principal minor is $M_3 = \det(A)$.
$M_3 = t(t^2 - 1) - 1(t - (-1)) + 1(-1 - t)$
$= t(t^2 - 1) - (t + 1) - (1 + t)$
$= t^3 - t - t - 1 - 1 - t$
$= t^3 - 3t - 2$.
For positive definiteness, $t^3 - 3t - 2 > 0$.

We know from question 19 that $k^3 - 3k - 2 = (k+1)^2(k-2)$. (Here $k$ is $t$)
So, $t^3 - 3t - 2 = (t+1)^2(t-2)$.
We need $(t+1)^2(t-2) > 0$.
Since $(t+1)^2 \ge 0$, and for it not to be zero, $t \neq -1$.
So we need $t-2 > 0$, which means $t > 2$.

Combining the conditions:

1) $t > 0$
2) $t > 1$
3) $t > 2$

The intersection of these conditions is $t > 2$.
Therefore, the quadratic form is positive definite when $t > 2$.
