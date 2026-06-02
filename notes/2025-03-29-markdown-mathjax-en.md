---
audio: false
generated: true
lang: en
layout: post
title: Markdown Rendering with MathJax or KaTeX
translated: false
type: note
---

To combine LaTeX math rendering with **Markdown** rendering on a webpage, you would typically use a JavaScript library (like **MathJax** or **KaTeX**) alongside a Markdown parser that can process standard Markdown syntax. The goal is to allow users to write math formulas in LaTeX within Markdown and have them rendered properly on the page.

Here’s how you can achieve this:

### 1. **Markdown Rendering with MathJax or KaTeX**

You can use a **Markdown parser** like **marked.js** or **remarkable.js** to render the basic Markdown content. Then, after rendering the Markdown content, use MathJax or KaTeX to render the LaTeX math inside it.

Below is a step-by-step approach to achieve this.

---

### **Step 1: Include Libraries**

You need to include both a **Markdown parser** and a **Math rendering library** (MathJax or KaTeX) in your HTML file.

Here’s how you can include them:

```html
<!-- Include KaTeX (or MathJax) for LaTeX rendering -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.15.3/katex.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.15.3/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.15.3/contrib/auto-render.min.js"></script>

<!-- Include a Markdown parser (like marked.js) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.0.10/marked.min.js"></script>
```

Alternatively, if you prefer **MathJax** instead of KaTeX, you can include MathJax like this:

```html
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
```

---

### **Step 2: Setup the Markdown to LaTeX Rendering Process**

Now, you can write your HTML structure and use JavaScript to render the Markdown and then process any LaTeX formulas within that Markdown.

Here is a simple example:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Markdown + Math Rendering</title>

  <!-- Include KaTeX for math rendering -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.15.3/katex.min.css">
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.15.3/katex.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.15.3/contrib/auto-render.min.js"></script>

  <!-- Include marked.js for Markdown rendering -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.0.10/marked.min.js"></script>
</head>
<body>

  <h1>Markdown + Math Rendering Example</h1>

  <!-- Textarea for Markdown input -->
  <textarea id="markdownInput" rows="10" cols="50">
This is a Markdown editor. You can add LaTeX math formulas like this:

Inline math: \( E = mc^2 \)

Block math:
\[
\int_0^1 x^2 \, dx = \frac{1}{3}
\]
  </textarea>

  <hr>

  <!-- Container for rendered Markdown -->
  <div id="markdownOutput"></div>

  <script>
    // Function to render Markdown + Math
    function renderMarkdown() {
      // Get the input Markdown
      const markdownText = document.getElementById('markdownInput').value;

      // Render the Markdown content
      const htmlContent = marked(markdownText);

      // Insert the rendered HTML into the output div
      document.getElementById('markdownOutput').innerHTML = htmlContent;

      // Render the math inside the HTML content using KaTeX
      renderMathInElement(document.getElementById('markdownOutput'), {
        delimiters: [
          { left: "\\(", right: "\\)", display: false }, // inline math
          { left: "\\[", right: "\\]", display: true }   // block math
        ]
      });
    }

    // Call the renderMarkdown function on page load and when user changes input
    renderMarkdown();
    document.getElementById('markdownInput').addEventListener('input', renderMarkdown);
  </script>
</body>
</html>
```

### **Explanation of the Code:**

1. **Markdown Parsing:**
   - The `marked.js` library is used to convert the input Markdown (written in the `<textarea>`) into HTML. The Markdown syntax will be processed and converted into HTML in the `<div id="markdownOutput"></div>` container.

2. **Math Rendering:**
   - The LaTeX equations in the Markdown (inline `\( ... \)` and block `\[ ... \]`) are rendered using **KaTeX**'s `renderMathInElement()` function.
   - **KaTeX** looks for `\( ... \)` for inline math and `\[ ... \]` for block math in the HTML content and automatically renders them.

3. **Interactive Markdown Editor:**
   - As the user types in the `<textarea>`, the `renderMarkdown` function is called to update the content dynamically, parsing the Markdown and rendering the LaTeX formulas.

---

### **Step 3: Customizing for Different Frontend Frameworks**

You can adapt this solution to work with any frontend framework like **React**, **Vue**, or **Angular**. For example, here's a **React** implementation for real-time Markdown + LaTeX rendering:

#### **React Example**

1. **Install KaTeX and marked via npm:**

```bash
npm install katex marked
```

2. **React Component for Markdown + Math Rendering:**

```jsx
import React, { useState, useEffect } from 'react';
import marked from 'marked';
import katex from 'katex';
import 'katex/dist/katex.min.css';

const MarkdownEditor = () => {
  const [markdown, setMarkdown] = useState('');

  useEffect(() => {
    // Render math formulas using KaTeX after the component mounts
    renderMath();
  }, [markdown]);

  const renderMath = () => {
    const renderedHTML = marked(markdown);
    document.getElementById('markdownOutput').innerHTML = renderedHTML;

    // Render LaTeX math formulas with KaTeX
    katex.renderMathInElement(document.getElementById('markdownOutput'), {
      delimiters: [
        { left: "\\(", right: "\\)", display: false }, // inline math
        { left: "\\[", right: "\\]", display: true }   // block math
      ]
    });
  };

  return (
    <div>
      <h1>Markdown + Math Rendering</h1>
      <textarea
        value={markdown}
        onChange={(e) => setMarkdown(e.target.value)}
        rows="10"
        cols="50"
      />
      <hr />
      <div id="markdownOutput"></div>
    </div>
  );
};

export default MarkdownEditor;
```

In the React version, we use the `marked` library to convert the Markdown text to HTML, and KaTeX’s `renderMathInElement()` function to process and render any LaTeX math formulas inside the HTML.

---

### **Summary**

- Use a **Markdown parser** (like `marked.js`) to convert Markdown syntax into HTML.
- Use **MathJax** or **KaTeX** to render LaTeX math expressions embedded in the Markdown content.
- Combine both by rendering Markdown to HTML and processing math formulas dynamically using KaTeX/MathJax.

This approach allows users to write and preview Markdown content with mathematical equations in real-time, which is perfect for applications like blog editors, knowledge base systems, or educational tools!
