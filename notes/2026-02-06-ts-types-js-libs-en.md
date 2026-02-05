---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: TypeScript Types for JavaScript Libraries
translated: false
type: note
---

Yes, exactly! `@types/` packages are TypeScript type definition files for JavaScript libraries.

Here's how it works:

Many popular JavaScript libraries (like React, Express, Lodash) were written in plain JavaScript before TypeScript existed or without TypeScript in mind. When you use these libraries in a TypeScript project, TypeScript doesn't know what types the library's functions expect or return.

The `@types/` packages provide these type definitions. For example:
- `@types/react` - type definitions for React
- `@types/node` - type definitions for Node.js
- `@types/express` - type definitions for Express

These packages are maintained in the [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped) repository, a community effort to provide high-quality TypeScript type definitions.

**When do you need them?**
- If a package is written in JavaScript and doesn't include its own types
- Modern packages often include their own type definitions (bundled in the package itself), so you don't need a separate `@types/` package

**Example:**
```bash
npm install lodash          # JavaScript library
npm install -D @types/lodash  # TypeScript definitions
```

The `@types/` package doesn't change the runtime behavior at all - it just helps TypeScript understand the library's API during development and compilation.