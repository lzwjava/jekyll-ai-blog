---
audio: false
generated: true
lang: en
layout: post
title: JavaScript library for Markdown
translated: false
type: note
---

It seems like you're asking about how to use the `marked` library, version `^0.3.6`, which is a JavaScript library for parsing Markdown text and converting it to HTML. Since you're referencing a specific version with the `^0.3.6` notation (likely from a `package.json` file in a Node.js project), I'll guide you through using this older version of `marked`. Note that version `0.3.6` is quite old (released around 2016), and the library has evolved significantly since then. However, I'll stick to what works for that version.

### Step 1: Installation

If you're working in a Node.js environment, you can install `marked` version `0.3.6` using npm:

```bash
npm install marked@0.3.6
```

The `^0.3.6` in a `package.json` means it will install `0.3.6` or any compatible patch updates (e.g., `0.3.7`), but for clarity, the command above locks it to exactly `0.3.6`.

### Step 2: Basic Usage

Here’s how to use `marked` version `0.3.6` in different environments:

#### In Node.js

1. **Require the library**:
   Create a file (e.g., `index.js`) and add the following:

   ```javascript
   var marked = require('marked');
   ```

2. **Convert Markdown to HTML**:
   Use the `marked()` function by passing a Markdown string to it. For example:

   ```javascript
   var markdownString = '# Hello World\nThis is **bold** text.';
   var html = marked(markdownString);
   console.log(html);
   ```

   **Output**:

   ```html
   <h1>Hello World</h1>
   <p>This is <strong>bold</strong> text.</p>
   ```

#### In the Browser

1. **Include the library**:
   You can use a CDN or download `marked@0.3.6` and include it via a `<script>` tag. For example, using a historical CDN link (if available) or a local file:

   ```html
   <script src="https://cdn.jsdelivr.net/npm/marked@0.3.6"></script>
   ```

2. **Use it in JavaScript**:
   After including the script, `marked` will be available globally:

   ```html
   <script>
     var markdownString = '# Hello World\nThis is **bold** text.';
     var html = marked(markdownString);
     console.log(html);
   </script>
   ```

### Step 3: Options (for version 0.3.6)

Version `0.3.6` supports some customization options. You can pass an options object as the second argument to `marked()`. Here’s an example:

```javascript
var markdownString = '# Hello\nThis is *text* with `code`.';
var html = marked(markdownString, {
  gfm: true,         // Enable GitHub Flavored Markdown
  tables: true,      // Enable GFM tables
  breaks: false,     // If true, adds <br> on single line breaks
  pedantic: false,   // If true, follows strict Markdown spec
  sanitize: false,   // If true, strips HTML tags for security
  smartLists: true,  // Improves list rendering
  smartypants: false // If true, uses "smart" typography (e.g., curly quotes)
});
console.log(html);
```

### Key Features in 0.3.6

- **Basic Markdown**: Supports headings (`#`), bold (`**`), italic (`*`), lists, code blocks (```), etc.
- **GFM Support**: GitHub Flavored Markdown (like tables and task lists) is available if `gfm: true` is set.
- **No Renderer Customization**: Unlike newer versions, `0.3.6` doesn’t support custom renderers, so you’re limited to its default output.

### Example with More Markdown

Here’s a fuller example in Node.js:

```javascript
var marked = require('marked');

var markdown = `
# My Title
## Subtitle

- Item 1
- Item 2

\`\`\`
console.log("Hello");
\`\`\`

| Name  | Age |
|-------|-----|
| Alice | 25  |
| Bob   | 30  |
`;

var html = marked(markdown, { gfm: true, tables: true });
console.log(html);
```

**Output**:

```html
<h1>My Title</h1>
<h2>Subtitle</h2>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
<pre><code>console.log("Hello");
</code></pre>
<table>
<thead>
<tr>
<th>Name</th>
<th>Age</th>
</tr>
</thead>
<tbody>
<tr>
<td>Alice</td>
<td>25</td>
</tr>
<tr>
<td>Bob</td>
<td>30</td>
</tr>
</tbody>
</table>
```

### Notes

- **Sanitization**: If you’re rendering user input, set `sanitize: true` to strip out raw HTML for security (e.g., `<script>` tags). However, this is basic in `0.3.6` and not as robust as modern alternatives.
- **Limitations**: This version lacks features added in later releases (e.g., async parsing, custom tokenizers), so if you need more, consider upgrading to a newer version like `5.x`.
- **Debugging**: If it’s not working, ensure the library is loaded correctly and check the Markdown syntax.
