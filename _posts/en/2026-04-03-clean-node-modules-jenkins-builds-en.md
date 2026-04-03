---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean node_modules in Jenkins Builds
translated: false
type: note
---

**Question:** On the same Jenkins build node, if `node_modules` from npm packages persists across builds, do we need to clean them up? Keeping them might cause dependency conflicts between different builds, leading to errors — is this correct?

**Answer:**

## Yes — But It's More Nuanced Than a Hard "Always Clean"

Your concern is **valid and correct in principle**. Shared, leftover `node_modules` on the same Jenkins build node can absolutely cause cross-build contamination. However, whether you *must* delete them depends on your npm version and workflow. Here's a full breakdown:

---

## Why Leftover `node_modules` Can Cause Problems

1. **Stale/orphaned packages** — If a previous build installed packages that are no longer in `package.json`, they stay in `node_modules` silently. A new build can accidentally pick them up.
2. **Version conflicts between branches** — Branch A might use `lodash@4.x`, Branch B uses `lodash@3.x`. If the same workspace/node is reused without cleaning, the wrong version may persist.
3. **Corrupted installs** — If a previous build crashed mid-install, `node_modules` may be in a broken/partial state.
4. **Non-reproducible builds** — Builds depend on hidden local state rather than what's declared in `package.json`, making debugging extremely hard.

---

## What npm Does Automatically (Modern npm ≥ v3)

Since npm 3, npm keeps track of resolved dependencies in `package-lock.json`, guaranteeing that the same dependency versions are used regardless of the prior state of `node_modules`. Additionally, `npm install` will remove packages that are not in `package.json` / `package-lock.json`, so packages from earlier builds that are no longer needed will be removed automatically.

This means **modern `npm install` handles many cases** — but it does NOT protect against:
- Manual tampering with `node_modules`
- Corrupted mid-build states
- Platform-specific binaries being stale (e.g., native addons)
- Multiple different projects sharing the same workspace directory

---

## Recommended Strategies

### ✅ Option 1: Full Clean Before Each Build (Safest, Slowest)
Delete `node_modules` entirely before every build for guaranteed reproducibility:

```bash
rm -rf node_modules
npm install
```

In Jenkinsfile:
```groovy
stage('Install') {
    steps {
        sh 'rm -rf node_modules'
        sh 'npm install'
    }
}
```

### ✅ Option 2: Use `npm ci` Instead of `npm install` (Best Practice for CI)
`npm ci` is designed for CI environments — it **always deletes `node_modules` and reinstalls from scratch** based on `package-lock.json`:

```bash
npm ci
```

This is the **recommended CI approach** because it:
- Guarantees a clean install every time
- Is faster than `rm -rf node_modules && npm install` in many cases
- Strictly respects `package-lock.json`

### ✅ Option 3: Use `npm prune` (Lighter Cleanup)
If you want speed and only need to remove orphaned packages:

```bash
npm prune
npm install
```

`npm prune` removes extraneous packages — those present in `node_modules` but not listed as any package's dependency. It can also remove `devDependencies` when the `--production` flag is used.

### ✅ Option 4: Jenkins Workspace Cleanup Plugin
You can use the Jenkins Workspace Cleanup Plugin to clean the workspace before or after builds. For example, you can clean everything but exclude `node_modules` if you want to cache it for future builds, or include it to ensure a clean state.

Example Jenkinsfile with clean before build:
```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                cleanWs()       // wipe workspace
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'npm ci'     // always clean install
                sh 'npm run build'
            }
        }
    }
    post {
        always {
            cleanWs(deleteDirs: true, notFailBuild: true)
        }
    }
}
```

---

## Summary Table

| Strategy | Clean? | Speed | Safety |
|---|---|---|---|
| `npm install` (reuse node_modules) | No | Fast | Medium (npm 3+ handles most cases) |
| `npm prune` + `npm install` | Partial | Medium | Good |
| `rm -rf node_modules` + `npm install` | Full | Slow | Best |
| `npm ci` | Full (auto) | Medium-Fast | Best for CI |
| Jenkins `cleanWs()` | Full workspace | Slowest | Best |

**TL;DR:** Use **`npm ci`** in Jenkins pipelines — it was built exactly for this use case and eliminates the cross-build contamination issue you described without requiring you to manually manage `node_modules` cleanup.

---

**References:**

- [Jenkins Workspace Cleanup Plugin](https://plugins.jenkins.io/ws-cleanup/)
- [Automatically Clean Up Jenkins Workspace](https://computingpost.medium.com/automatically-clean-up-jenkins-workspace-after-builds-complete-d3f29f230a5f)
- [Is it necessary to remove node_modules before a build server build?](https://software.codidact.com/posts/280097)
- [How to clean up node_modules](https://medium.com/@mariokandut/how-to-clean-up-node-modules-41a5)