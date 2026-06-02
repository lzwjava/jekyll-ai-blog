---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debug Angular Circular Dependencies Fast
translated: false
type: note
---

**Question:** How to find out which component or module has circular issues with its imports or standalone components in Angular 21?

**Answer:**

In Angular 21 (and since ~v14–v17 with Ivy + standalone push), circular imports often cause:

- build-time stack overflow in `@ngtools/webpack` / esbuild
- NG0919: Circular Dependency Detected
- NG0200: Circular Dependency in DI
- ReferenceError / Cannot access before initialization (especially with standalone)

Here are the most effective ways to locate the exact files causing circular dependencies in 2026-era Angular projects.

### 1. Use `madge` – still the #1 recommended tool (official Angular docs suggest it)

```bash
# Install once (recommended as dev dep)
npm install --save-dev madge

# Quick check
npx madge --circular --extensions ts src/

# More precise (start from entry point)
npx madge --circular src/main.ts

# Show warning level too (barrels, side-effects, etc.)
npx madge --circular --warning src/

# Generate visual graph (very helpful!)
npx madge --circular --extensions ts --image deps.svg src/
# then open deps.svg in browser
```

- Output example:
  ```
  ✖ Found 3 circular dependencies!
  1) src/app/featureA.component.ts → src/app/shared/utils.service.ts → src/app/featureA.component.ts
  2) src/app/dashboard/dashboard.component.ts → src/app/core/auth.service.ts → src/app/dashboard/data.service.ts → src/app/dashboard/dashboard.component.ts
  ```

### 2. Use `dependency-cruiser` (more powerful rules & reporting)

```bash
npm install --save-dev dependency-cruiser

# Initialize default config
npx depcruise --init

# Run (detects circular by default)
npx depcruise src --validate .dependency-cruiser.js

# Or focused on circular only
npx depcruise src --include-only "^src" --output-type err --ruleset .dependency-cruiser.js
```

Many teams prefer it over madge in larger monorepos because you can enforce “no circulars” in CI.

### 3. Angular CLI + build flags (narrow down quickly)

```bash
# Very verbose output → often shows file just before crash
ng build --verbose

# Or with higher stack trace
NODE_OPTIONS="--stack-trace-limit=400" ng build --verbose

# Disable incremental → sometimes reveals clearer file name
ng build --no-progress --aot
```

### 4. Standalone-specific circulars (very common in Angular 17–21)

Typical pattern: recursive / parent ↔ child standalone components

```ts
// parent.component.ts
imports: [ChildComponent]

// child.component.ts
imports: [ParentComponent]   ← direct cycle
```

Fix pattern using `forwardRef`:

```ts
// child.component.ts
import { forwardRef } from '@angular/core';
imports: [forwardRef(() => ParentComponent)]
```

But to **find** them:

- madge still catches them (it follows ES imports)
- Temporarily comment imports in `app.config.ts` / root bootstrap → add back one by one
- Search codebase for mutual imports:

  ```bash
  # rough grep (adjust paths)
  grep -r "imports.*Component" src/app | grep -B1 -A1 "Component"
  ```

### Quick action checklist (2026 best practice)

1. `npx madge --circular --extensions ts src/ > circular.txt`
2. Open `circular.txt` — fix from shortest cycles first
3. Common culprits:
   - Barrel files (`index.ts` re-exporting modules/components)
   - Shared utils/service imported back into feature
   - Recursive standalone components without `forwardRef`
   - Old NgModule → standalone migration leftovers
4. After fixing → run `ng build --prod` to confirm
5. Add to `package.json` scripts:

   ```json
   "check-circular": "madge --circular --extensions ts src/"
   ```

   → run before commit / in CI

Madge remains the fastest and most Angular-community-recommended tool even in Angular 21.

**References:**

- https://angular.dev/errors/NG0919
- https://medium.com/@vkrntteotia/how-to-automatically-detect-circular-dependencies-in-your-angular-project-using-a-tool-called-madge-9c2f8ab77b4f
- https://timdeschryver.dev/blog/fixing-angular-standalone-components-that-have-a-circular-dependency
- https://www.npmjs.com/package/madge
- https://github.com/sverweij/dependency-cruiser
