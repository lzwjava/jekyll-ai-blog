---
audio: false
generated: true
image: false
lang: en
layout: post
title: TypeScript Local Setup Guide Steps
translated: false
type: note
---

To run TypeScript locally, you’ll usually use **npm** and the TypeScript compiler (`tsc`). Here’s a step-by-step guide:

---

### 1. Initialize Your Project

If you don’t already have a `package.json`:

```bash
npm init -y
```

This creates a `package.json` so you can manage dependencies.

---

### 2. Install TypeScript

Install it as a dev dependency:

```bash
npm install typescript --save-dev
```

If you also want the TypeScript compiler (`tsc`) available globally:

```bash
npm install -g typescript
```

---

### 3. Create a tsconfig.json

Generate a default config file:

```bash
npx tsc --init
```

This creates `tsconfig.json` which controls how TypeScript compiles your files (target, module system, strict mode, etc.).

---

### 4. Write a TypeScript File

Example `index.ts`:

```ts
function greet(name: string): string {
  return `Hello, ${name}!`;
}

console.log(greet("World"));
```

---

### 5. Compile TypeScript

Run:

```bash
npx tsc
```

This compiles all `.ts` files according to `tsconfig.json`.

Or, to compile just one file:

```bash
npx tsc index.ts
```

This generates a `.js` file (e.g., `index.js`).

---

### 6. Run the Compiled JavaScript

Use Node.js:

```bash
node index.js
```

---

### 7. Optional: Auto-compile on Save

Run with `--watch` so it recompiles whenever you edit:

```bash
npx tsc --watch
```

---

👉 That’s the standard workflow:
`npm install` → `tsc` (compile) → `node` (run compiled code).

---

Do you want me to also show you how to **skip manual compilation** by running TypeScript directly with `ts-node`?
