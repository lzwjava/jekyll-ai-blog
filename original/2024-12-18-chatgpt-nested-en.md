---
audio: true
generated: false
image: false
lang: en
layout: post
title: ChatGPT’s Bug with Nested Code Blocks
type: post
---

### Issue Explanation

The problem arises because Jekyll’s Markdown parser struggles with nested code blocks when using triple backticks (\`\`\`). When you attempt to nest code blocks inside each other using the same delimiter, the parser often misinterprets the structure, resulting in rendering issues. Specifically, using triple backticks inside another block that also uses triple backticks causes the parser to fail in correctly parsing and rendering the content, which can break the layout or misalign the code.

This issue becomes especially problematic when you need to showcase code examples in a post that includes nested code blocks, such as configurations or templates. You might encounter situations where the inner code block doesn’t render correctly or the outer code block is incorrectly displayed.

---

### Why Does This Happen?

This problem occurs because Jekyll’s Markdown parser does not handle nested code blocks with the same delimiter (\`\`\`) correctly. When it encounters a code block inside another, it misinterprets the nested structure and causes rendering issues. This can result in broken or misaligned content in the rendered post.

---

### Current Solution

Currently, the most effective workaround for this problem is to use HTML `<pre>` tags for inner code blocks instead of relying on triple backticks. This ensures that the parser correctly handles the nested content. However, there is no ideal solution in Jekyll to handle nested code blocks purely with Markdown syntax without encountering rendering problems.

---

### Summary

At present, nested code blocks using triple backticks do not render correctly in Jekyll. The parser struggles with handling nested structures, causing formatting issues. Using HTML `<pre>` tags for inner code blocks is a common workaround, but there is no perfect solution for rendering nested code blocks using only Markdown syntax in Jekyll.
