---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ng-bootstrap 20 与 Angular 21 的兼容性
translated: true
type: note
---

问题：ng-bootstrap 20.0.0 是否支持 Angular 版本 21.2.0，我们可以一起使用它们吗？

回答：

**是的，ng-bootstrap 20.0.0 支持 Angular 21.2.0**，并且您可以一起使用它们。

根据 ng-bootstrap 的官方兼容性表：

- ng-bootstrap **20.x.x** 需要 **Angular ^21.0.0**
  （插入符号 `^` 表示 >=21.0.0 且 <22.0.0）

由于 Angular 21.2.0 落入此范围 (>=21.0.0 <22.0.0)，因此完全兼容。

这也在项目的 npm 页面和入门文档中得到确认。ng-bootstrap 20.0.0 是专门为支持 Angular 21（大约 2025 年末发布）而发布的，最低版本提升至 Angular 21.0.0。

**最近版本的快速总结（供参考）：**

- ng-bootstrap 18.x → Angular ^19.0.0
- ng-bootstrap 19.x → Angular ^20.0.0
- ng-bootstrap 20.x → Angular ^21.0.0

因此，使用 **ng-bootstrap 20.0.0** 与 **Angular 21.2.0** 不仅可能——这是预期的和支持的组合。

参考资料：

- [https://ng-bootstrap.github.io/#/getting-started](https://ng-bootstrap.github.io/#/getting-started)
- [https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap](https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap)
- [https://github.com/ng-bootstrap/ng-bootstrap/releases/tag/20.0.0](https://github.com/ng-bootstrap/ng-bootstrap/releases/tag/20.0.0)
- [https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md](https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md)
