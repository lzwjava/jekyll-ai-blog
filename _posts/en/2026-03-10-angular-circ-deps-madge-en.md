---
audio: false
generated: true
image: false
lang: en
layout: post
title: Detect Angular Circular Dependencies with Madge
translated: false
type: note
---

Question: How do I use Madge in an Angular project to detect circular dependencies?

Answer:

## What is Madge?

Madge is a developer tool for generating a visual graph of your module dependencies, finding circular dependencies, and giving you other useful info. It works for JavaScript (AMD, CommonJS, and ES6 modules) and also for CSS preprocessors (Sass, Stylus, and Less).

---

## Step 1: Install Madge

Install Madge globally (or as a dev dependency):

```bash
# Global install
npm install -g madge

# Or as dev dependency
npm install --save-dev madge
```

If you want to **generate visual graph images**, you also need Graphviz:

```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz
```

---

## Step 2: Basic Usage — Detect Circular Dependencies

Run from your Angular project **root directory**:

```bash
# Scan the entire src/ folder for circular dependencies
npx madge --circular src/
```

Or, for better TypeScript support, point it to `main.ts` with the `tsconfig.json`:

```bash
npx madge --circular src/main.ts --ts-config tsconfig.json
```

By running `npx madge --circular --extensions ts ./` you can quickly get a list of circular dependencies of all `.ts` files in the current directory and its subdirectories.

---

## Step 3: Generate a Visual Dependency Graph

Run `npx madge src/main.ts --ts-config tsconfig.json --image ./deps.png` to go through your entire application and create a dependency graph as an image. This can be used to identify circular dependencies, visualize relationships between your different components and services, and identify spaghetti code scenarios.

To generate a graph showing **only circular** dependencies:

```bash
npx madge --circular --extensions ts --image circular-graph.png src/
```

**Graph color legend:**
- **Blue** — files that have dependencies
- **Green** — files with no dependencies
- **Red** — files with circular dependencies

---

## Step 4: Useful Commands Summary

| Purpose | Command |
|---|---|
| Detect circular deps | `npx madge --circular src/` |
| With TypeScript support | `npx madge --circular --extensions ts src/` |
| With tsconfig | `npx madge --circular src/main.ts --ts-config tsconfig.json` |
| Generate full graph image | `npx madge --image deps.png src/main.ts --ts-config tsconfig.json` |
| Find orphan/dead code | `npx madge --orphans src/main.ts --ts-config tsconfig.json` |

---

## Step 5: Add to `package.json` Scripts

Inside your Angular project, go to `package.json` and add custom scripts:

```json
"scripts": {
  "check:circles": "madge --circular src/",
  "check:graph": "madge --image dependency-graph.png src/"
}
```


Then run any time with:

```bash
npm run check:circles
```

---

## Step 6: Skip Type-Only Imports (Recommended for Angular/TypeScript)

TypeScript `import type` statements can cause false positives. To skip them, add this configuration to `package.json`:

```json
"madge": {
  "detectiveOptions": {
    "ts": {
      "skipTypeImports": true,
      "skipAsyncImports": true
    },
    "tsx": {
      "skipTypeImports": true,
      "skipAsyncImports": true
    }
  }
}
```

---

## Step 7: Add to CI/CD Pipeline

Add Madge to your CI/CD pipeline to prevent circular dependencies from creeping back into your Angular project.

Example for GitLab CI:

```yaml
stages:
  - test

circular-dependency-check:
  stage: test
  image: node:18
  script:
    - npm install madge -g
    - npm install
    - npm run check:circles
  allow_failure: false
```

---

## Example Output

```
✖ Found 3 circular dependencies!

1) src/app/services/service-a.ts → src/app/services/service-b.ts → src/app/services/service-a.ts
2) src/app/module-a.module.ts → src/app/module-b.module.ts → src/app/module-a.module.ts
```

---

## How to Fix Circular Dependencies

To fix a circular reference issue, create a new file to break the relations and ensure that the dependencies between files are unidirectional, extracting the common dependencies into a separate shared file. Common strategies:

- **Extract shared interfaces/types** into a separate `models/` or `shared/` file
- **Create a shared module** for common functionality
- **Reorganize modules** to separate concerns and ensure one-directional dependency flow

References:

- [https://www.angulartraining.com/daily-newsletter/visualizing-internal-dependencies-with-madge/](https://www.angulartraining.com/daily-newsletter/visualizing-internal-dependencies-with-madge/)
- [https://www.npmjs.com/package/madge](https://www.npmjs.com/package/madge)
- [https://www.danywalls.com/how-to-detect-and-fix-circular-dependencies-in-typescript](https://www.danywalls.com/how-to-detect-and-fix-circular-dependencies-in-typescript)
- [https://angular.dev/errors/NG0919](https://angular.dev/errors/NG0919)
- [https://dev.to/greenroach/detecting-circular-dependencies-in-a-reacttypescript-app-using-madge-229](https://dev.to/greenroach/detecting-circular-dependencies-in-a-reacttypescript-app-using-madge-229)
