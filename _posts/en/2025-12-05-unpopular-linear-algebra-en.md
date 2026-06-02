---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Linear Algebra Opinions
translated: false
type: note
---

Question: What are some unpopular or controversial opinions in linear algebra?

Answer:

Here are several genuinely unpopular (or at least minority) opinions held by some mathematicians and researchers in linear algebra and related fields. These are not fringe crackpot ideas, but views that go against the mainstream textbook consensus or common teaching practices:

- **Determinants are overhyped and should almost never be used in serious linear algebra.**
  Many theoreticians (e.g., category theorists, some numerical analysts, and people like Terence Tao in certain contexts) argue that determinants are a historical artifact that obscure more natural concepts (exterior algebra, trace, characteristic polynomial, Pfaffian, etc.). They claim almost every theorem stated with det can be reformulated more cleanly without it, and teaching determinants early harms students’ intuition.

- **The spectral theorem for infinite-dimensional operators is overrated; most working analysts care much more about spectral measures and functional calculus than about “diagonalizability.”**
  In finite dimensions everyone loves eigenvalues, but in Hilbert space many experts think the obsession with “self-adjoint ⇒ diagonalizable” misleads students about what actually happens (continuous spectrum, etc.).

- **Row reduction (Gaussian elimination) is a terrible way to introduce linear algebra and should be delayed or removed from the first course.**
  Advocates (e.g., Sheldon Axler in “Down with Determinants!” and his book *Linear Algebra Done Right*) argue it encourages coordinate thinking and obscures the coordinate-free beauty of vector spaces, linear maps, and invariance.

- **Abstract vector spaces should be taught before ℝⁿ, not after.**
  The standard American curriculum does everything in ℝⁿ first, then generalizes. A sizable European and category-theory-influenced minority insists you should start with the axioms and give ℝⁿ only as an example later (or never, if the course is abstract enough).

- **The Jordan canonical form is mostly useless and should be de-emphasized or omitted.**
  While almost every textbook proves it, many researchers say it’s numerically unstable, rarely needed in applications, and the Schur triangulation or rational canonical form is more useful in practice. Some go further and say “minimal polynomial + invariant factors” (from module theory) is the real answer.

- **Inner products are not essential; finite-dimensional linear algebra works perfectly well (and sometimes better) without them.**
  A lot of modern representation theory, algebraic geometry, and combinatorics, and theoretical computer science treat vector spaces as plain modules over a field with no inner product in sight. Forcing orthogonality early is seen as a physics-inspired distraction.

- **The singular value decomposition (SVD) is vastly more important than the eigenvalue decomposition, yet textbooks still give eigenvalues pride of place.**
  Common complaint from data scientists and numerical analysts: the symmetric eigenvalue problem is a special case of SVD, and in almost all applications (PCA, least squares, low-rank approximation, stability) SVD is the right tool.

- **Matrix multiplication should not be the central operation; tensor products or exterior products or composition of linear maps deserve more attention.**
  Some category-minded people argue the monoidal structure (tensor product) is more fundamental than the ring structure on matrices.

- **Positive-definite matrices are over-privileged; indefinite metric spaces and Krein spaces are under-taught despite being crucial in physics and operator theory.**

These opinions range from “quietly held by many researchers” to “openly fought over in curriculum debates.” You’ll find strong defenders on both sides, especially about pedagogy (determinants vs. no determinants, coordinates-first vs. abstract-first).

References:

- [Down with Determinants! – Sheldon Axler](https://www.axler.net/DWD.html)
- [Linear Algebra Done Right – Sheldon Axler (Chapter on determinants)](https://linear.axler.net/)
- [Terence Tao’s blog posts on determinants and exterior algebra](https://terrytao.wordpress.com/?s=determinant)
- [The useless: Jordan form – Persiflage blog](https://sbseminar.wordpress.com/2008/06/02/the-jordan-chevalley-decomposition-and-the-uselessness-of-jordan-form/)
- [Why I Don’t Like the Jordan Canonical Form – Federico Poloni](https://fredrikj.net/blog/2018/03/why-i-dont-like-the-jordan-canonical-form/)
