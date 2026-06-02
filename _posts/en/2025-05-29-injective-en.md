---
audio: false
generated: true
lang: en
layout: post
title: Injective Functions
translated: false
type: note
---

In mathematics, the term "injective" refers to a function or mapping between two sets where distinct elements of the first set map to distinct elements of the second set. In other words, no two different elements in the domain (the first set) are mapped to the same element in the codomain (the second set).

This property is also known as "one-to-one." If a function \\( f \\) is injective, then for any two elements \\( x \\) and \\( y \\) in the domain, if \\( f(x) = f(y) \\), then it must be the case that \\( x = y \\). This ensures that each element in the codomain is mapped by at most one element in the domain.

---

To understand why a linear transformation \\( T \\) is injective if its kernel contains only the zero vector, let's break down the definitions and implications:

1. **Kernel of a Transformation**: The kernel of a linear transformation \\( T: V \rightarrow W \\) (denoted as \\( \ker(T) \\)) is the set of all vectors in \\( V \\) that are mapped to the zero vector in \\( W \\). Mathematically, \\( \ker(T) = \{ v \in V \mid T(v) = 0 \} \\).

2. **Injective Transformation**: A linear transformation \\( T \\) is injective (or one-to-one) if different vectors in \\( V \\) map to different vectors in \\( W \\). In other words, if \\( T(u) = T(v) \\), then \\( u = v \\).

Now, let's connect these two concepts:

- Suppose \\( \ker(T) = \{0\} \\). This means the only vector in \\( V \\) that maps to the zero vector in \\( W \\) is the zero vector itself.

- To show that \\( T \\) is injective, assume \\( T(u) = T(v) \\). By the linearity of \\( T \\), we have \\( T(u) - T(v) = T(u - v) = 0 \\).

- Since \\( \ker(T) = \{0\} \\), \\( T(u - v) = 0 \\) implies that \\( u - v = 0 \\), which means \\( u = v \\).

Thus, if \\( \ker(T) = \{0\} \\), the transformation \\( T \\) is injective. This is because the only solution to \\( T(v) = 0 \\) is \\( v = 0 \\), ensuring that no two distinct vectors in \\( V \\) are mapped to the same vector in \\( W \\).

---

The equation \\( T(u) - T(v) = T(u - v) \\) is a consequence of the linearity property of a linear transformation \\( T \\). Let's break down why this holds:

1. **Linearity of \\( T \\)**: A linear transformation \\( T \\) satisfies two key properties for any vectors \\( u \\) and \\( v \\) in the vector space and any scalar \\( c \\):
   - **Additivity**: \\( T(u + v) = T(u) + T(v) \\)
   - **Homogeneity**: \\( T(cu) = cT(u) \\)

2. **Derivation of \\( T(u) - T(v) = T(u - v) \\)**:
   - Using the additivity property, we can express \\( T(u - v) \\) as \\( T(u + (-v)) \\), which equals \\( T(u) + T(-v) \\).
   - By the homogeneity property, \\( T(-v) = -T(v) \\).
   - Therefore, \\( T(u - v) = T(u) + (-T(v)) = T(u) - T(v) \\).

Thus, \\( T(u) - T(v) = T(u - v) \\) is a direct result of the linearity of \\( T \\). This property is fundamental in linear algebra and is used frequently in proofs and derivations involving linear transformations.
