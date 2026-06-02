---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ng-bootstrap 20.0.0 和 Angular 21.0.0 时间线
translated: true
type: note
---

问题：ng-bootstrap 20.0.0 发布时，哪些 Angular 21 版本已经发布？

回答：

**ng-bootstrap 20.0.0 于 2025 年 12 月 12 日发布。**

当时，**Angular 21.0.0** 已经发布（2025 年 11 月 19 日），它是当时唯一可用的稳定次要版本。

- Angular 21 遵循其标准的半年一次的主要版本发布周期，**21.0.0** 于 2025 年 11 月中旬推出。
- ng-bootstrap 20.0.0 专门构建以支持 Angular ^21.0.0（意为 >=21.0.0 且 <22.0.0），其发布是在 Angular 21.0.0 稳定后大约三周。
- 截至 2025 年 12 月 12 日，尚未存在 21.1.x 或更高版本的次要发布：
  - Angular 21.1.x 稍后到来（大约 2026 年 1 月，1 月 12 日当周）。
  - Angular 21.2.x 更晚跟随（大约 2026 年 2 月，2 月 23 日当周）。

简而言之：ng-bootstrap 20.0.0 发布时，**仅有 Angular 21.0.0**（初始主要版本）可用。后来补丁/次要版本（21.0.x 补丁，然后 21.1、21.2 等）在 ng-bootstrap 20.0.0 之后发布。

这符合该项目的模式：ng-bootstrap 主要版本通常在相应的 Angular 主要版本之后不久跟随，以更新 peer dependencies 并确保兼容性。

参考资料：

- [https://github.com/ng-bootstrap/ng-bootstrap/releases/tag/20.0.0](https://github.com/ng-bootstrap/ng-bootstrap/releases/tag/20.0.0)
- [https://angular.dev/reference/releases](https://angular.dev/reference/releases)
- [https://github.com/angular/angular/releases](https://github.com/angular/angular/releases)
- [https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap](https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap)
- [https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md](https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md)
