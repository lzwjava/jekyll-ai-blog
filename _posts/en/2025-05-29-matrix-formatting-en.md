---
audio: false
generated: true
lang: en
layout: post
title: Fixing Matrix Formatting in Jekyll Blog
translated: false
type: note
---

The issue you're facing is related to how Markdown (kramdown) processes the content before MathJax renders it. The double backslashes (`\\`) in your matrix are being interpreted by Markdown before MathJax gets to them, which breaks the matrix formatting.

Here are a few solutions to fix this:

### Solution 1: Escape the backslashes

You can escape each backslash with another backslash:

```latex
$A - I = \begin{pmatrix} 1 & -3 & 0 \\\ 2 & 1 & 0 \\\ 0 & 0 & 2 \end{pmatrix} - \begin{pmatrix} 1 & 0 & 0 \\\ 0 & 1 & 0 \\\ 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} 0 & -3 & 0 \\\ 2 & 0 & 0 \\\ 0 & 0 & 1 \end{pmatrix}$
```

### Solution 2: Use `\\` inside math blocks

For display math (not inline), use `$$` or `\\\[ \\\]`:

```latex
$$
A - I = \begin{pmatrix} 1 & -3 & 0 \\ 2 & 1 & 0 \\ 0 & 0 & 2 \end{pmatrix} - \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} 0 & -3 & 0 \\ 2 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$
```

### Solution 3: Use HTML tags to prevent Markdown processing

Wrap your math in HTML `div` tags to prevent Markdown processing:

```html
<div>
$$
A - I = \begin{pmatrix} 1 & -3 & 0 \\ 2 & 1 & 0 \\ 0 & 0 & 2 \end{pmatrix} - \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} 0 & -3 & 0 \\ 2 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$
</div>
```

### Solution 4: Modify your kramdown configuration

Add this to your `_config.yml` to prevent kramdown from processing math blocks:

```yaml
kramdown:
  math_engine: mathjax
  syntax_highlighter: rouge
```

Then you can use:

```latex
$$ A - I = \begin{pmatrix} 1 & -3 & 0 \\ 2 & 1 & 0 \\ 0 & 0 & 2 \end{pmatrix} - \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} 0 & -3 & 0 \\ 2 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix} $$
```

Try these solutions one by one to see which works best with your Jekyll setup. The most reliable solution is typically to use display math (`$$` or `\\\[ \\\]`) instead of inline math (`$`) for matrices and other complex equations.
