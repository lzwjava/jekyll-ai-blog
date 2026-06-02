---
audio: false
generated: true
lang: en
layout: post
title: Using Autoprefixer
translated: false
type: note
---

I'll explain how to use Autoprefixer in frontend development. Autoprefixer is a PostCSS plugin that automatically adds vendor prefixes to your CSS, ensuring cross-browser compatibility.

Here are the main ways to integrate Autoprefixer into your frontend workflow:

1. Using with npm (Most Common Approach)
```bash
# Install autoprefixer and postcss
npm install autoprefixer postcss --save-dev
```

2. Basic Setup with PostCSS CLI
```bash
# Install postcss-cli
npm install postcss-cli --save-dev

# Create a postcss.config.js file
module.exports = {
  plugins: [
    require('autoprefixer')
  ]
}

# Add to package.json scripts
"scripts": {
  "build:css": "postcss src/styles.css -o dist/styles.css"
}
```

3. With Build Tools:

a) Webpack with postcss-loader
```bash
npm install postcss-loader --save-dev
```

```javascript
// webpack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: ['autoprefixer']
              }
            }
          }
        ]
      }
    ]
  }
}
```

b) Vite (built-in support)
```javascript
// vite.config.js
import autoprefixer from 'autoprefixer'

export default {
  css: {
    postcss: {
      plugins: [autoprefixer()]
    }
  }
}
```

4. Configuration Options
```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('autoprefixer')({
      overrideBrowserslist: ['> 1%', 'last 2 versions'], // Target browsers
      grid: true, // Enable grid prefixes
      flexbox: 'no-2009' // Flexbox support options
    })
  ]
}
```

5. Example Usage in CSS
```css
/* Input */
.container {
  display: flex;
  justify-content: space-between;
}

/* Output (after Autoprefixer) */
.container {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  justify-content: space-between;
}
```

Key Features and Tips:
- Automatically adds prefixes based on Can I Use data
- Controlled by browserslist (usually in package.json)
- Removes outdated prefixes from older CSS
- Works with modern CSS features like custom properties

Basic browserslist example in package.json:
```json
{
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead"
  ]
}
```

To run:
```bash
# With PostCSS CLI
npx postcss src/*.css --dir dist

# Or with your npm script
npm run build:css
```

Choose the integration method based on your project's existing setup (Webpack, Vite, etc.). The Webpack or Vite approaches are most common in modern frontend development as they integrate well with existing build processes.
