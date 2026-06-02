---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dependency Cruiser for Angular 21 Standalone
translated: false
type: note
---

**Question:** Give more details on using dependency-cruiser in Angular projects. Does it work with Angular 21's standalone components (module-less architecture)?

**Answer:**

**Dependency-cruiser** is an excellent choice for dependency analysis in Angular projects — including modern Angular versions (up to Angular 21 in 2026) — because it works at the **static source code level** and understands **TypeScript imports**.

### Key Advantages Over Tools Like Madge
- Much more powerful **custom rules** (forbidden dependencies, layer violations, no circulars, no feature → core imports, etc.)
- Excellent **circular dependency** detection (with full cycle paths shown)
- Many **report formats** (err, json, html, dot/graphviz, svg, mermaid, d3, csv, ...)
- CI-friendly `--output-type err` + exit code ≠ 0 when violations occur
- Supports **TypeScript** very well (including path aliases from `tsconfig.json`)

### Does It Work With Angular 21 + Standalone Components?
**Yes — it works perfectly well.**

Angular 21 (like versions since ~19) uses **standalone: true** by default and eliminates most NgModules.
Dependency-cruiser doesn't care about Angular's runtime module system or `@Component({ standalone: true, imports: […] })` — it only follows the **static import / export graph** in your TypeScript files.

So it will correctly detect:
- Regular `import { Something } from './something.component';`
- Barrel re-exports (`export * from './comp';`)
- Path aliases (`@app/shared`, `@core`, etc.)
- Circular dependencies between standalone components (very common in recursive trees, dialogs, etc.)

**Important note about circular dependencies in standalone components**

Angular itself sometimes requires `forwardRef(() => OtherComponent)` in the `imports: []` array to break circular *runtime* references.
**Dependency-cruiser ignores forwardRef** — it still sees the static `import` statement and will report the cycle.

This is actually **desirable** behavior in most teams:
- You usually want to know about **architectural cycles** even if Angular can technically handle them via `forwardRef`
- Many teams forbid cycles completely (except perhaps in very specific cases like recursive components)

If you want to allow certain cycles (e.g., recursive UI patterns), you can write a rule to **forbid most cycles but allow specific folders or named exceptions**.

### Recommended Setup for Angular 21 Project

```bash
# Install
npm install --save-dev dependency-cruiser

# Create default config (very good starting point)
npx depcruise --init
```

This creates `.dependency-cruiser.js` — edit it to add Angular-friendly rules:

```javascript
// .dependency-cruiser.js (example snippet)
module.exports = {
  forbidden: [
    // Classic: no circular dependencies at all
    {
      name: "no-circular",
      comment: "Don't allow circular dependencies",
      severity: "error",
      from: {},
      to: {
        circular: true
      }
    },

    // Optional: no feature components importing core/domain
    {
      name: "no-feature-to-core",
      comment: "Features shouldn't import core/domain logic",
      severity: "warn",
      from: { path: "^src/app/features" },
      to:   { path: "^src/app/core|^src/app/domain" }
    },

    // Optional: enforce clean architecture layers
    {
      name: "no-presentation-to-infrastructure",
      severity: "error",
      from: { path: "^src/app/(components|pages|features)" },
      to:   { path: "^src/app/infrastructure" }
    }
  ],

  options: {
    // Important for Angular path aliases
    doNotFollow: {
      path: "node_modules"
    },

    tsPreCompilationDeps: true,          // understand type-only imports
    tsConfig: { fileName: "tsconfig.json" }, // read paths/aliases

    // nicer output in CI
    reporterOptions: {
      dot: { collapsePattern: "^src/app/[^/]+" }
    }
  }
};
```

Run it:

```bash
# Quick check (fails CI if violations)
npx depcruise src --validate

# Only circulars, compact output
npx depcruise src --include-only "^src" --output-type err --ruleset .dependency-cruiser.js

# Beautiful interactive graph (open in browser)
npx depcruise src --output-type d3 --output-to dependency-graph.html

# CI example (exit ≠0 on violation)
npx depcruise src --validate || exit 1
```

Many large Angular monorepos (Nx, custom setups) use dependency-cruiser successfully in CI to enforce “no circular dependencies” and layered architecture — even with 100% standalone components.

**References:**

- [dependency-cruiser GitHub](https://github.com/sverweij/dependency-cruiser)
- [dependency-cruiser rules reference](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md)
- [dependency-cruiser npm page](https://www.npmjs.com/package/dependency-cruiser)
