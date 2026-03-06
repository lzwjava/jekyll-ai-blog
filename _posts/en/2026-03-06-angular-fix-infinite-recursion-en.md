---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Angular Infinite Recursion Error
translated: false
type: note
---

**Question:** Why do main.ts and polyfills.ts module builds fail with an error in @ngtools/webpack/src/ivy/index.js: "Error: Maximum call stack size exceeded" when migrating from Angular 14 to Angular 21, and how to fix it?

**Answer:**

This error almost always means the **Angular compiler (via Ivy in @ngtools/webpack)** has entered an infinite recursion / loop during the analysis or metadata processing phase of your application.

It shows up very early — usually on **main.ts** and **polyfills.ts** — because these entry files pull in the entire app graph, and the compiler crashes while trying to process circular or deeply recursive imports.

### Most Common Causes During Large Migrations (14 → 17/18/19/20/21)

- Circular imports / circular module dependencies (very common after major version jumps)
- A module that accidentally imports **itself** (direct or indirect via barrel files)
- Very old barrel files (`index.ts` re-exporting everything) that create huge import cycles after stricter Ivy / esbuild-based compilation rules
- Incorrect lazy-loading setup or NgModule imports that form a cycle
- Very rarely: extremely deep component nesting / recursive templates (but this usually crashes at runtime, not build time)
- Third-party library with broken metadata / very old code that the new compiler can't handle

### How to Fix (Step-by-Step)

1. **Clean everything first** (eliminates many false positives)

   ```bash
   rm -rf node_modules
   rm -rf dist
   npm cache clean --force
   npm install
   ```

2. **Look for circular dependencies**

   Install a helpful tool:

   ```bash
   npm install -g madge
   ```

   Then run (adjust entry point if needed):

   ```bash
   madge --circular --extensions ts src/
   madge --circular src/main.ts
   ```

   Fix every reported cycle — this solves ~70–80% of these errors.

3. **Check for self-importing modules**

   Search your codebase for patterns like:

   ```ts
   // in src/app/feature/feature.module.ts
   import { FeatureModule } from './feature.module';
   ```

   Or barrel files doing:

   ```ts
   // src/app/shared/index.ts
   export * from './shared.module';
   ```

   → delete or refactor such barrels.

4. **Try incremental compilation off** (sometimes helps identify the real file)

   ```bash
   ng build --no-progress --verbose
   ```

   Or temporarily add to angular.json:

   ```json
   "architect": {
     "build": {
       "options": {
         "progress": false
       }
     }
   }
   ```

5. **Migrate step-by-step if possible**

   Jumping from 14 directly to 21 is very aggressive (many breaking changes in 15, 16, 17 — standalone components, esbuild, new control flow, etc.).

   Recommended path:

   14 → 15 → 16 → 17 → 18 → 19 → 20 → 21

   Use official update guide each time:

   https://update.angular.dev/

   Run `ng update @angular/cli@next @angular/core@next` at each step and fix one version at a time.

6. **Quick workarounds to narrow down the problem** (not permanent fixes)

   - Temporarily comment out almost all imports in **app.module.ts** → see if it builds
   - Convert to **standalone bootstrap** (Angular 17+) — removes NgModule graph complexity

     ```ts
     // main.ts
     import { bootstrapApplication } from '@angular/platform-browser';
     import { AppComponent } from './app/app.component';
     bootstrapApplication(AppComponent);
     ```

   - Remove third-party modules one by one from AppModule

7. **If you are already on Angular 17+ and still see @ngtools/webpack**

   You should see **esbuild** instead in modern Angular versions.

   Force modern builder:

   ```bash
   ng build --esbuild
   ```

   Or update angular.json to use `@angular-devkit/build-angular:application` (new in v17+).

### Summary – Quick Action Plan

- Run **madge** → fix all circular dependencies
- Delete / refactor bad barrel files
- Migrate version-by-version (don't jump 14 → 21 directly)
- Clean node_modules & reinstall
- If stuck → create minimal reproduction → share on GitHub / Stack Overflow

This error is **almost never an Angular bug** — it's your project's import graph that the stricter/faster compiler no longer tolerates.

**References:**

- https://stackoverflow.com/questions/73197135/angular-14-ng-serve-error-ngtools-webpack-src-ivy-index-js-error-maximum
- https://github.com/angular/angular-cli/issues/26969
- https://github.com/angular/angular-cli/issues/23597
- https://github.com/angular/angular-cli/issues/23814