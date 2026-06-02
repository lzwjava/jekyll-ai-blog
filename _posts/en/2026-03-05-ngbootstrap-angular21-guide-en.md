---
audio: false
generated: true
image: false
lang: en
layout: post
title: NgBootstrap for Angular 21 Guide
translated: false
type: note
---

**Question:** Which ng-bootstrap version matches Angular 21?

**Answer:**

The version of **ng-bootstrap** that matches **Angular 21** is the **20.x.x** series (specifically **@ng-bootstrap/ng-bootstrap@^20.0.0**).

According to the official compatibility table from the ng-bootstrap documentation:

- ng-bootstrap **20.x.x** requires **Angular ^21.0.0**
- It is tested with **Bootstrap CSS 5.3.8** and **Popper ^2.11.8**

The stable release **20.0.0** was published on December 12, 2025, and it explicitly bumps the minimum required Angular version to 21.0.0.

Older versions (e.g. 19.x for Angular 20, 18.x for Angular 19) are not compatible with Angular 21 without forcing installation (which usually breaks due to peer dependency mismatches or API changes).

To install the matching version in an Angular 21 project, run:

```bash
npm install @ng-bootstrap/ng-bootstrap@20
# or
ng add @ng-bootstrap/ng-bootstrap   # (it should pick a compatible version)
```

Always check the latest changelog or the getting-started page for any patch updates or breaking changes when upgrading.

**References:**

- [https://ng-bootstrap.github.io/#/getting-started](https://ng-bootstrap.github.io/#/getting-started)
- [https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap](https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap)
- [https://github.com/ng-bootstrap/ng-bootstrap/releases](https://github.com/ng-bootstrap/ng-bootstrap/releases)
