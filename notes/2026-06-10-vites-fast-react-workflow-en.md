---
audio: false
generated: true
image: false
lang: en
layout: post
title: Vite's Fast React Workflow
translated: false
type: note
---

Question: How does Vite work with React?

Answer:

Vite (French for "fast") is a modern frontend build tool that has largely replaced older tools like Create React App (Webpack) for bundling and serving React applications. It provides a blazing-fast development experience by completely shifting how files are handled during development versus production.

Here is a breakdown of exactly how Vite works behind the scenes with React.

---

## 1. Development: On-Demand and Native ESM

Traditional bundlers like Webpack build and bundle your **entire** React application into a single JavaScript file before serving it to the browser. As your app grows, this makes the initial startup and reload times crawl.

Vite handles this differently:

* **Native ES Modules (ESM):** Vite leverages modern browser support for Native ES Modules. Instead of bundling your code upfront, Vite lets the browser do the heavy lifting. When you open your app, the browser requests the entry file (`main.jsx`) and follows the `import` statements natively.
* **On-Demand Compiling:** Vite only compiles and serves the specific React components or modules that the browser is currently requesting. If a component isn't on the screen or in use, Vite doesn't waste time processing it.

```
Traditional Bundler (Webpack):
[Entry] -> [Bundle Entire App] -> [Server Ready] (Slow)

Vite Dev Server:
[Entry] -> [Server Ready Instantly] -> [Compile on demand as Browser requests modules] (Fast)

```

---

## 2. Speeding Up Third-Party Dependencies (Esbuild)

React apps rely heavily on large node modules (like `react`, `react-dom`, or `lodash`). If the browser requested every individual file inside these dependencies, it would cause hundreds of network requests and slow down the page load.

To solve this, Vite uses a tool called **Esbuild** (written in Rust) to **pre-bundle** your external dependencies into single modules during the initial setup. Because Esbuild is written in a compiled language, it processes these dependencies 10 to 100 times faster than JavaScript-based bundlers.

---

## 3. Instant Changes: Hot Module Replacement (HMR)

When you modify a React component and hit save, you want to see the change instantly without losing your application's state (e.g., inputs in a form or an open modal).

* Vite uses native ESM to perform **Hot Module Replacement (HMR)** over WebSockets.
* When a file changes, Vite invalidates the link between the edited module and its boundary, replacing only that specific file in the browser.
* By pairing this with official plugins like `@vitejs/plugin-react` or `@vitejs/plugin-react-swc`, it hooks perfectly into React's Fast Refresh, updating the UI smoothly while preserving your component state.

---

## 4. Production: Optimized Bundling (Rollup)

While unbundled native ESM is ideal for local development, shipping hundreds of unbundled files to production over the internet causes network bottlenecks.

When you run `npm run build`, Vite switches strategies:

* It uses **Rollup** to compile, minify, and bundle your React application into highly optimized, static HTML, CSS, and JS assets.
* It automatically applies advanced production optimizations like **tree-shaking** (removing unused code) and automatic **code-splitting** (breaking down your app into smaller chunks that load asynchronously per route).

---

## Summary of the React + Vite File Structure

When you scaffold a Vite project, the entry point looks a bit different than older setups:

* **`index.html` is front and center:** Instead of being hidden in a public folder, `index.html` sits in the root directory. It acts as the literal entry point for Vite, using a standard `<script type="module" src="/src/main.jsx"></script>` tag to start the app.
* **`.jsx` / `.tsx` extensions are mandatory:** Vite strictly enforces correct file extensions so it knows exactly when to apply React-specific transformations to your code.
