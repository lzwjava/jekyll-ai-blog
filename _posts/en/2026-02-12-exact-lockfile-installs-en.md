---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Exact Lockfile Installations
translated: false
type: note
---

**Question:** Explain what `npm ci` does

**Answer:**

`npm ci` is a command specifically designed for **clean and reproducible installations** of dependencies — most commonly used in CI/CD pipelines, Docker builds, automated tests, and production-like environments.

### Key differences: `npm install` vs `npm ci`

| Feature                          | `npm install` (or `npm i`)                  | `npm ci`                                      |
|-------------------------------|-----------------------------------------------|-----------------------------------------------|
| Reads                            | `package.json`                               | `package-lock.json` (required)                |
| Writes / updates                 | `package-lock.json` (if missing or outdated) | Never modifies `package-lock.json`            |
| Creates / deletes `node_modules` | Usually only adds missing packages           | **Always deletes** existing `node_modules` first |
| Allowed when `package-lock.json` is missing? | Yes                                          | **No** — fails with error                     |
| Installs exact versions          | Tries to (if lockfile exists), but can still change | **Always** installs exact versions from lockfile |
| Can install new packages         | Yes (`npm install lodash`)                   | **No** — fails if you try                     |
| Speed                            | Slower when lockfile is outdated             | Usually faster (no dependency resolution)     |
| Main use case                    | Local development, adding/updating packages  | CI, CD, Docker, production builds, tests      |

### What `npm ci` actually does (step by step)

1. Deletes the existing `node_modules` folder (if it exists)
2. Checks that `package-lock.json` exists — if not → fails
3. Reads **only** `package-lock.json` (ignores `package.json` versions)
4. Installs **exactly** the dependency tree described in the lockfile
5. Does **not** update or re-generate the lockfile
6. Does **not** run `prepare` scripts of dependencies (since 7.x — faster)

### Typical real-world usage patterns

```bash
# In CI/CD pipelines (GitHub Actions, GitLab CI, CircleCI, Jenkins, etc.)
npm ci
npm test

# In Dockerfile — very common pattern
COPY package.json package-lock.json ./
RUN npm ci --omit=dev          # or --production in older versions
COPY . .
```

```bash
# Local development — you usually still use:
npm install

# But sometimes you want to reproduce CI exactly:
rm -rf node_modules
npm ci
```

### Common error messages and what they mean

```
npm ERR! ci can only install packages with an exact version number in package-lock.json
→ you modified package.json but didn't run npm install to update the lockfile

npm ERR! Missing script: "ci"
→ no, just means package-lock.json is missing

npm ERR! cb() never called!
→ very rare nowadays — usually means disk/full cache problems
```

### Quick rule of thumb

- Developing / adding / updating dependencies → `npm install`
- Want exact same dependency tree as in lockfile (CI, tests, Docker, production builds) → `npm ci`

**Bottom line:**
`npm ci` = "install exactly what's in package-lock.json, nothing else, and don't touch the lockfile"

**References:**

- https://docs.npmjs.com/cli/v10/commands/npm-ci
- https://blog.npmjs.org/post/178027064160/next-generation-package-management
