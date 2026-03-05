---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular 21 NgBootstrap 指南
translated: true
type: note
---

**问题：** 哪个 ng-bootstrap 版本匹配 Angular 21？

**回答：** 

匹配 **Angular 21** 的 **ng-bootstrap** 版本是 **20.x.x** 系列（具体为 **@ng-bootstrap/ng-bootstrap@^20.0.0**）。

根据 ng-bootstrap 文档中的官方兼容性表：

- ng-bootstrap **20.x.x** 需要 **Angular ^21.0.0**
- 它已与 **Bootstrap CSS 5.3.8** 和 **Popper ^2.11.8** 测试

稳定的 **20.0.0** 版本于 2025 年 12 月 12 日发布，它明确将所需的最低 Angular 版本提升至 21.0.0。

较旧版本（例如 19.x 用于 Angular 20，18.x 用于 Angular 19）在不强制安装的情况下与 Angular 21 不兼容（通常由于 peer dependency 不匹配或 API 更改而导致问题）。

在 Angular 21 项目中安装匹配版本，请运行：

```bash
npm install @ng-bootstrap/ng-bootstrap@20
# or
ng add @ng-bootstrap/ng-bootstrap   # (it should pick a compatible version)
```

升级时始终检查最新的 changelog 或 getting-started 页面，以了解任何补丁更新或破坏性更改。

**参考：**  

- [https://ng-bootstrap.github.io/#/getting-started](https://ng-bootstrap.github.io/#/getting-started)
- [https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap](https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap)
- [https://github.com/ng-bootstrap/ng-bootstrap/releases](https://github.com/ng-bootstrap/ng-bootstrap/releases)