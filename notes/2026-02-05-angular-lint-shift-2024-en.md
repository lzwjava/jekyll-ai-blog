---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Angular Linting Shift TSLint to ESLint
translated: false
type: note
---

Yes, you're on the right track! Here's what happened with those transitions:

**Webpack**: Angular has used webpack as its underlying bundler since Angular 2+, including both Angular 9 and Angular 14. This didn't change between those versions.

**TSLint → ESLint transition**: This is correct!

- **Angular 9 and earlier**: Used TSLint for linting TypeScript code
- **Angular 11**: TSLint was officially deprecated, and the Angular team recommended migrating to ESLint
- **Angular 12+**: New projects started using ESLint by default via `@angular-eslint`
- **Angular 14**: Continued using ESLint (TSLint support was completely removed)

The switch happened because TSLint itself was deprecated by its maintainers in 2019, with the recommendation to move to ESLint. The Angular team created `@angular-eslint` to provide Angular-specific linting rules for ESLint.

If you're migrating an older Angular 9 project to Angular 14, you'd need to migrate from TSLint to ESLint as part of the upgrade process. The Angular team provided migration schematics to help automate this transition.
