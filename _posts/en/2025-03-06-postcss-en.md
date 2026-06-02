---
audio: false
generated: true
lang: en
layout: post
title: Using PostCSS for Transforming CSS
translated: false
type: note
---

I'll explain how to use PostCSS in a frontend project. PostCSS is a tool for transforming CSS with JavaScript plugins, offering features like autoprefixing, minification, and future CSS syntax support. Here's a step-by-step guide:

### 1. **Set Up Your Project**

Ensure you have a frontend project with Node.js installed. If not, initialize one:

```bash
mkdir my-project
cd my-project
npm init -y
```

### 2. **Install PostCSS and Required Tools**

Install PostCSS, the PostCSS CLI, and any plugins you want to use (e.g., `autoprefixer` for vendor prefixes or `cssnano` for minification):

```bash
npm install --save-dev postcss postcss-cli autoprefixer cssnano
```

### 3. **Create a CSS File**

Create a source CSS file, e.g., `src/styles.css`:

```css
/* src/styles.css */
.container {
  display: flex;
  transition: all 0.3s ease;
}
```

### 4. **Configure PostCSS**

Create a `postcss.config.js` file in your project root to specify plugins:

```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('autoprefixer'), // Adds vendor prefixes
    require('cssnano')({ preset: 'default' }) // Minifies CSS
  ]
};
```

### 5. **Add a Build Script**

In your `package.json`, add a script to process your CSS with PostCSS:

```json
"scripts": {
  "build:css": "postcss src/styles.css -o dist/styles.css"
}
```

- `src/styles.css`: Input file
- `dist/styles.css`: Output file

### 6. **Run PostCSS**

Run the build command:

```bash
npm run build:css
```

This processes `src/styles.css` and outputs the transformed CSS to `dist/styles.css`. For example, `autoprefixer` might add prefixes, and `cssnano` will minify it:

```css
/* dist/styles.css */
.container{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-transition:all .3s ease;transition:all .3s ease}
```

### 7. **Integrate with a Build Tool (Optional)**

For a more robust setup, integrate PostCSS with tools like Webpack, Vite, or Gulp:

#### **With Vite**

If using Vite, install `postcss` and configure it in `vite.config.js`:

```javascript
// vite.config.js
import postcss from 'postcss';
import autoprefixer from 'autoprefixer';

export default {
  css: {
    postcss: {
      plugins: [autoprefixer()]
    }
  }
};
```

Vite handles PostCSS automatically when you import CSS files.

#### **With Webpack**

Install `postcss-loader`:

```bash
npm install --save-dev postcss-loader
```

Update your `webpack.config.js`:

```javascript
module.exports = {
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader']
      }
    ]
  }
};
```

### 8. **Watch for Changes (Optional)**

To process CSS automatically during development, modify your `package.json` script:

```json
"scripts": {
  "watch:css": "postcss src/styles.css -o dist/styles.css --watch"
}
```

Run `npm run watch:css` to watch for file changes.

### 9. **Common Plugins**

Here are some popular PostCSS plugins:

- `autoprefixer`: Adds vendor prefixes based on browser support.
- `cssnano`: Minifies CSS.
- `postcss-preset-env`: Lets you use future CSS features today.
- `postcss-import`: Resolves `@import` rules.
Install them as needed:

```bash
npm install --save-dev postcss-preset-env postcss-import
```

Add them to `postcss.config.js`:

```javascript
module.exports = {
  plugins: [
    require('postcss-import'),
    require('postcss-preset-env'),
    require('autoprefixer'),
    require('cssnano')({ preset: 'default' })
  ]
};
```

### Example Workflow

1. Write modern CSS in `src/styles.css`:

```css
@custom-media --viewport-medium (width >= 768px);

:root {
  --main-color: #1a73e8;
}

.container {
  color: var(--main-color);
  display: grid;
}

@media (--viewport-medium) {
  .container {
    grid-template-columns: 1fr 1fr;
  }
}
```

2. Run `npm run build:css`.
3. Get processed CSS in `dist/styles.css` with prefixes, resolved variables, and minification.

### Tips

- Use `--map` in the CLI (`postcss src/styles.css -o dist/styles.css --map`) to generate source maps for debugging.
- Check plugin docs for specific configuration options.
- Combine with a frontend framework (React, Vue, etc.) by linking the output CSS to your HTML or bundler.

Let me know if you need help with a specific setup or plugin!
