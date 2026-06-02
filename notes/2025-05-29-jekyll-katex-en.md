---
audio: false
generated: true
lang: en
layout: post
title: Using KaTeX in Jekyll
translated: false
type: note
---

To use KaTeX instead of MathJax in Jekyll with your current setup, you'll need to replace the MathJax scripts with KaTeX and adjust your Jekyll configuration. KaTeX is faster and lighter than MathJax, but it requires a different approach since it doesn't support all of MathJax's features (e.g., automatic equation numbering is more manual). Below is a step-by-step guide to switch to KaTeX in your Jekyll site:

### 1. Update Your Jekyll Configuration
Modify your `_config.yml` to use KaTeX as the math engine for Kramdown. Update the `kramdown` section as follows:

```yaml
kramdown:
  math_engine: katex
  input: GFM
  syntax_highlighter: rouge
```

This tells Kramdown to render LaTeX math expressions using KaTeX instead of MathJax.

### 2. Include KaTeX in Your HTML
Remove the MathJax scripts from your HTML and replace them with KaTeX. You can include KaTeX via a CDN. Add the following to the `<head>` section of your Jekyll layout file (e.g., `_layouts/default.html`):

```html
<!-- KaTeX CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" integrity="sha384-nB0miv6/jRmo5SLY8cTjmnkA3wC7o1L0jOey4Cki5N3kdjdPD/mW59G1Qsxa8c3y" crossorigin="anonymous">

<!-- KaTeX JS -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" integrity="sha384-7zkKLzPD3M4y9W8FWsN4Z0yO5eLu8qUn0QHY6hZ2r3fDzqjk0McYc3vJrmE2h6cZ" crossorigin="anonymous"></script>

<!-- Auto-render extension (optional, for automatic rendering of math) -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" integrity="sha384-43gviWU0YVjaDtb/GhzOouOXtZMP/7XUzwPTL0xF3iS9Ho94fSc31UyUyIDgWvB4" crossorigin="anonymous"></script>

<!-- Auto-render configuration -->
<script>
  document.addEventListener("DOMContentLoaded", function() {
    renderMathInElement(document.body, {
      delimiters: [
        {left: "$$", right: "$$", display: true}, // Block math
        {left: "\\[", right: "\\]", display: true}, // Block math
        {left: "\\(", right: "\\)", display: false}, // Inline math
        {left: "$", right: "$", display: false} // Inline math
      ],
      throwOnError: false
    });
  });
</script>
```

### 3. Remove MathJax Configuration
Delete the MathJax-related code from your layout file, including the `<script type="text/x-mathjax-config">` block and the MathJax CDN script. KaTeX doesn't use a configuration like MathJax's `tex2jax`, and the above auto-render script handles similar functionality.

### 4. Write Math in Your Markdown
With KaTeX and Kramdown configured, you can write LaTeX math in your Markdown files using the same delimiters as before:

- **Inline math**: Use `$...$` or `\(...\)` (e.g., `$E=mc^2$` or `\(E=mc^2\)`).
- **Display math**: Use `$$...$$` or `\[...\]` (e.g., `$$E=mc^2$$` or `\[E=mc^2\]`).

For example:

```markdown
Inline math: $E=mc^2$ or \(E=mc^2\).

Display math:
$$E=mc^2$$

or

\[E=mc^2\]
```

Kramdown with the KaTeX math engine will process these into HTML that KaTeX renders.

### 5. Notes on KaTeX vs. MathJax
- **Automatic Equation Numbering**: KaTeX doesn't support automatic equation numbering like MathJax's `autoNumber: "AMS"`. If you need equation numbers, you must manually add them using `\tag{}` in your LaTeX code (e.g., `$$E=mc^2 \tag{1}$$`).
- **Performance**: KaTeX is significantly faster than MathJax, which is ideal for static sites like Jekyll.
- **Feature Set**: KaTeX supports fewer LaTeX commands than MathJax. Check the [KaTeX supported functions](https://katex.org/docs/supported.html) to ensure your math expressions are compatible.
- **Rendering**: The auto-render script above mimics MathJax's behavior by automatically rendering math expressions within the specified delimiters. Adjust the `delimiters` array in the script if you want to change or limit the delimiters.

### 6. Test Your Setup
Run your Jekyll site locally (`jekyll serve`) and verify that math expressions render correctly. If you encounter issues:
- Check the browser console for KaTeX-related errors.
- Ensure the KaTeX CDN URLs are up-to-date (the ones above use version 0.16.11, the latest as of my knowledge).
- Confirm that your Markdown files use valid KaTeX-compatible LaTeX syntax.

### 7. Optional: Local KaTeX Files
If you prefer to host KaTeX files locally to avoid CDN dependency:
1. Download `katex.min.css`, `katex.min.js`, and `auto-render.min.js` from the [KaTeX GitHub releases](https://github.com/KaTeX/KaTeX/releases).
2. Place them in your Jekyll assets folder (e.g., `assets/katex/`).
3. Update the `<link>` and `<script>` tags to point to your local files (e.g., `/assets/katex/katex.min.css`).

### 8. Troubleshooting
- **Math not rendering**: Ensure the KaTeX scripts are loading correctly and the `kramdown.math_engine` is set to `katex`.
- **Delimiter issues**: Verify that your delimiters in the auto-render script match those in your Markdown.
- **Unsupported commands**: If a LaTeX command fails, check the KaTeX documentation for supported commands or rewrite the expression.

If you need specific help with a particular math expression or configuration, share the details, and I can provide tailored guidance!
