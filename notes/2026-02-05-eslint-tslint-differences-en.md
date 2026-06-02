---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: ESLint vs TSLint Key Differences Explained
translated: false
type: note
---

Here are the key differences between TSLint and ESLint:

**1. Language Focus**

- **TSLint**: Built specifically for TypeScript only
- **ESLint**: Originally for JavaScript, but now supports TypeScript through `@typescript-eslint/parser`

**2. Maintenance Status**

- **TSLint**: Deprecated in 2019, no longer maintained
- **ESLint**: Actively maintained and developed

**3. Performance**

- **TSLint**: Generally slower, uses TypeScript's compiler API directly
- **ESLint**: Faster for most use cases, more efficient parsing

**4. Ecosystem & Plugin Support**

- **TSLint**: Smaller ecosystem, fewer plugins available
- **ESLint**: Massive ecosystem with thousands of plugins and configurations (Prettier integration, React rules, accessibility rules, etc.)

**5. Configuration**

- **TSLint**: Used `tslint.json`
- **ESLint**: Uses `.eslintrc.json` (or .js, .yml variants)

**6. Rule Coverage**

- **TSLint**: TypeScript-specific rules only
- **ESLint**: Covers JavaScript + TypeScript, plus framework-specific rules (React, Vue, Angular)

**7. Community & Future**

- **TSLint**: Dead project, no future development
- **ESLint**: Industry standard, continues evolving with new JavaScript/TypeScript features

**Why the switch happened**: The TypeScript team and TSLint maintainers decided that rather than maintaining two separate linting tools, it made more sense to consolidate efforts around ESLint with TypeScript support. This gives the community one powerful, well-maintained tool for all JavaScript and TypeScript linting needs.
