---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Development Dependencies and Build Tools
translated: false
type: note
---

### DevDependencies

These are packages used during development, not included in the final build.

- **babel-core** (6.13.0): Core Babel compiler for transpiling modern JavaScript (ES6+) to ES5 for broader browser compatibility.
- **babel-loader** (6.2.5): Webpack loader that integrates Babel for JavaScript transformation in build processes.
- **babel-plugin-transform-runtime** (6.12.0): Babel plugin that reuses runtime helpers to reduce bundle size in transpiled code.
- **babel-preset-es2015** (6.13.2): Babel preset for compiling ES2015 (ES6) features to ES5.
- **babel-runtime** (6.11.6): Runtime library providing polyfills and helpers for Babel-transpiled code.
- **cross-env** (^1.0.8): Sets environment variables cross-platform (e.g., NODE_ENV) without shell differences.
- **css-loader** (^0.23.1): Loads and processes CSS files, resolving imports and dependencies.
- **detect-indent** (4.0.0): Detects the indentation style (spaces/tabs) of files for consistent formatting.
- **exports-loader** (^0.6.3): Makes module exports available in different contexts (e.g., for non-AMD modules).
- **extract-text-webpack-plugin** (^1.0.1): Extracts CSS from JavaScript bundles into separate files for better performance.
- **file-loader** (0.9.0): Handles loading files (e.g., images) by emitting them to the output directory and returning URLs.
- **html-webpack-plugin** (^2.22.0): Generates HTML files and injects bundled assets, simplifying single-page app setups.
- **rimraf** (^2.5.4): Cross-platform recursive file removal (like rm -rf on Unix).
- **style-loader** (^0.13.1): Injects CSS into DOM via style tags for dynamic loading.
- **stylus** (^0.54.5): CSS preprocessor with expressive syntax, compiled to CSS.
- **stylus-loader** (^2.1.1): Webpack loader for processing Stylus files into CSS.
- **url-loader** (0.5.7): Base64-encodes small files (e.g., images) inline or emits larger ones; falls back to file-loader.
- **vue-hot-reload-api** (^1.2.0): Enables hot module replacement for Vue.js components during development.
- **vue-html-loader** (^1.0.0): Webpack loader for parsing HTML templates in Vue single-file components.
- **vue-loader** (8.5.3): Loads and processes Vue single-file components (.vue files) into JavaScript and CSS.
- **vue-style-loader** (^1.0.0): Handles CSS from Vue components, integrating with style-loader.
- **webpack** (1.13.2): Module bundler for building and optimizing web assets like JS, CSS, and images.
- **webpack-dev-server** (1.14.0): Development server with live reloading and hot module replacement.

### Dependencies

These are runtime packages included in the final application build.

- **debug** (^2.2.0): Debug utility with namespaced logging and conditional output (only enabled via DEBUG env var).
- **es6-promise** (^3.0.2): Polyfill for ES6 Promise API in older browsers/environments.
- **font-awesome** (^4.6.3): Popular icon library providing scalable vector icons via CSS classes.
- **github-markdown-css** (^2.4.0): CSS for styling GitHub-flavored Markdown.
- **highlight.js** (^9.6.0): Syntax highlighter for code blocks in multiple languages.
- **hls.js** (^0.7.6): JavaScript library for playing HTTP Live Streaming (HLS) videos with HTML5 video.
- **inherit** (^2.2.6): Utility for classical and prototypal inheritance in JavaScript objects.
- **jquery** (^3.1.0): Fast, feature-rich JavaScript library for DOM manipulation, AJAX, and events.
- **json-loader** (^0.5.4): Loads JSON files as JavaScript modules.
- **leancloud-realtime** (^3.2.3): SDK for LeanCloud's real-time messaging and data synchronization service.
- **marked** (^0.3.6): Markdown parser that converts Markdown to HTML.
- **moment** (^2.14.1): Date/time manipulation library for parsing, validating, and formatting dates.
- **moment-timezone** (^0.5.7): Extension for Moment.js to handle time zones and DST.
- **qiniu-js-sdk** (0.0.2): JavaScript SDK for interacting with Qiniu cloud storage (uploading/downloading files).
- **raw-loader** (^0.5.1): Webpack loader that loads files as raw strings (e.g., text templates).
- **rupture** (^0.6.1): Media query extension for Stylus, providing breakpoints for responsive design.
- **sprintf-js** (^1.0.3): JavaScript sprintf implementation for string formatting with placeholders.
- **vue** (^1.0.26): Progressive MVVM framework for building user interfaces (v1.x, which is older).
- **vue-resource** (^0.6.1): HTTP client for Vue.js to simplify AJAX/API requests.
- **vue-router** (^0.7.13): Official router for Vue.js, enabling single-page application navigation.
- **vue-spinner** (^1.0.2): Spinner/loading component library for Vue.js.
- **vue-weui** (^0.3.2): Vue.js wrappers for WeUI components (UI library for WeChat-style interfaces).
- **weixin-js-sdk** (^1.2.0): WeChat JavaScript SDK for integrating WeChat web features (e.g., sharing, scanning).
- **weui** (^0.4.3): WeUI CSS framework for building mobile interfaces inspired by WeChat's design.
- **word-color** (^1.2.0): Library for coloring words based on factors like hash or language, likely for heatmap-like effects.
