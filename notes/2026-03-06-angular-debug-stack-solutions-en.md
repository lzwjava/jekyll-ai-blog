---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debugging Angular Stack Overflow Solutions
translated: false
type: note
---

**Question:** Could we update ivy/index.js source code to output the stack there (in order to debug the "Maximum call stack size exceeded" error during Angular migration)?

**Answer:**

Yes — it is technically possible, but it is **usually not a good or practical solution**. Here's why, and what you can do instead.

### Why patching @ngtools/webpack/src/ivy/index.js is difficult / not recommended

- The file is inside `node_modules/@ngtools/webpack/src/ivy/index.js`
- It is part of a compiled/transpiled package — the real logic lives in TypeScript sources in the Angular repository
- node_modules is normally overwritten on every `npm install` / `npm ci`
- Even if you patch it, most teams consider this a maintenance nightmare (breaks on next `@angular-devkit/build-angular` update)

### Realistic ways to get a better stack trace

1. **Best & cleanest option: use NODE_OPTIONS --stack-trace-limit**

   Most modern node versions respect this flag:

   ```bash
   # Try 200–500 first, then go higher if needed
   NODE_OPTIONS="--stack-trace-limit=300" ng build

   # or even higher
   NODE_OPTIONS="--stack-trace-limit=1000" ng build --verbose
   ```

   This often reveals 5–15 more frames and usually shows you **which file / symbol / decorator / import** is causing the recursion.

2. **Patch temporarily using patch-package (most controllable way)**

   Steps:

   ```bash
   npm install --save-dev patch-package
   ```

   - Open `node_modules/@ngtools/webpack/src/ivy/index.js`
   - Find the place where it throws the RangeError (search for "Maximum call stack size exceeded")
   - Replace / wrap it like this:

     ```js
     // original probably looks roughly like:
     throw new Error("Maximum call stack size exceeded");

     // change to:
     const err = new Error("Maximum call stack size exceeded");
     err.stack = new Error().stack;           // capture fuller stack
     console.error("[IVY PATCH] Deep recursion detected");
     console.error(err.stack);
     throw err;
     ```

   - Then run:

     ```bash
     npx patch-package @ngtools/webpack
     ```

   - Commit the generated `patches/@ngtools+webpack+...patch` file
   - Add `"postinstall": "patch-package"` to package.json scripts

   → Now every time you `npm install`, the patch is applied automatically.

3. **Use a debugger instead of patching**

   - Add this to your `package.json` scripts:

     ```json
     "build:debug": "node --inspect-brk ./node_modules/@angular-devkit/build-angular/src/dev-server/index.js"
     ```

   - Or simpler — just run the builder in inspect mode:

     ```bash
     node --inspect-brk ./node_modules/.bin/ng build
     ```

   - Open chrome://inspect → connect → set breakpoint on the line that throws "Maximum call stack size exceeded"
   - When it pauses, look at the call stack in Chrome DevTools

4. **Quick & dirty – monkey-patch at runtime**

   Create a file `debug-ivy.js`:

   ```js
   const originalError = Error;

   Error = function (...args) {
     const err = new originalError(...args);
     if (args[0]?.includes?.("Maximum call stack size exceeded")) {
       console.error("[DEBUG] Ivy recursion crash");
       console.error(new originalError().stack); // capture outer stack
       console.error(err.stack);
     }
     return err;
   };
   Error.prototype = originalError.prototype;
   ```

   Then run:

   ```bash
   node -r ./debug-ivy.js ./node_modules/.bin/ng build
   ```

### Summary – Recommended order

1. First try → `NODE_OPTIONS="--stack-trace-limit=500" ng build --verbose`
2. If still not enough → use `patch-package` on ivy/index.js (easiest to maintain)
3. If you really need deep debugging → use `--inspect-brk` + Chrome debugger
4. Avoid editing node_modules directly without patch-package

In 95% of real-world cases people solve the underlying circular import after seeing just 30–50 more stack frames via `--stack-trace-limit`.

Patching the source is possible — but should be your last resort, not first choice.

**References:**

- <https://github.com/angular/angular-cli/issues?q=is%3Aissue+label%3A%22type%3A+bug%22+%22Maximum+call+stack%22>
- <https://stackoverflow.com/questions/73197135/angular-14-ng-serve-error-ngtools-webpack-src-ivy-index-js-error-maximum>
