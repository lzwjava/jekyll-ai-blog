---
audio: false
generated: true
lang: en
layout: post
title: Linear Independence Proof
translated: false
type: note
---

### Translation

23. Given that the vectors \\( \alpha_1, \alpha_2, \alpha_3 \\) are linearly independent, and the vectors \\( \beta_1 = \alpha_1 + 2\alpha_2 \\), \\( \beta_2 = -\alpha_1 + \alpha_2 - 3\alpha_3 \\), \\( \beta_3 = 3\alpha_1 + 6\alpha_3 \\). Prove that the vectors \\( \beta_1, \beta_2, \beta_3 \\) are linearly related.

### Solution

To prove that the vectors \\( \beta_1, \beta_2, \beta_3 \\) are linearly related, we need to show that there exist scalars \\( c_1, c_2, c_3 \\) (not all zero) such that:

\\[ c_1 \beta_1 + c_2 \beta_2 + c_3 \beta_3 = 0 \\]

Given:
\\[ \beta_1 = \alpha_1 + 2\alpha_2 \\]
\\[ \beta_2 = -\alpha_1 + \alpha_2 - 3\alpha_3 \\]
\\[ \beta_3 = 3\alpha_1 + 6\alpha_3 \\]

We need to find constants \\( c_1, c_2, c_3 \\) such that:

\\[ c_1 (\alpha_1 + 2\alpha_2) + c_2 (-\alpha_1 + \alpha_2 - 3\alpha_3) + c_3 (3\alpha_1 + 6\alpha_3) = 0 \\]

This can be rewritten as:

\\[ (c_1 - c_2 + 3c_3)\alpha_1 + (2c_1 + c_2)\alpha_2 + (-3c_2 + 6c_3)\alpha_3 = 0 \\]

Since \\( \alpha_1, \alpha_2, \alpha_3 \\) are linearly independent, the coefficients of \\( \alpha_1, \alpha_2, \alpha_3 \\) must each be zero:

1. \\( c_1 - c_2 + 3c_3 = 0 \\)
2. \\( 2c_1 + c_2 = 0 \\)
3. \\( -3c_2 + 6c_3 = 0 \\)

Let's solve this system of equations:

From equation 2:
\\[ 2c_1 + c_2 = 0 \implies c_2 = -2c_1 \\]

From equation 3:
\\[ -3c_2 + 6c_3 = 0 \implies -3(-2c_1) + 6c_3 = 0 \implies 6c_1 + 6c_3 = 0 \implies c_3 = -c_1 \\]

Substitute \\( c_2 = -2c_1 \\) and \\( c_3 = -c_1 \\) into equation 1:
\\[ c_1 - (-2c_1) + 3(-c_1) = 0 \implies c_1 + 2c_1 - 3c_1 = 0 \implies 0 = 0 \\]

This holds true for any \\( c_1 \\). Let's choose \\( c_1 = 1 \\):

Then:
\\[ c_2 = -2 \\]
\\[ c_3 = -1 \\]

Thus, we have found constants \\( c_1 = 1, c_2 = -2, c_3 = -1 \\) such that:

\\[ 1 \cdot \beta_1 - 2 \cdot \beta_2 - 1 \cdot \beta_3 = 0 \\]

This proves that the vectors \\( \beta_1, \beta_2, \beta_3 \\) are linearly related.
