---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 小众线性代数观点
translated: true
type: note
---

问题：线性代数中有哪些不受欢迎或有争议的观点？

回答：

以下是线性代数及相关领域中一些数学家和研究人员持有的几个真正不受欢迎（或至少是少数人持有）的观点。这些不是边缘的蹩脚想法，而是与主流教材共识或常见教学实践相悖的观点：

- **行列式被过度吹捧，在严肃的线性代数中几乎不应该使用。**
  许多理论家（例如，范畴论者、一些数值分析师以及某些语境下的Terence Tao等人）认为，行列式是历史遗物，它掩盖了更自然的 Svd概念（外代数、迹、特征多项式、Pfaffian等）。他们声称几乎所有用det表述的定理都可以在没有它的情况下更清晰地重新表述，并且过早教授行列式会损害学生的直觉。

- **无限维算子的谱定理被高估了；大多数工作的分析师更关心谱测度和函数演算，而不是“可对角化性”。**
  在有限维中，每个人都喜欢特征值，但在希尔伯特空间中，许多专家认为对“自伴 ⇒ 可对角化”的痴迷误导了学生关于实际发生的情况（连续谱等）。

- **行约化（高斯消元法）是一种糟糕的线性代数入门方法，应该推迟或从第一门课程中删除。**
  支持者（例如，Sheldon Axler在“Down with Determinants!”和他的书《Linear Algebra Done Right》中）认为，这会鼓励坐标思维，并掩盖向量空间、线性映射和不变性的无坐标之美。

- **抽象向量空间应该在 ℝⁿ 之前教授，而不是之后。**
  标准的美国课程首先在 ℝⁿ 中进行所有操作，然后进行概括。受范畴论影响的相当一部分欧洲人坚持认为，应该从公理开始，然后才将 ℝⁿ 作为示例给出（如果课程足够抽象，甚至不给出）。

- **Jordan 标准形大部分无用，应该被淡化或省略。**
  虽然几乎每本教科书都证明了它，但许多研究人员表示它在数值上不稳定，在应用中很少需要，而 Schur 三角化或有理标准形在实践中更有用。有些人更进一步说，“最小多项式 + 不变因子”（来自模理论）才是真正的答案。

- **内积并非必不可少；有限维线性代数在没有它们的情况下也能很好地（有时甚至更好）工作。**
  许多现代表示论、代数几何、组合学以及理论计算机科学将向量空间视为一个域上的普通模，根本没有内积。过早强调正交性被视为一种受物理学启发的干扰。

- **奇异值分解（SVD）比特征值分解重要得多，但教科书仍然将特征值置于首位。**
  数据科学家和数值分析师的普遍抱怨：对称特征值问题是 SVD 的一个特例，在几乎所有应用（PCA、最小二乘、低秩近似、稳定性）中，SVD 都是正确的工具。

- **矩阵乘法不应该是核心运算；张量积或外积或线性映射的复合应该得到更多关注。**
  一些具有范畴思维的人认为，张量积的幺半群结构比矩阵的环结构更基本。

- **正定矩阵被过度优待；不定度量空间和 Krein 空间在物理学和算子理论中至关重要，但却教学不足。**

这些观点包括“许多研究人员私下持有”到“在课程辩论中公开争论”。你会发现双方都有强烈的捍卫者，尤其是在教学法方面（行列式与无行列式，坐标优先与抽象优先）。

参考文献：
- [Down with Determinants! – Sheldon Axler](https://www.axler.net/DWD.html)
- [Linear Algebra Done Right – Sheldon Axler (Chapter on determinants)](https://linear.axler.net/)
- [Terence Tao’s blog posts on determinants and exterior algebra](https://terrytao.wordpress.com/?s=determinant)
- [The useless: Jordan form – Persiflage blog](https://sbseminar.wordpress.com/2008/06/02/the-jordan-chevalley-decomposition-and-the-uselessness-of-jordan-form/)
- [Why I Don’t Like the Jordan Canonical Form – Federico Poloni](https://fredrikj.net/blog/2018/03/why-i-dont-like-the-jordan-canonical-form/)
