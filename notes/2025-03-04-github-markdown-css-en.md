---
audio: false
generated: true
lang: en
layout: post
title: GitHub's Markdown Styling
translated: false
type: note
---

### Key Points
- It seems likely that to use the "github-markdown-css" npm package, you first install it with `npm install github-markdown-css`.
- Research suggests you then import the CSS file into your project and wrap your Markdown content in a div with the class "markdown-body".
- The evidence leans toward setting optional width and padding to match GitHub's style, and ensuring a DOctype to avoid styling issues.

### Installation
Start by installing the package using npm in your project directory:
- Run `npm install github-markdown-css` to add it to your dependencies.

### Usage
After installation, integrate the CSS into your project:
- Import the CSS file, for example, in JavaScript/React with `import 'github-markdown-css';`.
- Wrap your rendered Markdown content in a `<div class="markdown-body">...</div>` to apply the styles.
- Optionally, add CSS for width and padding to mimic GitHub's look:
  ```css
  .markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
  }
  @media (max-width: 767px) {
    .markdown-body {
      padding: 15px;
    }
  }
  ```
- Ensure your HTML includes a DOctype (e.g., `<!DOCTYPE html>`) to prevent quirks mode issues, which could affect styling.

### Unexpected Detail
You might not expect that the package also supports generating custom CSS via a related package, [generate-github-markdown-css](https://www.npmjs.com/package/generate-github-markdown-css), if you need tailored styles.

---

### Survey Note: Comprehensive Guide to Using the github-markdown-css npm Package

This detailed guide explores the usage of the "github-markdown-css" npm package, designed to replicate GitHub's Markdown styling in web projects. It provides a step-by-step approach for installation and integration, along with additional considerations for optimal use, especially in various development contexts like React or plain HTML. The information is derived from official package documentation, GitHub repositories, and related web resources, ensuring a thorough understanding for developers at all levels.

#### Background and Purpose
The "github-markdown-css" package, maintained by [sindresorhus](https://github.com/sindresorhus), offers a minimal set of CSS to emulate GitHub's Markdown rendering style. This is particularly useful for developers who want their Markdown content, such as documentation or blog posts, to appear consistent with GitHub's familiar and clean presentation. The package is widely used, with over 1,168 other projects in the npm registry utilizing it, indicating its popularity and reliability as of recent updates.

#### Installation Process
To begin, you need to install the package via npm, the Node.js package manager. The command is straightforward:
- Execute `npm install github-markdown-css` in your project directory. This adds the package to your `node_modules` folder and updates your `package.json` with the dependency.

The package's latest version, as of recent checks, is 5.8.1, last published about three months ago, suggesting active maintenance and updates. This ensures compatibility with modern web development practices and frameworks.

#### Integration and Usage
Once installed, the next step is to integrate the CSS into your project. The package provides a file named `github-markdown.css`, which you can import depending on your project setup:

- **For JavaScript/Modern Frameworks (e.g., React, Vue):**
  - Use an import statement in your JavaScript or TypeScript files, such as `import 'github-markdown-css';`. This works well with bundlers like Webpack or Vite, which handle CSS imports seamlessly.
  - For React, you might see examples where developers import it in a component file, ensuring the styles are available globally or scoped as needed.

- **For Plain HTML:**
  - Link the CSS file directly in your HTML head section:
    ```html
    <link rel="stylesheet" href="node_modules/github-markdown-css/github-markdown.css">
    ```
  - Note that the path might vary based on your project structure; ensure the relative path points correctly to the `node_modules` directory.

After importing, apply the styles by wrapping your rendered Markdown content in a `<div>` with the class "markdown-body". For example:
```html
<div class="markdown-body">
  <h1>Unicorns</h1>
  <p>All the things</p>
</div>
```
This class is crucial as the CSS targets elements within `.markdown-body` to apply GitHub-like styling, including typography, code blocks, tables, and more.

#### Styling Considerations
To fully replicate GitHub's Markdown appearance, consider setting the width and padding for the `.markdown-body` class. The documentation suggests:
- A maximum width of 980px, with 45px padding on larger screens, and 15px padding on mobile devices (screens ≤ 767px).
- You can achieve this with the following CSS:
  ```css
  .markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
  }
  @media (max-width: 767px) {
    .markdown-body {
      padding: 15px;
    }
  }
  ```
This ensures responsiveness and aligns with GitHub's design, enhancing readability and user experience.

#### Technical Notes and Best Practices
- **DOctype Requirement:** The documentation highlights potential styling issues, such as tables in dark mode rendering incorrectly, if the browser enters quirks mode. To prevent this, always include a DOctype at the top of your HTML, such as `<!DOCTYPE html>`. This ensures standards-compliant rendering and avoids unexpected behavior.
- **Markdown Parsing:** While the package provides CSS, it doesn't parse Markdown to HTML. You'll need a Markdown parser like [marked.js](https://marked.js.org/) or [react-markdown](https://github.com/remarkjs/react-markdown) for React projects to convert Markdown text to HTML, which can then be styled with this CSS.
- **Custom CSS Generation:** For advanced users, the related package [generate-github-markdown-css](https://www.npmjs.com/package/generate-github-markdown-css) allows generating custom CSS, potentially useful for specific theming or modifications. This is an unexpected detail for those who might assume the package is only for direct use.

#### Usage in Specific Contexts
- **React Projects:** In React, combining `github-markdown-css` with `react-markdown` is common. After installing both, import the CSS and use the component:
  ```javascript
  import React from 'react';
  import ReactMarkdown from 'react-markdown';
  import 'github-markdown-css';

  const MarkdownComponent = () => (
    <div className="markdown-body">
      <ReactMarkdown># Hello, World!</ReactMarkdown>
    </div>
  );
  ```
  Ensure you also set the width and padding CSS as shown earlier for full GitHub styling.

- **Plain HTML with CDN:** For quick prototyping, you can use a CDN version, available at [cdnjs](https://cdnjs.com/libraries/github-markdown-css), by linking directly:
  ```html
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown.min.css">
  ```
  Then apply the `.markdown-body` class as before.

#### Potential Issues and Solutions
- **Styling Conflicts:** If your project uses other CSS frameworks (e.g., Tailwind, Bootstrap), ensure there are no specificity conflicts. The `.markdown-body` class should override most styles, but test thoroughly.
- **Dark Mode Support:** The package includes support for dark mode, but ensure your Markdown parser and project setup handle theme switching correctly, especially for code blocks and tables.
- **Browser Compatibility:** Given the package's widespread use, compatibility is generally good, but always test across major browsers (Chrome, Firefox, Safari) to ensure consistent rendering.

#### Comparative Analysis
Compared to other Markdown CSS options, like [Markdown CSS](https://markdowncss.github.io/), "github-markdown-css" stands out for its direct replication of GitHub's style, making it ideal for documentation mirroring GitHub's look. However, it lacks built-in theming options without additional customization, unlike some alternatives that offer multiple themes out of the box.

#### Table: Key Features and Considerations

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Installation Command     | `npm install github-markdown-css`                                           |
| CSS Import Method        | `import 'github-markdown-css';` or `<link>` in HTML                         |
| Required Class           | `.markdown-body` for styling application                                    |
| Width and Padding        | Max 980px, 45px padding (desktop); 15px padding (mobile ≤ 767px)            |
| DOctype Requirement      | Essential to avoid quirks mode and ensure proper rendering                  |
| Custom CSS Generation    | Possible via [generate-github-markdown-css](https://www.npmjs.com/package/generate-github-markdown-css) |
| Compatibility            | Works with Markdown parsers like marked.js, react-markdown; broad browser support |

#### Conclusion
Using "github-markdown-css" is straightforward for developers seeking to replicate GitHub's Markdown styling. By following the installation and integration steps, and considering additional styling and technical notes, you can achieve a consistent and professional look for your Markdown content. For advanced customization, explore the generation package, and always test for compatibility and rendering issues, especially in complex projects.

#### Key Citations
- [github-markdown-css npm package page](https://www.npmjs.com/package/github-markdown-css)
- [The minimal amount of CSS to replicate GitHub Markdown style GitHub repo](https://github.com/sindresorhus/github-markdown-css)
- [GitHub Markdown CSS demo page](https://sindresorhus.com/github-markdown-css/)
- [Generate the CSS for github-markdown-css npm package](https://www.npmjs.com/package/generate-github-markdown-css)
- [github-markdown-css CDN by cdnjs](https://cdnjs.com/libraries/github-markdown-css)
