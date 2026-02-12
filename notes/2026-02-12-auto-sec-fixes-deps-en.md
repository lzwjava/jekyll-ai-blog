---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Automatic Security Fixes for Dependencies
translated: false
type: note
---

**Question:** Explain what "npm audit fix" does

**Answer:**

`npm audit fix` is a command that **automatically attempts to fix** security vulnerabilities found in your project's dependencies.

Here's a clear breakdown of what it does and how it works:

### What `npm audit` does first
```bash
npm audit
```
- Scans your dependency tree (everything in `package-lock.json` or `npm-shrinkwrap.json`)
- Checks against the npm security database
- Reports known vulnerabilities with severity (low / moderate / high / critical)
- Shows which packages are vulnerable and suggests fixed versions

### What `npm audit fix` actually does
```bash
npm audit fix
```

1. Looks at the vulnerabilities reported by `npm audit`
2. For each vulnerability, tries to install a **semvert-compatible** fixed version:
   - patch version update → allowed (1.2.3 → 1.2.17)
   - minor version update → allowed (1.2.0 → 1.5.1)
   - **major** version update → **NOT** allowed by default
3. Updates `package-lock.json` (and `npm-shrinkwrap.json` if present)
4. **Does NOT** change `package.json` ranges (unless you use `--force`)

### Most common outcomes

| Situation                              | What `npm audit fix` does                     | Result in package-lock.json |
|----------------------------------------|------------------------------------------------|------------------------------|
| Fix available in patch/minor range     | Updates to safe version                        | Updated                      |
| Fix requires major version bump        | Skipped (ignored)                              | No change                    |
| Package is a devDependency             | Usually still fixes it                         | Updated                      |
| Package is direct dependency           | Fixes if semver allows                         | Updated                      |
| Vulnerability in transitive dependency | Tries to update the top-level package         | May update several packages  |

### Important variants

```bash
npm audit fix --force
```
- Also installs **breaking** (major) version updates when needed
- Very risky — can break your application
- Use only when you are prepared to test and fix breaking changes

```bash
npm audit fix --dry-run
```
- Shows what *would* be changed without actually modifying files

```bash
npm audit fix --package-lock-only
```
- Only updates `package-lock.json`, doesn't touch `node_modules`
- Useful in CI / lockfile-only workflows

### Quick decision table (2024–2026 practice)

| You want...                                 | Recommended command                     | Risk level |
|---------------------------------------------|------------------------------------------|------------|
| Safe, automatic fixes                       | `npm audit fix`                          | Low        |
| See what would change                       | `npm audit fix --dry-run`                | None       |
| Fix almost everything (careful!)            | `npm audit fix --force`                  | High       |
| Only update lockfile (CI/monorepo)          | `npm audit fix --package-lock-only`      | Low        |
| Just understand the problems                | `npm audit` or `npm audit --json`        | None       |

### Modern recommendations (2025–2026)

Most teams now prefer:

1. `npm audit --audit-level=high`  
   → only care about high + critical

2. `npm audit fix`  
   → apply safe fixes regularly

3. Dependabot, Renovate or Socket.dev  
   → create PRs for both version updates **and** security fixes

`npm audit fix` is convenient, but it's not magic — it cannot fix vulnerabilities that require:
- code changes in your app
- major version upgrades
- removing the dependency completely

**References:**

- [https://docs.npmjs.com/cli/v10/commands/npm-audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [https://docs.npmjs.com/cli/v10/commands/npm-audit-fix](https://docs.npmjs.com/cli/v10/commands/npm-audit-fix)