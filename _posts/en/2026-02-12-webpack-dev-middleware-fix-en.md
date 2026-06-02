---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Webpack Dev Middleware Security Risk
translated: false
type: note
---

**Question:** Is the update from webpack-dev-middleware 5.3.3 to 5.3.4 a security fix update? And can we use overrides instead of upgrading Angular 14 to a higher version, since @angular-devkit/build-angular uses that package?

**Answer:**

Yes, the update from **webpack-dev-middleware 5.3.3** to **5.3.4** is specifically a **security fix** release.

It patches **CVE-2024-29180**, a **path traversal vulnerability** (also known as a file leak issue due to insufficient URL validation). Versions <= 5.3.3 are vulnerable, while 5.3.4 (and the corresponding patches in other major branches: 6.1.2 and 7.1.0) fix the problem by properly unescaping and normalizing URLs before processing them. This prevents attackers from accessing arbitrary local files on the developer's machine via crafted requests to the development server (especially dangerous if the dev server is exposed on a public interface or reachable via DNS rebinding / malicious links).

In Angular 14 projects, **@angular-devkit/build-angular** (used by `ng serve` and the webpack-based dev server) depends on an older version of webpack-dev-middleware (typically in the 5.x range around that time, which includes vulnerable versions like 5.3.3 or earlier). This often triggers high-severity warnings in `npm audit`.

You can avoid upgrading the entire Angular version (from 14 → 15/16/etc.) by using **npm overrides** (or yarn/pnpm equivalents) to force webpack-dev-middleware to 5.3.4 in your project. This is a common and effective workaround for this exact CVE in older Angular/CLI/Vue CLI setups.

Example for **package.json** (using npm overrides):

```json
{
  "overrides": {
    "@angular-devkit/build-angular": {
      "webpack-dev-middleware": "5.3.4"
    }
  }
}
```

After adding this:
- Delete `node_modules` and `package-lock.json` (or `yarn.lock` / `pnpm-lock.yaml`)
- Run `npm install` again

This should pull in 5.3.4 without breaking Angular 14's build/dev setup (as the 5.3.4 patch is backward-compatible within the 5.x series). Many developers have successfully used this approach for similar dependency-constrained projects.

Note: Overrides are a good temporary fix, but for long-term maintenance, consider migrating to a newer Angular version (which uses updated dependencies) or switching to the modern esbuild-based builder (available in newer Angular versions).

**References:**

- [https://nvd.nist.gov/vuln/detail/CVE-2024-29180](https://nvd.nist.gov/vuln/detail/CVE-2024-29180)
- [https://github.com/webpack/webpack-dev-middleware/security/advisories/GHSA-wr3j-pwj9-hqq6](https://github.com/webpack/webpack-dev-middleware/security/advisories/GHSA-wr3j-pwj9-hqq6)
- [https://github.com/webpack/webpack-dev-middleware/releases/tag/v5.3.4](https://github.com/webpack/webpack-dev-middleware/releases/tag/v5.3.4)
- [https://github.com/angular/angular-cli/issues/27334](https://github.com/angular/angular-cli/issues/27334)
