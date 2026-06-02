---
audio: false
generated: true
lang: zh
layout: post
title: Hugo中的LaTeX渲染
translated: true
type: note
---

您描述的问题出现在 **Jekyll** 中使用 **Kramdown** 并配置 **MathJax** 作为数学引擎时。当 Kramdown 配置了 `math_engine: mathjax` 时，它会将 Markdown 内容中的圆括号 `( )` 解释为 LaTeX 行内数学公式的分隔符（例如 `\( \)`），这可能会破坏包含圆括号的普通文本。这是因为 MathJax 被设置为解析 `\( \)` 或 `$ $` 作为行内数学公式，正如您的配置所示。

在 **Hugo** 中，默认情况下不太可能出现此问题，但这取决于您如何配置 Hugo 的 Markdown 处理器和 MathJax 集成。下面，我将解释为什么 Hugo 在大多数情况下能避免此问题，如何在 Jekyll 中预防或修复它，以及如何确保它在 Hugo 中不会发生。

---

### **Hugo 有这个问题吗？**
Hugo 通常能避免此问题，因为：
1.  **Markdown 处理器**：Hugo 使用 **Goldmark**（或可选地使用 Blackfriday）作为其默认的 Markdown 渲染器，它默认不启用 MathJax 或 LaTeX 解析。除非您显式配置 Hugo 使用 MathJax 并设置行内数学分隔符如 `\( \)`，否则您内容中的普通圆括号 `( )` 不会被误解为 LaTeX。
2.  **MathJax 集成**：Hugo 本身不解析 LaTeX。如果您需要 MathJax 支持，您必须手动将 MathJax 脚本（如您提供的那个）添加到您主题的模板中（例如，在 `layouts/partials/head.html`）并配置分隔符。Hugo 的灵活性允许您控制 MathJax 如何处理内容，从而避免自动解析 `( )`，除非显式启用。
3.  **数学公式的短代码**：Hugo 用户通常使用短代码（例如 `{{< math >}}...{{< /math >}}`）来实现 LaTeX 渲染，这明确指定了数学内容，防止普通圆括号被误认为是 LaTeX。

总之，除非您配置 MathJax 使用相同的行内分隔符（`\( \)`）并且在没有适当保护措施的情况下启用自动解析，否则 Hugo 不会遇到此问题。通过使用短代码或避免使用 `\( \)` 作为分隔符，Hugo 可以完全避开此问题。

---

### **在 Jekyll 中修复此问题**
在 Jekyll 中，出现此问题是因为 Kramdown 的 `math_engine: mathjax` 设置，结合您的 MathJax 配置，导致 `( )` 被解析为 LaTeX。以下是修复方法：

#### **1. 更改 MathJax 行内分隔符**
修改 MathJax 配置，使用不同的行内数学分隔符，例如 `$ $`，而不是 `\( \)`，以避免与普通圆括号冲突。在您 Jekyll 站点的 HTML 中更新脚本（例如在 `_includes/head.html` 中）：

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [['$','$']], // 使用 $ $ 作为行内数学分隔符
      displayMath: [['$$','$$'], ['\[','\]']],
      processEscapes: true // 允许转义 $ 以按字面意思使用它
    },
    "HTML-CSS": { linebreaks: { automatic: true } },
    "CommonHTML": { linebreaks: { automatic: true } },
    TeX: { equationNumbers: { autoNumber: "AMS" } }
  });
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
```

-   **为什么有效**：通过从 `inlineMath` 中移除 `['\(','\)']`，MathJax 不再将 `( )` 解释为 LaTeX 分隔符，从而保留它们用于普通文本。`processEscapes: true` 设置允许您在 Markdown 中写入 `\$` 来显示字面量的 `$`（如果需要）。
-   **在您的 Markdown 中**：使用 `$x^2$` 作为行内数学公式，而不是 `\(x^2\)`。例如：
    ```markdown
    这是一个公式：$x^2 + y^2 = z^2$。普通文本（不会被解析）。
    ```

#### **2. 在 Markdown 中转义圆括号**
如果您想保留 `\( \)` 作为分隔符，请在您的 Markdown 内容中转义圆括号，以防止 Kramdown/MathJax 将它们解析为 LaTeX。在每个圆括号前使用反斜杠 `\`：

```markdown
普通文本 \(not a formula\)。这是一个真正的公式：\(x^2 + y^2\)。
```

-   **输出**：转义的 `\(not a formula\)` 将渲染为 `(not a formula)`，而 `\(x^2 + y^2\)` 将渲染为 LaTeX 公式。
-   **缺点**：这需要手动转义内容中的每一个 `( )` 实例，对于大型站点来说可能很繁琐。

#### **3. 为特定页面禁用 MathJax**
如果您只需要在某些页面（例如，数学内容较多的文章）上使用 MathJax，请默认禁用它，并仅在需要时启用：
-   从全局的 `_layouts/default.html` 或 `_includes/head.html` 中移除 MathJax 脚本。
-   在您的布局或页面 Front Matter 中添加条件包含。例如，在 `_layouts/post.html` 中：

{% raw %}
```html
{% if page.mathjax %}
  <script type="text/x-mathjax-config">
    MathJax.Hub.Config({
      tex2jax: {
        inlineMath: [['$','$']],
        displayMath: [['$$','$$'], ['\[','\]']],
        processEscapes: true
      }
    });
  </script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
{% endif %}
```
{% endraw %}

-   在您 Markdown 文件的 Front Matter 中，仅为特定页面启用 MathJax：
    ```yaml
    ---
    title: 我的数学文章
    mathjax: true
    ---
    ```

-   **为什么有效**：没有设置 `mathjax: true` 的页面不会加载 MathJax，因此 `( )` 不会被解析为 LaTeX。

#### **4. 使用不同的数学引擎**
从 MathJax 切换到 Kramdown 支持的其他数学引擎，例如 **KaTeX**，它速度更快，并且除非显式配置，否则不太可能误解圆括号。在您的 Jekyll 站点中安装 KaTeX：
-   将 KaTeX 脚本添加到 `_includes/head.html`：
    ```html
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/auto-render.min.js"></script>
    <script>
      document.addEventListener("DOMContentLoaded", function() {
        renderMathInElement(document.body, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false }
          ]
        });
      });
    </script>
    ```
-   更新 `_config.yml`：
    ```yaml
    kramdown:
      math_engine: katex
      input: GFM
      syntax_highlighter: rouge
    ```

-   **为什么有效**：KaTeX 对解析更严格，并且默认使用 `$ $` 作为行内数学分隔符，减少了与 `( )` 的冲突。它也比 MathJax 更快。

---

### **确保 Hugo 避免此问题**
要在 Hugo 中使用 MathJax 而不遇到 `( )` 解析问题，请遵循以下步骤：

1.  **将 MathJax 添加到 Hugo**：
    -   将 MathJax 脚本放在您主题的局部模板中（例如 `layouts/partials/head.html`）：
{% raw %}
        ```html
        {{ if .Params.mathjax }}
        <script type="text/x-mathjax-config">
          MathJax.Hub.Config({
            tex2jax: {
              inlineMath: [['$','$']],
              displayMath: [['$$','$$'], ['\[','\]']],
              processEscapes: true
            },
            "HTML-CSS": { linebreaks: { automatic: true } },
            "CommonHTML": { linebreaks: { automatic: true } },
            TeX: { equationNumbers: { autoNumber: "AMS" } }
          });
        </script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
        {{ end }}
        ```
{% endraw %}
    -   通过在前言中设置来为特定页面启用 MathJax：
        ```yaml
        ---
        title: 我的数学文章
        mathjax: true
        ---
        ```

2.  **使用短代码处理数学公式**：
    创建一个短代码（例如 `layouts/shortcodes/math.html`）来显式包装数学内容：
{% raw %}
    ```html
    {{ if .IsNamedParams }}
      <span class="math">{{ .Get "content" | safeHTML }}</span>
    {{ else }}
      <span class="math">{{ .Inner | safeHTML }}</span>
    {{ end }}
    ```
{% endraw %}
    在您的 Markdown 中使用它：
{% raw %}
    ```markdown
    普通文本（不会被解析）。公式：{{< math >}}$x^2 + y^2${{< /math >}}。
    ```
{% endraw %}
    -   **为什么有效**：短代码确保只有明确标记的内容才会被作为数学公式处理，而普通文本中的 `( )` 则保持不变。

3.  **改用 KaTeX**：
    Hugo 用户通常更喜欢 KaTeX，因为它速度更快。将 KaTeX 添加到 `layouts/partials/head.html`：
{% raw %}
    ```html
    {{ if .Params.math }}
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/auto-render.min.js"></script>
    <script>
      document.addEventListener("DOMContentLoaded", function() {
        renderMathInElement(document.body, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false }
          ]
        });
      });
    </script>
    {{ end }}
    ```
{% endraw %}
    在前言中启用它：
    ```yaml
    math: true
    ```
    使用 `$ $` 作为行内数学分隔符以避免 `( )` 冲突。

---

### **推荐**
-   **对于 Jekyll**：切换到使用 `$ $` 作为 MathJax 的分隔符，或使用 KaTeX，以避免 `( )` 解析问题。转义圆括号是一种备用方案，但对于大型站点来说不太实用。
-   **对于 Hugo**：除非您显式配置 MathJax 使用 `\( \)` 分隔符，否则您不太可能遇到此问题。使用短代码或 KaTeX 进行数学公式渲染，以确保普通圆括号的安全。

如果您正在从 Jekyll 迁移到 Hugo，并希望保留您的数学内容，我建议在 Hugo 中使用 KaTeX 并配合短代码进行显式控制。如果您需要帮助设置 Hugo 的 MathJax/KaTeX 集成或转换您 Jekyll 站点的数学内容，请告诉我！
