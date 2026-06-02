---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Angular Legacy Linting Tools Deprecated
translated: false
type: note
---

In Angular 9 and older Angular versions, **TSLint** and **Codelyzer** worked together to enforce code quality and Angular-specific best practices:

## TSLint
TSLint was a static analysis tool for TypeScript code that:
- Checked for code quality issues, bugs, and style inconsistencies
- Enforced coding standards across your TypeScript files
- Provided configurable rules for formatting, naming conventions, and code patterns
- Helped maintain consistency in codebases

## Codelyzer
Codelyzer was a set of TSLint rules specifically designed for Angular applications that:
- Enforced Angular style guide recommendations
- Checked component, directive, and service naming conventions
- Validated template syntax and best practices
- Ensured proper use of Angular decorators and lifecycle hooks
- Caught Angular-specific anti-patterns

## How They Worked Together
You'd configure them in your `tslint.json` file:
```json
{
  "extends": ["tslint:recommended", "codelyzer"],
  "rules": {
    "component-class-suffix": true,
    "directive-selector": [true, "attribute", "app", "camelCase"],
    // other rules
  }
}
```

## Important Note: They're Deprecated
Both TSLint and Codelyzer are now **deprecated**:
- TSLint was deprecated in 2019
- The Angular team migrated to **ESLint** with **angular-eslint** as the replacement
- Angular 11+ uses ESLint by default

If you're working with Angular 9 or older projects, you might still encounter these tools, but for modern Angular development, you should migrate to ESLint and angular-eslint for linting capabilities.
