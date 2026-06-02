---
audio: false
generated: true
lang: zh
layout: post
title: MathJax问题排查指南
translated: true
type: note
---

您的 MathJax 配置似乎存在问题。让我们根据您提供的代码来识别并修复这个问题。

### 当前配置
您当前的 MathJax 配置如下：

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ["\\(","\\)"] ],
      displayMath: [ ['$$','$$'], ["\[","\]"] ],
      processEscapes: true
    },
    "HTML-CSS": { linebreaks: { automatic: true } },
    "CommonHTML": {
      linebreaks: { automatic: true },
      scale: 85
    },
    TeX: { equationNumbers: { autoNumber: "AMS" } }
  });
</script>

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
```

此配置旨在：
- 在 `\( ... \)` 分隔符之间渲染行内数学公式
- 在 `$$ ... $$` 或 `\[ ... \]` 分隔符之间渲染显示数学公式
- 启用对长公式的自动换行
- 使用 CommonHTML 输出处理器将数学输出缩放至 85%
- 使用 AMS 样式自动编号公式

但您报告说它"无法正常工作"，这可能意味着数学公式没有渲染，或者特定功能（如自动换行）没有按预期工作。

### 问题所在
主要问题在于 `displayMath` 分隔符配置：

```javascript
displayMath: [ ['$$','$$'], ["\[","\]"] ]
```

在 JavaScript 中，字符串 `"["` 被字面解释为 `[`，因为 `\[` 不是一个特殊的转义序列——它只是一个反斜杠后跟一个方括号。同样，`"\]"` 变成了 `]`。因此，MathJax 被配置为将 `[ ... ]` 识别为显示数学分隔符，**而不是** `\[ ... \]`。由于您的数学表达式（如示例 `\[ \text{Bit rate} = 2400 \, \text{baud} \times 3 \, \text{bits/symbol} = 7200 \, \text{bits per second (bps)} \]`）使用的是 `\[ ... \]`，MathJax 在当前设置下不会将它们识别为显示数学公式。

行内数学分隔符 `["\\(","\\)"]` 是正确的，因为 JavaScript 字符串中的 `\\(` 和 `\\)` 表示 `\(` 和 `\)`——这是行内数学公式的标准 LaTeX 分隔符。但是，显示数学分隔符需要调整。

### 解决方案
要修复此问题，请更新 `displayMath` 配置，使 MathJax 正确识别 `\[ ... \]` 作为显示数学分隔符。在 JavaScript 中，要表示字符串 `\[`，您需要写成 `"\\["`，因为每个反斜杠都必须被转义。同样，`\]` 变为 `"\\]"`。以下是修正后的配置：

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ["\\(","\\)"] ],
      displayMath: [ ["$$","$$"], ["\\[","\\]"] ],
      processEscapes: true
    },
    "HTML-CSS": { linebreaks: { automatic: true } },
    "CommonHTML": {
      linebreaks: { automatic: true },
      scale: 85
    },
    TeX: { equationNumbers: { autoNumber: "AMS" } }
  });
</script>

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
```

#### 关键更改
- 将 `displayMath` 数组中的 `["\[","\]"]` 更改为 `["\\[","\\]"]`
- 这确保了分隔符设置为 `\[ ... \]`（和 `$$ ... $$`），与标准 LaTeX 表示法匹配

### 其他注意事项
1. **自动换行问题**：您提到某些表达式过长导致溢出，尤其是在移动端视图中。`"CommonHTML"` 输出处理器中的 `linebreaks: { automatic: true }` 设置应处理此问题，但这要求数学公式位于具有定义宽度的容器内（例如 `width: 100%`）。请确保您的 HTML 结构包含类似内容：

   ```html
   <div style="width: 100%; overflow-x: auto;">
     \[ \text{Bit rate} = 2400 \, \text{baud} \times 3 \, \text{bits/symbol} = 7200 \, \text{bits per second (bps)} \]
   </div>
   ```

   这允许 MathJax 根据容器的宽度进行换行，适应屏幕尺寸。

2. **输出处理器**：您的脚本加载了 `TeX-MML-AM_CHTML`，默认使用 CommonHTML 输出。`"CommonHTML"` 设置（例如 `scale: 85`、`linebreaks: { automatic: true }`）将生效，但 `"HTML-CSS"` 设置可能不会生效，因为该输出处理器未激活。由于 CommonHTML 是现代且广泛支持的，这没问题——只需确保您的设置与其对齐。

3. **测试**：更新配置后，使用您的示例表达式进行测试：

   ```html
   \[ \text{Bit rate} = 2400 \, \text{baud} \times 3 \, \text{bits/symbol} = 7200 \, \text{bits per second (bps)} \]
   ```

   它现在应正确渲染为显示数学公式，并在需要时进行适当的换行。

4. **浏览器兼容性**：MathJax 2.7.7 应在大多数现代浏览器中工作。如果问题仍然存在，请确保控制台中没有 JavaScript 错误或冲突的 CSS 规则（例如 `white-space: nowrap`）覆盖数学渲染。

### 最终修正代码
以下是完整、修正后的设置：

```html
<!-- MathJax Configuration -->
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ["\\(","\\)"] ],
      displayMath: [ ["$$","$$"], ["\\[","\\]"] ],
      processEscapes: true
    },
    "CommonHTML": {
      linebreaks: { automatic: true },
      scale: 85
    },
    TeX: { equationNumbers: { autoNumber: "AMS" } }
  });
</script>

<!-- Load MathJax -->
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

<!-- Example Math -->
<div style="width: 100%; overflow-x: auto;">
  \[ \text{Bit rate} = 2400 \, \text{baud} \times 3 \, \text{bits/symbol} = 7200 \, \text{bits per second (bps)} \]
</div>
```

### 为何此解决方案有效
- **分隔符修复**：`["\\[","\\]"]` 确保 MathJax 将 `\[ ... \]` 识别为显示数学公式，与您的内容匹配
- **自动换行**：具有适当容器的 `CommonHTML` 设置可对长表达式启用自动换行
- **渲染**：CDN 脚本和配置共同确保数学公式被正确处理和显示

使用此修复程序更新您的代码，您的 MathJax 设置应该按预期工作！如果问题仍然存在，请分享失败的数学表达式的具体示例或遇到的任何错误消息。

---

为了配置 MathJax 以良好地渲染所提供内容中的数学表达式，您需要确保它能正确处理像 \( T_p \) 和 \( 2 \times T_p \) 这样的行内数学表达式，这些表达式用 LaTeX 风格的分隔符括起来。内容使用 `\( ... \)` 表示行内数学，虽然它不包含显示数学（例如，单独成行的方程），但为了灵活性，最好将 MathJax 配置为同时支持行内和显示数学。以下是实现此目标的分步指南。

### 第 1 步：在 HTML 中包含 MathJax
首先，您需要加载 MathJax 库。您可以使用内容分发网络 (CDN) 将其包含在 HTML 文件中。将以下脚本标签添加到 HTML 的 `<head>` 或包含数学公式的内容之前：

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js?config=TeX-AMS_CHTML"></script>
```

这将加载 MathJax 2.7.9 版本及 `TeX-AMS_CHTML` 配置，该配置支持 LaTeX 输入并将数学公式渲染为带 CSS 的 HTML，适用于大多数 Web 应用程序。

### 第 2 步：配置 MathJax 分隔符
MathJax 需要知道识别数学表达式的分隔符。内容使用 `\( ... \)` 表示行内数学，这是标准的 LaTeX 分隔符。为确保 MathJax 正确处理这些，请在 MathJax 库脚本之前添加一个配置脚本。以下是基本配置：

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['\\(', '\\)'] ],
      displayMath: [ ['$$', '$$'], ['\\[', '\\]'] ],
      processEscapes: true
    }
  });
</script>
```

- **`inlineMath`**：告诉 MathJax 将 `\( ... \)` 之间的文本视为行内数学。使用双括号 `[ ['\\(', '\\)'] ]` 是因为 MathJax 接受分隔符对的数组。
- **`displayMath`**：配置 MathJax 将 `$$ ... $$` 和 `\[ ... \]` 识别为显示数学，即使当前内容未使用这些。这确保了与未来内容的兼容性。
- **`processEscapes`**：允许转义分隔符（例如，使用 `\$` 显示字面美元符号），尽管对于此特定内容而言并非关键。

### 第 3 步：增强响应式渲染能力
为使渲染的数学公式适应不同的屏幕尺寸（例如，防止在移动设备上溢出），请对长表达式启用自动换行。像这样更新配置：

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['\\(', '\\)'] ],
      displayMath: [ ['$$', '$$'], ['\\[', '\\]'] ],
      processEscapes: true
    },
    "HTML-CSS": { linebreaks: { automatic: true } },
    CommonHTML: { linebreaks: { automatic: true } },
    SVG: { linebreaks: { automatic: true } }
  });
</script>
```

- **`HTML-CSS`、`CommonHTML`、`SVG`**：这些是 MathJax 用于渲染数学公式的输出处理器。启用 `linebreaks: { automatic: true }` 可确保长表达式自然换行，尽管此内容中的表达式（\( T_p \)、\( 2 \times T_p \)）很短，不太可能需要换行。

### 第 4 步：整合所有内容
以下是在您的内容之前需要包含在 HTML 文件中的完整设置：

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['\\(', '\\)'] ],
      displayMath: [ ['$$', '$$'], ['\\[', '\\]'] ],
      processEscapes: true
    },
    "HTML-CSS": { linebreaks: { automatic: true } },
    CommonHTML: { linebreaks: { automatic: true } },
    SVG: { linebreaks: { automatic: true } }
  });
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js?config=TeX-AMS_CHTML"></script>
```

### 第 5 步：验证内容是否正确渲染
使用此配置，您内容中的行内数学——例如 \( T_p \) 和 \( 2 \times T_p \)——将渲染为格式正确的数学表达式。例如：
- \( T_p \) 变为带下标的变量。
- \( 2 \times T_p \) 显示为带乘号 (×) 和下标的 \( T_p \)。

### 其他注意事项
- **无显示数学**：由于您的内容仅使用行内数学，`displayMath` 设置并非严格必需，但为了完整性而包含。
- **CSS 样式**：确保您内容的 HTML 容器（例如 `<div>`）具有 `width: 100%` 或适当的样式以保持布局的响应性。
- **测试**：添加此配置后，在浏览器中加载您的页面，确认 \( T_p \) 和 \( 2 \times T_p \) 按预期渲染。

此设置确保 MathJax 清晰且专业地渲染您 CSMA/CD 解释中的数学表达式，从而增强用户的可读性。

---

要修复 MathJax 在渲染括号 `\(...\)` 和其他 LaTeX 分隔符时的问题，请调整您的配置，以在 JavaScript 字符串中正确转义反斜杠。以下是修正后的设置：

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['\\(','\\)'] ],  // 正确转义以用于 JavaScript
      displayMath: [ ['$$','$$'], ['\\[','\\]'] ],  // 修复了 \[ 和 \] 的转义
      processEscapes: true
    },
    "HTML-CSS": { linebreaks: { automatic: true } },
    "CommonHTML": {
      linebreaks: { automatic: true },
      scale: 85
    },
    TeX: { equationNumbers: { autoNumber: "AMS" } }
  });
</script>

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
```

### 关键修复：
1. **转义反斜杠**：
   - 将 `["\\(","\\)"]` 改为 `['\\(','\\)']`（单引号避免了额外的转义）。
   - 将 `["\[","\]"]` 修复为 `['\\[','\\]']` 以确保 `\[...\]` 对显示公式有效。

2. **建议**：
   - 对显示公式使用 `'$$...$$'` 或 `\\[...\\]`。
   - 对行内公式使用 `\\(...\\)`。
   - 确保没有冲突的 Markdown 处理器更改您的 LaTeX。

### 使用示例：
```html
<p>行内数学：\( E = mc^2 \)。</p>

<p>显示数学：</p>
\[
  \int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}
\]
```

此配置确保 MathJax 正确解析所有 LaTeX 分隔符。

---

我理解您正在使用 Jekyll 和 Kramdown 来渲染 Markdown 文章，并希望配置 MathJax 以正确显示数学表达式。您已经提供了一个 MathJax 配置，并注意到您是在 Markdown 文章中而非 HTML 标签内渲染数学公式。让我们确保 MathJax 能与您的设置无缝协作。

### 您当前的设置
您正在使用：
- **带 Kramdown 的 Jekyll**：Kramdown 是 Jekyll 的默认 Markdown 解析器，支持 LaTeX 风格的数学表达式。
- **MathJax**：您的配置指定了行内和显示数学公式的分隔符：
  - 行内：`\( ... \)`
  - 显示：`$$ ... $$` 和 `\[ ... \]`

您还包含了一个 `marked.min.js` 脚本，但由于 Jekyll 使用 Kramdown 在服务器端渲染 Markdown，而不是在客户端，因此它可能不相关。

### 渲染可能无法工作的原因
Kramdown 和 MathJax 需要在对分隔符的处理上保持一致。您的 MathJax 设置将 `\( ... \)` 识别为行内数学公式，并将 `$$ ... $$` 和 `\[ ... \]` 识别为显示数学公式。然而，除非配置正确，否则 Kramdown 的默认行为可能不会将所有分隔符正确传递给 MathJax，特别是在 Markdown 中出现转义问题时。

### 解决方案：使用 Kramdown 配置 MathJax
以下是使其工作的方法：

#### 1. 在 Jekyll 中配置 Kramdown
确保您的 Jekyll `_config.yml` 文件启用了 MathJax 作为 Kramdown 的数学引擎。添加或验证以下内容：

```yaml
markdown: kramdown
kramdown:
  math_engine: mathjax
```

这告诉 Kramdown 处理数学表达式并将其传递给 MathJax。默认情况下，Kramdown 识别：
- `\( ... \)` 用于行内数学公式。
- `$$ ... $$` 用于显示数学公式。

虽然您的 MathJax 配置也支持 `\[ ... \]` 用于显示数学公式，但 Kramdown 本身不使用此分隔符，除非正确处理，否则可能导致问题。

#### 2. 在 Markdown 中使用一致的数学分隔符
为避免混淆或转义问题，请在 Markdown 文章中坚持使用 Kramdown 的默认分隔符：
- **行内数学公式**：使用 `\( ... \)`。
  示例：`这是行内公式：\( E = mc^2 \)` 渲染为 "这是行内公式：\( E = mc^2 \)"。
- **显示数学公式**：使用 `$$ ... $$`。
  示例：
  ```markdown
  $$
  \int_0^1 x^2 \, dx = \frac{1}{3}
  $$
  ```
  这将渲染为居中的公式：\( \int_0^1 x^2 \, dx = \frac{1}{3} \)。

如果您偏好 `\[ ... \]`，您可以使用它，但 Markdown 的反斜杠转义可能需要特别注意（例如 `\\[ ... \\]`）。然而，`$$ ... $$` 更简单，并且与 Kramdown 的默认设置一致，减少了潜在的错误。

#### 3. 简化您的 MathJax 配置
由于 Kramdown 对数学公式进行了预处理，您的 MathJax 配置可以专注于渲染。以下是根据您的设置简化的版本：

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['\\(','\\)'] ],
      displayMath: [ ['$$','$$'] ], // 坚持使用 $$ 以求简单
      processEscapes: true
    },
    "CommonHTML": {
      linebreaks: { automatic: true },
      scale: 85
    },
    TeX: { equationNumbers: { autoNumber: "AMS" } }
  });
</script>

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
```

- 我已从 `displayMath` 中移除了 `['\\[','\\]']` 以匹配 Kramdown 对 `$$ ... $$` 的偏好。如果您仍想使用 `\[ ... \]`，请保留它，但请彻底测试。
- 移除了 `"HTML-CSS"`，因为 `"CommonHTML"` 对于现代 MathJax 渲染已足够。

将其放在您 Jekyll 布局的 `<head>` 部分。

#### 4. 移除不必要的脚本
您包含了 `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>`，但由于 Jekyll 在服务器端使用 Kramdown，除非您正在用它做特定的事情，否则不需要 Marked.js（一个客户端解析器）。如果不是，请移除它以避免潜在的冲突或混淆。

#### 5. 测试您的设置
将这些示例添加到 Markdown 文章中以确认渲染有效：
- 行内：`能量是 \( E = mc^2 \)。`
- 显示：
  ```markdown
  $$
  \text{Bit rate} = 2400 \, \text{baud} \times 3 \, \text{bits/symbol} = 7200 \, \text{bps}
  $$
  ```

运行 `jekyll serve`，在浏览器中打开网站，并检查数学公式是否正确渲染。如果没有，请检查浏览器控制台中的 MathJax 错误。

### 最后说明
- **一致性**：使用 `\( ... \)` 和 `$$ ... $$` 可确保 Kramdown 和 MathJax 之间的兼容性，而无需额外的转义麻烦。
- **故障排除**：如果数学公式仍未渲染，请验证：
  - MathJax 脚本加载无误（检查浏览器控制台）。
  - 您的 Jekyll 构建成功完成。
  - 分隔符或配置中没有拼写错误。

此设置应在 Jekyll Markdown 文章中完美渲染您的数学表达式！如果您在尝试渲染的示例中遇到具体问题，请告知我。
