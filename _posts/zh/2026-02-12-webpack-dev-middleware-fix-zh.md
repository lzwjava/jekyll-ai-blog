---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Webpack Dev Middleware 安全风险
translated: true
type: note
---

**Question:** 从 webpack-dev-middleware 5.3.3 更新到 5.3.4 是安全修复更新吗？由于 @angular-devkit/build-angular 使用了该 package，我们能否使用 overrides 而不是将 Angular 14 升级到更高版本？

**Answer:**

是的，从 **webpack-dev-middleware 5.3.3** 到 **5.3.4** 的更新专门是一个 **security fix** 版本。

它修复了 **CVE-2024-29180**，这是一个 **path traversal vulnerability**（路径遍历漏洞，也称为由于 URL 验证不足导致的文件泄漏问题）。5.3.3 及以下版本存在漏洞，而 5.3.4（以及其他主要分支中的相应补丁：6.1.2 和 7.1.0）通过在处理 URL 之前对其进行正确的 unescaping 和 normalizing 修复了该问题。这可以防止攻击者通过向 development server 发送精心构造的请求，访问开发者机器上的任意本地文件（如果 dev server 暴露在公共接口上，或者通过 DNS rebinding / 恶意链接可达，则尤其危险）。

在 Angular 14 项目中，**@angular-devkit/build-angular**（由 `ng serve` 和基于 webpack 的 dev server 使用）依赖于较旧版本的 webpack-dev-middleware（通常在当时的 5.x 范围内，包括 5.3.3 或更早的漏洞版本）。这通常会在 `npm audit` 中触发高危漏洞警告。

你可以通过使用 **npm overrides**（或 yarn/pnpm 的等效功能）在项目中强制将 webpack-dev-middleware 指定为 5.3.4，从而避免升级整个 Angular 版本（从 14 → 15/16 等）。对于在旧版 Angular/CLI/Vue CLI 设置中解决此特定 CVE，这是一种常见且有效的 workaround。

**package.json** 示例（使用 npm overrides）：

```json
{
  "overrides": {
    "@angular-devkit/build-angular": {
      "webpack-dev-middleware": "5.3.4"
    }
  }
}
```

添加此配置后：
- 删除 `node_modules` 和 `package-lock.json`（或 `yarn.lock` / `pnpm-lock.yaml`）
- 再次运行 `npm install`

这应该会引入 5.3.4 版本，而不会破坏 Angular 14 的 build/dev 设置（因为 5.3.4 补丁在 5.x 系列中是向下兼容的）。许多开发者已成功在类似的受依赖限制的项目中使用此方法。

注意：Overrides 是一个很好的临时修复手段，但为了长期维护，请考虑迁移到较新的 Angular 版本（使用更新的 dependencies）或切换到现代的 esbuild-based builder（在较新的 Angular 版本中可用）。

**References:**

- [https://nvd.nist.gov/vuln/detail/CVE-2024-29180](https://nvd.nist.gov/vuln/detail/CVE-2024-29180)
- [https://github.com/webpack/webpack-dev-middleware/security/advisories/GHSA-wr3j-pwj9-hqq6](https://github.com/webpack/webpack-dev-middleware/security/advisories/GHSA-wr3j-pwj9-hqq6)
- [https://github.com/webpack/webpack-dev-middleware/releases/tag/v5.3.4](https://github.com/webpack/webpack-dev-middleware/releases/tag/v5.3.4)
- [https://github.com/angular/angular-cli/issues/27334](https://github.com/angular/angular-cli/issues/27334)
